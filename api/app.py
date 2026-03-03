"""
Flask API for Time Series Market Data
Implements CRUD operations for SQL and MongoDB databases.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config.settings as settings
from utils.database import (
    get_mysql_connection, execute_sql_query, 
    get_mongo_collection, get_mongo_db
)
from utils.preprocessing import (
    preprocess_data, extract_features, 
    format_market_data_for_db, format_mongodb_doc
)

app = Flask(__name__)
CORS(app)

# Load trained model
model = None


def load_model():
    """Load the trained model."""
    global model
    try:
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            settings.MODEL_PATH
        )
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model not found at {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")


load_model()


# ==================== Root Endpoint ====================

@app.route('/')
def index():
    """API root endpoint."""
    return jsonify({
        'name': settings.API_TITLE,
        'version': settings.API_VERSION,
        'description': settings.API_DESCRIPTION,
        'endpoints': {
            'sql': {
                'create': 'POST /api/sql/market-data',
                'read_all': 'GET /api/sql/market-data',
                'read_latest': 'GET /api/sql/market-data/latest',
                'read_date_range': 'GET /api/sql/market-data/range',
                'update': 'PUT /api/sql/market-data/<date>',
                'delete': 'DELETE /api/sql/market-data/<date>'
            },
            'mongodb': {
                'create': 'POST /api/mongo/market-data',
                'read_all': 'GET /api/mongo/market-data',
                'read_latest': 'GET /api/mongo/market-data/latest',
                'read_date_range': 'GET /api/mongo/market-data/range',
                'update': 'PUT /api/mongo/market-data/<date>',
                'delete': 'DELETE /api/mongo/market-data/<date>'
            },
            'prediction': 'POST /api/predict'
        }
    })


# ==================== SQL Endpoints ====================

@app.route('/api/sql/market-data', methods=['POST'])
def sql_create():
    """Create a new market data record in SQL database."""
    data = request.get_json()
    
    if not data or 'date' not in data:
        return jsonify({'error': 'Date is required'}), 400
    
    formatted_data = format_market_data_for_db(data)
    
    query = """
        INSERT INTO market_data (
            date, equities_us, equities_tech, equities_emerging,
            bonds_longterm, gold, oil, volatility_index, crypto_bitcoin,
            yield_curve_spread, high_yield_spread, financial_stress_index
        ) VALUES (
            %(date)s, %(equities_us)s, %(equities_tech)s, %(equities_emerging)s,
            %(bonds_longterm)s, %(gold)s, %(oil)s, %(volatility_index)s, %(crypto_bitcoin)s,
            %(yield_curve_spread)s, %(high_yield_spread)s, %(financial_stress_index)s
        )
    """
    
    result = execute_sql_query(query, formatted_data, fetch=False)
    
    if result is not None:
        return jsonify({'message': 'Record created successfully', 'date': formatted_data['date']}), 201
    else:
        return jsonify({'error': 'Failed to create record'}), 500


@app.route('/api/sql/market-data', methods=['GET'])
def sql_read_all():
    """Read all market data records from SQL database."""
    query = "SELECT * FROM market_data ORDER BY date DESC LIMIT 100"
    results = execute_sql_query(query)
    
    if results is not None:
        return jsonify(results), 200
    else:
        return jsonify({'error': 'Failed to fetch records'}), 500


@app.route('/api/sql/market-data/latest', methods=['GET'])
def sql_read_latest():
    """Read the latest market data record from SQL database."""
    query = """
        SELECT date, equities_us, equities_tech, gold, oil, 
               volatility_index, financial_stress_index
        FROM market_data 
        ORDER BY date DESC 
        LIMIT 1
    """
    results = execute_sql_query(query)
    
    if results is not None and len(results) > 0:
        return jsonify(results[0]), 200
    else:
        return jsonify({'error': 'No records found'}), 404


@app.route('/api/sql/market-data/range', methods=['GET'])
def sql_read_range():
    """Read market data by date range from SQL database."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date are required'}), 400
    
    query = """
        SELECT date, equities_us, volatility_index, financial_stress_index
        FROM market_data
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY date ASC
    """
    
    results = execute_sql_query(query, {'start_date': start_date, 'end_date': end_date})
    
    if results is not None:
        return jsonify(results), 200
    else:
        return jsonify({'error': 'Failed to fetch records'}), 500


