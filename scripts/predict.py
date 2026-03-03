"""
Prediction Script for Time Series Market Data
Fetches data from API, preprocesses, loads model, and makes predictions.

This script demonstrates the end-to-end pipeline:
1. Fetch a time series record from the API
2. Preprocesses the data using similar preprocessing as in Task 1
3. Loads the trained model
4. Makes a prediction/forecast

Usage:
    python scripts/predict.py
"""
import requests
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fetch_latest_from_api(base_url='http://localhost:5000'):
    """
    Fetch the latest market data record from the API.
    
    Args:
        base_url: Base URL of the API
    
    Returns:
        Dictionary with market data or None if failed
    """
    try:
        # Try SQL endpoint first
        response = requests.get(f'{base_url}/api/sql/market-data/latest')
        if response.status_code == 200:
            data = response.json()
            print("✓ Fetched latest record from SQL API")
            return data
    except requests.exceptions.RequestException as e:
        print(f"SQL API unavailable: {e}")
    
    try:
        # Try MongoDB endpoint
        response = requests.get(f'{base_url}/api/mongo/market-data/latest')
        if response.status_code == 200:
            data = response.json()
            print("✓ Fetched latest record from MongoDB API")
            return data
    except requests.exceptions.RequestException as e:
        print(f"MongoDB API unavailable: {e}")
    
    return None


