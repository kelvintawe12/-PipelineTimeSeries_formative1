-- SQL Database Schema for Time Series Market Data
-- Author: Michael Kimani
-- Date: 2026-02-28

-- Table 1: assets - Reference table for financial instruments
CREATE TABLE assets (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(100) NOT NULL,
    asset_type ENUM('equity', 'bond', 'commodity', 'crypto', 'index') NOT NULL,
    ticker_symbol VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: market_data - Main time series data
CREATE TABLE market_data (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    equities_us DECIMAL(10, 2),
    equities_tech DECIMAL(10, 2),
    equities_emerging DECIMAL(10, 2),
    bonds_longterm DECIMAL(10, 2),
    gold DECIMAL(10, 2),
    oil DECIMAL(10, 2),
    volatility_index DECIMAL(10, 2),
    crypto_bitcoin DECIMAL(12, 2),
    yield_curve_spread DECIMAL(10, 2),
    high_yield_spread DECIMAL(10, 2),
    financial_stress_index DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_date (date),
    INDEX idx_financial_stress (financial_stress_index)
);

-- Table 3: predictions - Store model predictions
CREATE TABLE predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    predicted_value DECIMAL(10, 4),
    actual_value DECIMAL(10, 4),
    prediction_error DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (date) REFERENCES market_data(date),
    INDEX idx_model (model_name),
    INDEX idx_prediction_date (date)
);
