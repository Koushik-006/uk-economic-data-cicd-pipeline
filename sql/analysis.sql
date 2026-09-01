-- Latest observation for each economic indicator.
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY dataset ORDER BY date DESC) AS row_num
    FROM economic_indicators
)
SELECT dataset, date, value, unit
FROM ranked
WHERE row_num = 1
ORDER BY dataset;

