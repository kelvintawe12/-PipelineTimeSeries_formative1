"""
Preprocessing utilities for time-series data.
Handles feature engineering for model predictions.
"""
import pandas as pd
import numpy as np


def create_features(df):
    """
    Alias for preprocess_data - creates lag features, moving averages, etc.
    """
    return preprocess_data(df)


def preprocess_data(df):
    """
    Preprocess raw time-series data for model prediction.
    Creates lag features, moving averages, and rolling correlations.
    
    Args:
        df: DataFrame with raw market data
    
    Returns:
        DataFrame with engineered features
    """
    # Ensure required columns exist
    required_cols = ['Equities_US', 'Financial_Stress_Index']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Convert to numeric
    df = df.copy()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Handle missing values - forward fill then backward fill
    df = df.ffill().bfill()
    
    # Feature engineering
    # Lag features
    df['lag_1'] = df['Equities_US'].shift(1)
    df['lag_7'] = df['Equities_US'].shift(7)
    
    # Moving averages
    df['ma_7'] = df['Equities_US'].rolling(window=7).mean()
    
    # Volatility
    df['vol_7'] = df['Equities_US'].pct_change().rolling(7).std() * np.sqrt(252)
    
    # Rolling correlation
    df['rolling_corr_30'] = df['Equities_US'].rolling(window=30).corr(df['Financial_Stress_Index'])
    
    # Return
    df['return_1d'] = df['Equities_US'].pct_change()
    
    # Drop NaN rows created by lag/rolling operations
    df = df.dropna()
    
    return df


def extract_features(df, feature_columns):
    """
    Extract specific features for model prediction.
    
    Args:
        df: DataFrame with engineered features
        feature_columns: List of column names to use as features
    
    Returns:
        numpy array of features
    """
    # Check for missing features
    missing_features = [col for col in feature_columns if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")
    
    # Extract features
    features = df[feature_columns].values
    
    # Handle any remaining NaN values
    features = np.nan_to_num(features, nan=0.0)
    
    return features


def prepare_prediction_input(data_dict, feature_columns):
    """
    Prepare a single prediction input from a dictionary.
    
    Args:
        data_dict: Dictionary with market data
        feature_columns: List of required feature columns
    
    Returns:
        numpy array ready for model prediction
    """
    # Create a single-row DataFrame
    df = pd.DataFrame([data_dict])
    df['Date'] = pd.to_datetime(df.get('Date', pd.Timestamp.now()))
    df = df.set_index('Date')
    
    # Preprocess
    df = preprocess_data(df)
    
    # Extract features
    features = extract_features(df, feature_columns)
    
    return features


def format_market_data_for_db(data_dict):
    """
    Format market data for database insertion.
    
    Args:
        data_dict: Raw market data dictionary
    
    Returns:
        Formatted dictionary for SQL/MongoDB insertion
    """
    formatted = {
        'date': data_dict.get('Date', pd.Timestamp.now().strftime('%Y-%m-%d')),
        'equities_us': float(data_dict.get('Equities_US', 0)),
        'equities_tech': float(data_dict.get('Equities_Tech', 0)),
        'equities_emerging': float(data_dict.get('Equities_Emerging', 0)),
        'bonds_longterm': float(data_dict.get('Bonds_LongTerm', 0)),
        'gold': float(data_dict.get('Gold', 0)),
        'oil': float(data_dict.get('Oil', 0)),
        'volatility_index': float(data_dict.get('Volatility_Index', 0)),
        'crypto_bitcoin': float(data_dict.get('Crypto_Bitcoin', 0)),
        'yield_curve_spread': float(data_dict.get('Yield_Curve_Spread', 0)),
        'high_yield_spread': float(data_dict.get('High_Yield_Spread', 0)),
        'financial_stress_index': float(data_dict.get('Financial_Stress_Index', 0))
    }
    return formatted


def format_mongodb_doc(data_dict):
    """
    Format market data as MongoDB document with nested structure.
    
    Args:
        data_dict: Raw market data dictionary
    
    Returns:
        MongoDB document structure
    """
    doc = {
        '_id': data_dict.get('Date', pd.Timestamp.now().strftime('%Y-%m-%d')),
        'date': data_dict.get('Date', pd.Timestamp.now().isoformat()),
        'equities': {
            'us': float(data_dict.get('Equities_US', 0)),
            'tech': float(data_dict.get('Equities_Tech', 0)),
            'emerging': float(data_dict.get('Equities_Emerging', 0))
        },
        'commodities': {
            'gold': float(data_dict.get('Gold', 0)),
            'oil': float(data_dict.get('Oil', 0))
        },
        'crypto': {
            'bitcoin': float(data_dict.get('Crypto_Bitcoin', 0))
        },
        'bonds': {
            'longterm': float(data_dict.get('Bonds_LongTerm', 0))
        },
        'indicators': {
            'volatility_index': float(data_dict.get('Volatility_Index', 0)),
            'financial_stress_index': float(data_dict.get('Financial_Stress_Index', 0)),
            'yield_curve_spread': float(data_dict.get('Yield_Curve_Spread', 0)),
            'high_yield_spread': float(data_dict.get('High_Yield_Spread', 0))
        }
    }
    return doc

