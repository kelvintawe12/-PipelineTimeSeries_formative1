-- SQL Queries for Time Series Data
-- Author: Michael Kimani

-- Query 1: Get latest record
SELECT date, equities_us, gold, volatility_index, financial_stress_index
FROM market_data
ORDER BY date DESC
LIMIT 1;

-- Expected Result:
-- date       | equities_us | gold   | volatility_index | financial_stress_index
-- 2026-02-25 | 687.35      | 474.61 | 19.55            | -0.6208


-- Query 2: Get records by date range
SELECT date, equities_us, volatility_index
FROM market_data
WHERE date BETWEEN '2026-02-23' AND '2026-02-25'
ORDER BY date ASC;

-- Expected Result:
-- date       | equities_us | volatility_index
-- 2026-02-23 | 682.39      | 21.01
-- 2026-02-24 | 687.35      | 19.55
-- 2026-02-25 | 687.35      | 19.55


-- Query 3: Aggregate statistics for high stress periods
SELECT 
    YEAR(date) as year,
    COUNT(*) as total_records,
    AVG(volatility_index) as avg_volatility,
    MAX(financial_stress_index) as max_stress,
    MIN(financial_stress_index) as min_stress
FROM market_data
WHERE financial_stress_index < -0.5
GROUP BY YEAR(date)
ORDER BY year DESC;

-- Expected Result:
-- year | total_records | avg_volatility | max_stress | min_stress
-- 2026 | 3             | 20.04          | -0.6208    | -0.6208
