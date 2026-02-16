TRUNCATE TABLE stg_logs;

INSERT INTO stg_logs (
    log_id,
    log_timestamp,
    log_date,
    log_hour,
    log_level,
    service_name,
    message,
    is_error
)
SELECT
    id,
    log_timestamp,
    DATE(log_timestamp),
    EXTRACT(HOUR FROM log_timestamp),
    log_level,
    service_name,
    message,
    CASE WHEN log_level = 'ERROR' THEN TRUE ELSE FALSE END
FROM raw_logs;