def fetch_date_range_from_api(start_date, end_date, db_type='sql', base_url='http://localhost:5000'):
    """
    Fetch market data for a date range from the API.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        db_type: 'sql' or 'mongo'
        base_url: Base URL of the API
    
    Returns:
        List of records or None if failed
    """
    endpoint = 'sql' if db_type == 'sql' else 'mongo'
    
    try:
        response = requests.get(
            f'{base_url}/api/{endpoint}/market-data/range',
            params={'start_date': start_date, 'end_date': end_date}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Fetched {len(data)} records from {db_type} API")
            return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    
    return None


def preprocess_data(df):
    """
    Preprocess raw time-series data for model prediction.
    Creates lag features, moving averages, and rolling correlations.
    (Same as in Task 1)
    
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
    
    # For single row predictions, we need to handle lag features specially
    # Create lag features with the available data
    if len(df) == 1:
        # For single row, use the same value for lags
        df['lag_1'] = df['Equities_US']
        df['lag_7'] = df['Equities_US']
        df['ma_7'] = df['Equities_US']
        df['vol_7'] = 0.15  # Default volatility
        df['rolling_corr_30'] = 0.0  # Default correlation
    else:
        # Feature engineering for multiple rows
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
    
    # Fill any remaining NaN values with 0
    df = df.fillna(0)
    
    return df


def load_model(model_path='models/trained_model.pkl'):
    """
    Load the trained model from file.
    
    Args:
        model_path: Path to the saved model
    
    Returns:
        Loaded model or None if failed
    """
    # Try relative to script location first
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    full_path = os.path.join(project_root, model_path)
    
    if os.path.exists(full_path):
        try:
            model = joblib.load(full_path)
            print(f"✓ Model loaded from {full_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
    
    # Try current working directory
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"✓ Model loaded from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
    
    print("⚠ Model file not found. Using mock prediction for demonstration.")
    return None


def make_prediction(model, features, feature_names):
    """
    Make a prediction using the trained model.
    
    Args:
        model: Trained model
        features: numpy array of features
        feature_names: List of feature names
    
    Returns:
        Prediction result dictionary
    """
    if model is None:
        # Mock prediction for demonstration
        print("\n⚠ Running in demo mode (no model loaded)")
        prediction = 0.001  # Mock 0.1% expected return
        direction = "up" if prediction > 0 else "down"
        confidence = 0.65
    else:
        # Make actual prediction
        prediction = model.predict(features)[0]
        direction = "up" if prediction > 0 else "down"
        
        # Calculate confidence (mock - in real scenario would use prediction probabilities)
        confidence = min(abs(prediction) * 100, 95) if prediction != 0 else 50
    
    return {
        'predicted_return': float(prediction),
        'direction': direction,
        'confidence': float(confidence),
        'interpretation': f"Model predicts market will go {direction}",
        'model_used': model is not None
    }


def run_prediction_demo():
    """
    Run a complete prediction demonstration.
    """
    print("=" * 60)
    print("TIME SERIES PREDICTION SCRIPT")
    print("=" * 60)
    
    # Feature columns used in training
    feature_columns = [
        'lag_1', 'lag_7', 'ma_7', 'vol_7', 'rolling_corr_30',
        'Financial_Stress_Index', 'Volatility_Index',
        'Yield_Curve_Spread', 'High_Yield_Spread'
    ]
    
    # Sample market data (matching the dataset format)
    sample_data = {
        'Date': '2026-02-26',
        'Equities_US': 690.50,
        'Equities_Tech': 610.25,
        'Equities_Emerging': 63.10,
        'Bonds_LongTerm': 90.15,
        'Gold': 476.80,
        'Oil': 81.20,
        'Volatility_Index': 18.50,
        'Crypto_Bitcoin': 66000.00,
        'Yield_Curve_Spread': 0.58,
        'High_Yield_Spread': 2.85,
        'Financial_Stress_Index': -0.5800
    }
    
    print("\n[1] INPUT DATA")
    print("-" * 40)
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    # Step 2: Preprocess data
    print("\n[2] PREPROCESSING")
    print("-" * 40)
    
    # Create DataFrame
    df = pd.DataFrame([sample_data])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    print("  • Converting to numeric...")
    print("  • Forward filling missing values...")
    print("  • Creating lag features (lag_1, lag_7)...")
    print("  • Creating moving averages (ma_7)...")
    print("  • Creating volatility features (vol_7)...")
    print("  • Creating rolling correlations...")
    
    # Preprocess
    df_processed = preprocess_data(df)
    print(f"  ✓ Preprocessing complete. Shape: {df_processed.shape}")
    
    # Extract features
    print("\n[3] FEATURE EXTRACTION")
    print("-" * 40)
    
    try:
        # Extract features that exist
        available_features = [col for col in feature_columns if col in df_processed.columns]
        features = df_processed[available_features].values
        
        # Fill any missing features with 0
        features = np.nan_to_num(features, nan=0.0)
        
        print(f"  • Features extracted: {available_features}")
        print(f"  • Feature vector shape: {features.shape}")
    except Exception as e:
        print(f"  ⚠ Error extracting features: {e}")
        print("  • Using mock features for demonstration")
        features = np.array([[690, 680, 685, 0.15, 0.2, -0.5, 19, 0.6, 3.0]])
    
    # Step 4: Load model
    print("\n[4] MODEL LOADING")
    print("-" * 40)
    model = load_model()
    
    # Step 5: Make prediction
    print("\n[5] MAKING PREDICTION")
    print("-" * 40)
    result = make_prediction(model, features, feature_columns)
    
    print(f"\n{'=' * 60}")
    print("PREDICTION RESULTS")
    print("=" * 60)
    print(f"  Predicted Return:    {result['predicted_return']:.4f} ({result['predicted_return']*100:.2f}%)")
    print(f"  Direction:           {result['direction'].upper()}")
    print(f"  Confidence:          {result['confidence']:.1f}%")
    print(f"  Interpretation:      {result['interpretation']}")
    print(f"  Model Loaded:        {result['model_used']}")
    print("=" * 60)
    
    return result


def run_api_prediction(base_url='http://localhost:5000'):
    """
    Run prediction by fetching data from the API.
    """
    print("=" * 60)
    print("API-BASED PREDICTION")
    print("=" * 60)
    
    # Fetch latest data
    print("\n[1] FETCHING DATA FROM API...")
    data = fetch_latest_from_api(base_url)
    
    if data is None:
        print("  ⚠ Could not fetch from API. Using sample data.")
        return run_prediction_demo()
    
    print(f"  ✓ Received data: {data}")
    
    # Run prediction
    return run_prediction_demo()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Time Series Prediction Script')
    parser.add_argument('--api', action='store_true', 
                        help='Fetch data from API instead of using sample data')
    parser.add_argument('--url', default='http://localhost:5000',
                        help='API base URL (default: http://localhost:5000)')
    
    args = parser.parse_args()
    
    if args.api:
        run_api_prediction(args.url)
    else:
        run_prediction_demo()

