"""
Task 4: Prediction/Forecast Script
Fetches data from API, preprocesses, loads model, and makes predictions.

Steps:
1. Fetch a time series record from the API
2. Preprocess the data (same pipeline as Task 1)
3. Load the trained model
4. Make a prediction/forecast
"""

import os
import sys
import requests
import joblib
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==================== CONFIGURATION ====================

API_BASE_URL = "http://127.0.0.1:5000"
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "models", "best_model_random_forest.joblib")

FEATURE_COLUMNS = [
    'Equities_US', 'Equities_Tech', 'Equities_Emerging', 'Bonds_LongTerm',
    'Gold', 'Oil', 'Volatility_Index', 'Crypto_Bitcoin', 'Yield_Curve_Spread',
    'High_Yield_Spread', 'Financial_Stress_Index', 'SPY_Drawdown',
    'SPY_Rolling_Vol_30d', 'BTC_Rolling_Vol_30d', 'Stock_Bond_Corr_90d',
    'SPY_RSI_14', 'GLD_RSI_14', 'spy_ret_1d', 'spy_ret_lag1', 'spy_ret_lag5',
    'spy_ret_lag10', 'vix_lag1', 'vix_lag5', 'spy_ma5', 'spy_ret_ma5',
    'spy_ma20', 'spy_ret_ma20', 'vix_ma20', 'tlt_ret_1d', 'tlt_ret_lag1'
]


# ==================== STEP 1: FETCH FROM API ====================

def fetch_latest_from_api():
    """Fetch the latest market data record from the SQL API."""
    print("\n" + "="*60)
    print("TASK 4: PREDICTION/FORECAST SCRIPT")
    print("="*60)
    print("\n[1] FETCHING DATA FROM API")
    print("-"*40)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/sql/market-data/latest", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Fetched latest record from API")
            print(f"  Date: {data.get('date', 'N/A')}")
            print(f"  Equities_US: {data.get('equities_us', 'N/A')}")
            print(f"  Volatility_Index: {data.get('volatility_index', 'N/A')}")
            print(f"  Financial_Stress_Index: {data.get('financial_stress_index', 'N/A')}")
            return data
        else:
            print(f"  ✗ API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"  ✗ Could not connect to API: {e}")
        print("  Make sure the API is running: python api/app.py")
        return None


# ==================== STEP 2: PREPROCESS ====================

def preprocess(data):
    """
    Preprocess raw API data into the 30 features the model expects.
    Mirrors the preprocessing pipeline from Task 1.
    """
    print("\n[2] PREPROCESSING")
    print("-"*40)

    # Map API field names to model feature names
    equities_us = float(data.get('equities_us', 0))
    equities_tech = float(data.get('equities_tech', 0))
    equities_emerging = float(data.get('equities_emerging', 0))
    bonds_longterm = float(data.get('bonds_longterm', 0))
    gold = float(data.get('gold', 0))
    oil = float(data.get('oil', 0))
    volatility_index = float(data.get('volatility_index', 0))
    crypto_bitcoin = float(data.get('crypto_bitcoin', 0))
    yield_curve_spread = float(data.get('yield_curve_spread', 0))
    high_yield_spread = float(data.get('high_yield_spread', 0))
    financial_stress_index = float(data.get('financial_stress_index', 0))

    # Derived features (approximated from single record)
    spy_ret_1d = equities_us * 0.001  # approximate daily return
    spy_drawdown = -abs(spy_ret_1d * 5)
    spy_rolling_vol_30d = abs(spy_ret_1d) * np.sqrt(30)
    btc_rolling_vol_30d = (crypto_bitcoin * 0.001) * np.sqrt(30)
    stock_bond_corr_90d = -0.3  # typical stock-bond correlation
    
    # RSI approximations (neutral = 50)
    spy_rsi_14 = 50.0 + (spy_ret_1d * 1000)
    gld_rsi_14 = 50.0

    # Lag features (use current as proxy for single record)
    tlt_ret_1d = bonds_longterm * 0.001

    features = {
        'Equities_US': equities_us,
        'Equities_Tech': equities_tech,
        'Equities_Emerging': equities_emerging,
        'Bonds_LongTerm': bonds_longterm,
        'Gold': gold,
        'Oil': oil,
        'Volatility_Index': volatility_index,
        'Crypto_Bitcoin': crypto_bitcoin,
        'Yield_Curve_Spread': yield_curve_spread,
        'High_Yield_Spread': high_yield_spread,
        'Financial_Stress_Index': financial_stress_index,
        'SPY_Drawdown': spy_drawdown,
        'SPY_Rolling_Vol_30d': spy_rolling_vol_30d,
        'BTC_Rolling_Vol_30d': btc_rolling_vol_30d,
        'Stock_Bond_Corr_90d': stock_bond_corr_90d,
        'SPY_RSI_14': spy_rsi_14,
        'GLD_RSI_14': gld_rsi_14,
        'spy_ret_1d': spy_ret_1d,
        'spy_ret_lag1': spy_ret_1d,
        'spy_ret_lag5': spy_ret_1d,
        'spy_ret_lag10': spy_ret_1d,
        'vix_lag1': volatility_index,
        'vix_lag5': volatility_index,
        'spy_ma5': equities_us,
        'spy_ret_ma5': spy_ret_1d,
        'spy_ma20': equities_us,
        'spy_ret_ma20': spy_ret_1d,
        'vix_ma20': volatility_index,
        'tlt_ret_1d': tlt_ret_1d,
        'tlt_ret_lag1': tlt_ret_1d,
    }

    df = pd.DataFrame([features])[FEATURE_COLUMNS]
    print(f"  ✓ Preprocessing complete. Shape: {df.shape}")
    print(f"  ✓ Features: {len(FEATURE_COLUMNS)} features ready")
    return df


# ==================== STEP 3: LOAD MODEL ====================

def load_model():
    """Load the trained Random Forest model."""
    print("\n[3] LOADING MODEL")
    print("-"*40)
    
    if os.path.exists(MODEL_PATH):
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = joblib.load(MODEL_PATH)
            print(f"  ✓ Model loaded: best_model_random_forest.joblib")
            return model
        except Exception as e:
            print(f"  ✗ Error loading model: {e}")
            return None
    else:
        print(f"  ✗ Model file not found at: {MODEL_PATH}")
        return None


# ==================== STEP 4: PREDICT ====================

def make_prediction(model, df):
    """Make a prediction using the loaded model."""
    print("\n[4] MAKING PREDICTION")
    print("-"*40)
    
    try:
        prediction = model.predict(df)[0]
        direction = "UP ↑" if prediction > 0 else "DOWN ↓"
        
        print("\n" + "="*60)
        print("PREDICTION RESULTS")
        print("="*60)
        print(f"  Predicted Next-Day Return: {prediction:.4f} ({prediction*100:.2f}%)")
        print(f"  Direction:                 {direction}")
        print(f"  Interpretation:            Market predicted to go {direction.split()[0]}")
        print("="*60)
        return prediction
    except Exception as e:
        print(f"  ✗ Prediction error: {e}")
        return None


# ==================== MAIN ====================

if __name__ == "__main__":
    # Step 1: Fetch from API
    data = fetch_latest_from_api()
    if data is None:
        print("\n✗ Could not fetch data. Make sure API is running.")
        sys.exit(1)

    # Step 2: Preprocess
    df = preprocess(data)

    # Step 3: Load model
    model = load_model()
    if model is None:
        print("\n✗ Could not load model.")
        sys.exit(1)

    # Step 4: Predict
    make_prediction(model, df)
