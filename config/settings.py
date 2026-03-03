"""
Configuration settings for the Time Series Pipeline API.
Load environment variables from .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application."""
    
    # Flask settings
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # MySQL Database settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'timeseries_db')
    
    # MongoDB settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'timeseries_db')
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'market_timeseries')
    
    # Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/trained_model.pkl')
    FEATURES = [
        'lag_1', 'lag_7', 'ma_7', 'vol_7', 'rolling_corr_30',
        'Financial_Stress_Index', 'Volatility_Index',
        'Yield_Curve_Spread', 'High_Yield_Spread'
    ]
    
    # API settings
    API_VERSION = 'v1'
    API_TITLE = 'Time Series Market Data API'
    API_DESCRIPTION = 'REST API for time-series market data with CRUD operations'


# Flask settings
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# MySQL Database settings
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'timeseries_db')

# MongoDB settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'timeseries_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'market_timeseries')

# Model settings
MODEL_PATH = os.getenv('MODEL_PATH', 'models/trained_model.pkl')
FEATURES = [
    'lag_1', 'lag_7', 'ma_7', 'vol_7', 'rolling_corr_30',
    'Financial_Stress_Index', 'Volatility_Index',
    'Yield_Curve_Spread', 'High_Yield_Spread'
]

# API settings
API_VERSION = 'v1'
API_TITLE = 'Time Series Market Data API'
API_DESCRIPTION = 'REST API for time-series market data with CRUD operations'

