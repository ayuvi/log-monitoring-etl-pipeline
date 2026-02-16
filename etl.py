import os
import time
import logging
import psycopg2
from datetime import datetime


# ==============================
# DATABASE CONFIG (FIXED)
# ==============================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "dbname": os.getenv("DB_NAME", "app_monitoring"),  # ✅ dbname not database
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppass"),
    "port": os.getenv("DB_PORT", "5432"),
}

print("DB CONFIG =", DB_CONFIG)


# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)


# ==============================
# DB CONNECTION
# ==============================

def connect_db(max_retries=5, delay=3):
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            logging.info("Database connected")
            return conn

        except Exception as e:
            logging.error(f"Connection failed ({attempt}/{max_retries}): {e}")
            time.sleep(delay)

    logging.error("Max retries exceeded. Could not connect to database.")
    return None


# ==============================
# LOG PARSER
# ==============================

def parse_log_line(line):
    line = line.strip()
    if not line:
        return None

    parts = line.split(" ", 4)

    if len(parts) < 5:
        logging.warning(f"Skipping malformed log: {line}")
        return None

    timestamp = f"{parts[0]} {parts[1]}"
    log_level = parts[2]
    service = parts[3]
    message = parts[4]

    return (
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        log_level,
        service,
        message
    )


# ==============================
# ALERT CHECK
# ==============================

def check_error_alert(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM raw_logs
            WHERE log_level = 'ERROR'
        """)
        error_count = cur.fetchone()[0]

        if error_count >= 2:
            logging.warning(f"ALERT: High error count detected! Total ERROR = {error_count}")


# ==============================
# TRANSFORMATION
# ==============================

def run_sql_file(conn, filename):
    with conn.cursor() as cur:
        with open(filename, "r") as f:
            sql = f.read()
            cur.execute(sql)
    conn.commit()


# ==============================
# MAIN ETL
# ==============================

def main():
    conn = connect_db()

    if conn is None:
        logging.error("Stopping ETL due to database connection failure.")
        return

    with conn:
        with conn.cursor() as cur:

            # truncate
            cur.execute("TRUNCATE TABLE raw_logs;")

            insert_query = """
                INSERT INTO raw_logs 
                (log_timestamp, log_level, service_name, message)
                VALUES (%s, %s, %s, %s)
            """

            with open("data/app.log", "r") as f:
                for line in f:
                    record = parse_log_line(line)
                    if record:
                        cur.execute(insert_query, record)

        conn.commit()

        # transformation & mart
        run_sql_file(conn, "transform.sql")
        run_sql_file(conn, "mart.sql")

        # alert check
        check_error_alert(conn)

    conn.close()
    logging.info("ETL load success!")


if __name__ == "__main__":
    main()