@app.route('/api/sql/market-data/<date>', methods=['PUT'])
def sql_update(date):
    """Update a market data record in SQL database."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    formatted_data = format_market_data_for_db(data)
    formatted_data['date'] = date
    
    query = """
        UPDATE market_data SET
            equities_us = %(equities_us)s,
            equities_tech = %(equities_tech)s,
            equities_emerging = %(equities_emerging)s,
            bonds_longterm = %(bonds_longterm)s,
            gold = %(gold)s,
            oil = %(oil)s,
            volatility_index = %(volatility_index)s,
            crypto_bitcoin = %(crypto_bitcoin)s,
            yield_curve_spread = %(yield_curve_spread)s,
            high_yield_spread = %(high_yield_spread)s,
            financial_stress_index = %(financial_stress_index)s
        WHERE date = %(date)s
    """
    
    result = execute_sql_query(query, formatted_data, fetch=False)
    
    if result is not None:
        return jsonify({'message': 'Record updated successfully', 'date': date}), 200
    else:
        return jsonify({'error': 'Failed to update record'}), 500


@app.route('/api/sql/market-data/<date>', methods=['DELETE'])
def sql_delete(date):
    """Delete a market data record from SQL database."""
    query = "DELETE FROM market_data WHERE date = %(date)s"
    
    result = execute_sql_query(query, {'date': date}, fetch=False)
    
    if result is not None:
        return jsonify({'message': 'Record deleted successfully', 'date': date}), 200
    else:
        return jsonify({'error': 'Failed to delete record'}), 500


# ==================== MongoDB Endpoints ====================

@app.route('/api/mongo/market-data', methods=['POST'])
def mongo_create():
    """Create a new market data document in MongoDB."""
    data = request.get_json()
    
    if not data or 'date' not in data:
        return jsonify({'error': 'Date is required'}), 400
    
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    doc = format_mongodb_doc(data)
    
    try:
        # Use upsert to handle both create and update
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': doc},
            upsert=True
        )
        return jsonify({'message': 'Document created successfully', 'date': doc['_id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mongo/market-data', methods=['GET'])
def mongo_read_all():
    """Read all market data documents from MongoDB."""
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    try:
        results = list(collection.find().sort('date', -1).limit(100))
        # Convert ObjectId to string
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mongo/market-data/latest', methods=['GET'])
def mongo_read_latest():
    """Read the latest market data document from MongoDB."""
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    try:
        result = collection.find_one(sort=[('date', -1)])
        if result:
            result['_id'] = str(result['_id'])
            return jsonify(result), 200
        else:
            return jsonify({'error': 'No documents found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mongo/market-data/range', methods=['GET'])
def mongo_read_range():
    """Read market data by date range from MongoDB."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date are required'}), 400
    
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    try:
        query = {
            'date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        results = list(collection.find(query).sort('date', 1))
        
        # Convert ObjectId to string
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mongo/market-data/<date>', methods=['PUT'])
def mongo_update(date):
    """Update a market data document in MongoDB."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    doc = format_mongodb_doc(data)
    doc['_id'] = date
    
    try:
        collection.update_one(
            {'_id': date},
            {'$set': doc},
            upsert=True
        )
        return jsonify({'message': 'Document updated successfully', 'date': date}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mongo/market-data/<date>', methods=['DELETE'])
def mongo_delete(date):
    """Delete a market data document from MongoDB."""
    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'error': 'MongoDB connection failed'}), 500
    
    try:
        result = collection.delete_one({'_id': date})
        if result.deleted_count > 0:
            return jsonify({'message': 'Document deleted successfully', 'date': date}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Prediction Endpoint ====================

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make a prediction using the trained model."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        import pandas as pd
        import numpy as np
        
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
        
        # Ensure required columns exist
        required = ['Equities_US', 'Financial_Stress_Index']
        for col in required:
            if col not in df.columns:
                return jsonify({'error': f'Missing required column: {col}'}), 400
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle single-row prediction (no historical data)
        # Create lag features with available data
        equities = df['Equities_US'].iloc[0]
        
        df['lag_1'] = equities  # Use current value as proxy
        df['lag_7'] = equities
        df['ma_7'] = equities
        df['vol_7'] = df['Equities_US'].pct_change().rolling(7).std().iloc[-1] if len(df) > 1 else 0.15
        df['vol_7'] = df['vol_7'] * np.sqrt(252) if pd.notna(df['vol_7'].iloc[-1]) else 0.15
        df['rolling_corr_30'] = 0.0  # Default correlation
        
        # Ensure all feature columns exist
        for col in settings.FEATURES:
            if col not in df.columns:
                df[col] = 0.0
        
        # Fill any NaN values
        df = df.fillna(0)
        
        # Extract features in the correct order
        features = df[settings.FEATURES].values
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Get prediction direction
        direction = "up" if prediction > 0 else "down"
        
        return jsonify({
            'prediction': float(prediction),
            'direction': direction,
            'input_features': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Health Check ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    # Check SQL connection
    sql_status = 'connected' if get_mysql_connection() else 'disconnected'
    
    # Check MongoDB connection
    try:
        mongo_status = 'connected' if get_mongo_collection() else 'disconnected'
    except:
        mongo_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'sql': sql_status,
        'mongodb': mongo_status,
        'model_loaded': model is not None
    }), 200


if __name__ == '__main__':
    app.run(
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG
    )

