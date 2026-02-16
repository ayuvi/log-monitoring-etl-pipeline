-- RAW
CREATE TABLE IF NOT EXISTS raw_logs (
    id SERIAL PRIMARY KEY,
    log_timestamp TIMESTAMP,
    log_level VARCHAR(10),
    service_name VARCHAR(50),
    message TEXT
);

-- STAGING (cleaned & enriched layer)
CREATE TABLE IF NOT EXISTS stg_logs (
    log_id INTEGER,
    log_timestamp TIMESTAMP,
    log_date DATE,
    log_hour INTEGER,
    log_level VARCHAR(10),
    service_name VARCHAR(50),
    message TEXT,
    is_error BOOLEAN
);


-- MART
CREATE TABLE IF NOT EXISTS log_summary (
    log_date DATE,
    log_level VARCHAR(10),
    total INTEGER
);

-- MART: error summary per service per day
CREATE TABLE IF NOT EXISTS mart_error_summary (
    log_date DATE,
    service_name VARCHAR(50),
    total_error INTEGER
);

CREATE DATABASE grafana;
