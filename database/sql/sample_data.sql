-- Sample Data Inserts for Time Series Market Database
-- Author: Michael Kimani
-- Date: 2026-02-28

-- Insert sample asset data
INSERT INTO assets (asset_name, asset_type, ticker_symbol) VALUES 
('US Equities', 'equity', 'SPY'),
('Technology Stocks', 'equity', 'XLK'),
('Emerging Markets', 'equity', 'EEM'),
('Long-Term Bonds', 'bond', 'TLT'),
('Gold', 'commodity', 'GLD'),
('Crude Oil', 'commodity', 'USO'),
('Bitcoin', 'crypto', 'BTC');

-- Insert sample market data
INSERT INTO market_data (date, equities_us, equities_tech, equities_emerging, bonds_longterm, gold, oil, volatility_index, crypto_bitcoin, yield_curve_spread, high_yield_spread, financial_stress_index) VALUES
('2026-02-19', 668.00, 595.50, 60.25, 88.50, 470.00, 79.50, 19.20, 62000.00, 0.55, 2.80, -0.5950),
('2026-02-20', 670.50, 598.00, 60.80, 88.75, 471.50, 79.80, 19.50, 62500.00, 0.56, 2.82, -0.6000),
('2026-02-21', 675.00, 602.00, 61.50, 89.00, 473.00, 80.00, 19.80, 63000.00, 0.57, 2.83, -0.6050),
('2026-02-22', 678.20, 605.00, 62.00, 89.50, 474.00, 80.50, 20.00, 63500.00, 0.58, 2.85, -0.6100),
('2026-02-23', 680.50, 607.00, 62.30, 89.75, 474.50, 80.60, 20.50, 64000.00, 0.59, 2.88, -0.6150),
('2026-02-24', 682.39, 607.50, 62.50, 89.85, 474.55, 80.70, 21.01, 64616.74, 0.60, 2.90, -0.6180),
('2026-02-25', 687.35, 607.87, 62.62, 89.90, 474.61, 80.76, 19.55, 65568.49, 0.61, 2.95, -0.6208);

-- Insert sample predictions
INSERT INTO predictions (date, model_name, predicted_value, actual_value, prediction_error) VALUES
('2026-02-25', 'RandomForest', -0.0472, -0.0450, 0.0022),
('2026-02-24', 'RandomForest', -0.0350, -0.0320, 0.0030),
('2026-02-23', 'LinearRegression', -0.0280, -0.0300, -0.0020);

-- Verify data
SELECT * FROM assets;
SELECT * FROM market_data ORDER BY date DESC LIMIT 5;
SELECT * FROM predictions ORDER BY prediction_id DESC LIMIT 3;

