TRUNCATE TABLE mart_error_summary;

INSERT INTO mart_error_summary (
    log_date,
    service_name,
    total_error
)
SELECT
    log_date,
    service_name,
    COUNT(*)
FROM stg_logs
WHERE is_error = TRUE
GROUP BY log_date, service_name;


