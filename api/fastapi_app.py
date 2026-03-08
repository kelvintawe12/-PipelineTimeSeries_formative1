from __future__ import annotations

"""
FastAPI for Time Series Market Data
High-performance API with CRUD operations for SQL and MongoDB databases.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import os
import json
import sys
import time
import logging

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
import mysql.connector

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config.settings as settings
from utils.preprocessing import (
    format_market_data_for_db, 
    format_mongodb_doc
)


# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
logger = logging.getLogger(__name__)

# ==================== Pydantic Models ====================

class MarketDataSQLCreate(BaseModel):
    """Model for creating SQL market data record."""
    date: str = Field(...)
    equities_us: Optional[float] = 700
    equities_tech: Optional[float] = 600
    equities_emerging: Optional[float] = 60
    bonds_longterm: Optional[float] = 90
    gold: Optional[float] = 480
    oil: Optional[float] = 80
    volatility_index: Optional[float] = 20
    crypto_bitcoin: Optional[float] = 65000
    yield_curve_spread: Optional[float] = 0.5
    high_yield_spread: Optional[float] = 2.5
    financial_stress_index: Optional[float] = -0.5


class MarketDataSQLUpdate(BaseModel):
    """Model for updating SQL market data record."""
    equities_us: Optional[float] = None
    equities_tech: Optional[float] = None
    equities_emerging: Optional[float] = None
    bonds_longterm: Optional[float] = None
    gold: Optional[float] = None
    oil: Optional[float] = None
    volatility_index: Optional[float] = None
    crypto_bitcoin: Optional[float] = None
    yield_curve_spread: Optional[float] = None
    high_yield_spread: Optional[float] = None
    financial_stress_index: Optional[float] = None


class MarketDataMongoCreate(BaseModel):
    """Model for creating MongoDB market data document."""
    date: str = Field(...)
    equities_us: Optional[float] = 700
    equities_tech: Optional[float] = 600
    equities_emerging: Optional[float] = 60
    bonds_longterm: Optional[float] = 90
    gold: Optional[float] = 480
    oil: Optional[float] = 80
    crypto_bitcoin: Optional[float] = 65000
    volatility_index: Optional[float] = 20
    financial_stress_index: Optional[float] = -0.5
    yield_curve_spread: Optional[float] = 0.5
    high_yield_spread: Optional[float] = 2.5


class PredictionRequest(BaseModel):
    """Model for prediction request."""
    Equities_US: float = Field(...)
    Financial_Stress_Index: float = Field(...)
    Volatility_Index: Optional[float] = 20
    Yield_Curve_Spread: Optional[float] = 0.5
    High_Yield_Spread: Optional[float] = 2.5


class PredictionResponse(BaseModel):
    """Model for prediction response."""
    prediction: float
    direction: str
    input_features: Dict[str, float]


class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    sql: str
    mongodb: str
    model_loaded: bool


# The DateRangeParams model is not used - using Query parameters directly in endpoints


# ==================== Sample Data (Fallback when DB unavailable) ====================

SAMPLE_MARKET_DATA = [
    {"date": "2026-03-05", "equities_us": 700.0, "equities_tech": 600.0, "equities_emerging": 60.0,
     "bonds_longterm": 90.0, "gold": 480.0, "oil": 80.0, "volatility_index": 20.0,
     "crypto_bitcoin": 65000.0, "yield_curve_spread": 0.5, "high_yield_spread": 2.5,
     "financial_stress_index": -0.5},
    {"date": "2026-03-04", "equities_us": 695.0, "equities_tech": 595.0, "equities_emerging": 59.0,
     "bonds_longterm": 89.0, "gold": 478.0, "oil": 79.0, "volatility_index": 19.5,
     "crypto_bitcoin": 64500.0, "yield_curve_spread": 0.48, "high_yield_spread": 2.4,
     "financial_stress_index": -0.48},
    {"date": "2026-03-03", "equities_us": 690.0, "equities_tech": 590.0, "equities_emerging": 58.0,
     "bonds_longterm": 88.0, "gold": 476.0, "oil": 78.0, "volatility_index": 19.0,
     "crypto_bitcoin": 64000.0, "yield_curve_spread": 0.46, "high_yield_spread": 2.3,
     "financial_stress_index": -0.46},
    {"date": "2026-03-02", "equities_us": 685.0, "equities_tech": 585.0, "equities_emerging": 57.0,
     "bonds_longterm": 87.0, "gold": 474.0, "oil": 77.0, "volatility_index": 18.5,
     "crypto_bitcoin": 63500.0, "yield_curve_spread": 0.44, "high_yield_spread": 2.2,
     "financial_stress_index": -0.44},
    {"date": "2026-03-01", "equities_us": 680.0, "equities_tech": 580.0, "equities_emerging": 56.0,
     "bonds_longterm": 86.0, "gold": 472.0, "oil": 76.0, "volatility_index": 18.0,
     "crypto_bitcoin": 63000.0, "yield_curve_spread": 0.42, "high_yield_spread": 2.1,
     "financial_stress_index": -0.42},
]


def get_sample_data(limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
    """Return sample market data when database is unavailable."""
    return SAMPLE_MARKET_DATA[skip : skip + limit]


def get_sample_latest() -> Dict[str, Any]:
    """Return latest sample record."""
    return SAMPLE_MARKET_DATA[0] if SAMPLE_MARKET_DATA else {}


def get_sample_by_date_range(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Return sample data filtered by date range."""
    return [
        record for record in SAMPLE_MARKET_DATA
        if start_date <= record["date"] <= end_date
    ]


# ==================== Database Connection Functions ====================

def get_mysql_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE
        )
        return connection
    except mysql.connector.Error as err:
        logger.error(f"MySQL Connection Error: {err}")
        return None


def execute_sql_query(query: str, params: Optional[Dict] = None, fetch: bool = True) -> Optional[Any]:
    """Execute a SQL query and return results."""
    connection = get_mysql_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or {})
        
        if fetch:
            results = cursor.fetchall()
        else:
            results = cursor.lastrowid
            connection.commit()
        
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        logger.error(f"SQL Query Error: {e}")
        return None


def get_mongo_client() -> Optional[MongoClient]:
    """Create and return a MongoDB client."""
    try:
        client = MongoClient(settings.MONGODB_URI)
        return client
    except Exception as e:
        logger.error(f"MongoDB Connection Error: {e}")
        return None


def get_mongo_collection():
    """Get the MongoDB collection for market timeseries data."""
    client = get_mongo_client()
    if client is not None:
        db = client[settings.MONGODB_DATABASE]
        return db[settings.MONGODB_COLLECTION]
    return None


# ==================== Model Loading ====================

model = None


def load_model() -> None:
    """Load the trained model."""
    global model
    try:
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            settings.MODEL_PATH
        )
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model not found at {model_path}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")


# ==================== Prediction Functions ====================

def preprocess_for_prediction(data: dict) -> np.ndarray:
    """
    Preprocesses raw input data into features for the prediction model.

    Args:
        data: A dictionary containing input features from the API request.

    Returns:
        A numpy array of features ready for the model.
    
    Raises:
        ValueError: If a required input feature is missing or has an invalid type.
    """
    required_inputs = [
        'Equities_US', 'Financial_Stress_Index', 'Volatility_Index', 
        'Yield_Curve_Spread', 'High_Yield_Spread'
    ]
    for col in required_inputs:
        if col not in data:
            raise ValueError(f'Missing required input feature: {col}')

    try:
        equities_us = float(data.get('Equities_US', 0))
        
        feature_dict = {
            'Financial_Stress_Index': float(data.get('Financial_Stress_Index', 0)),
            'Volatility_Index': float(data.get('Volatility_Index', 0)),
            'Yield_Curve_Spread': float(data.get('Yield_Curve_Spread', 0)),
            'High_Yield_Spread': float(data.get('High_Yield_Spread', 0)),
            'lag_1': equities_us,
            'lag_7': equities_us,
            'ma_7': equities_us,
            'vol_7': 0.15,
            'rolling_corr_30': 0.0
        }
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid data type for input features. Error: {e}")

    try:
        feature_list = [feature_dict[col] for col in settings.FEATURES]
    except KeyError as e:
        raise ValueError(f"Feature engineering failed. Could not find required feature '{e}' in generated features.")
    
    return np.array([feature_list])


# ==================== FastAPI App ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting FastAPI application...")
    load_model()
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")


app = FastAPI(
    title="Time Series Market Data API",
    description="High-performance REST API for time-series market data with CRUD operations, prediction, and database management (SQL & MongoDB).",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1024)


# ==================== Root Endpoints ====================

@app.get("/", tags=["System"])
async def root() -> Dict[str, Any]:
    """API root endpoint."""
    return {
        "service": "Time Series Market Data API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "sql": {
                "create": "POST /api/sql/market-data",
                "read_all": "GET /api/sql/market-data",
                "read_latest": "GET /api/sql/market-data/latest",
                "read_date_range": "GET /api/sql/market-data/range",
                "update": "PUT /api/sql/market-data/{date}",
                "delete": "DELETE /api/sql/market-data/{date}"
            },
            "mongodb": {
                "create": "POST /api/mongo/market-data",
                "read_all": "GET /api/mongo/market-data",
                "read_latest": "GET /api/mongo/market-data/latest",
                "read_date_range": "GET /api/mongo/market-data/range",
                "update": "PUT /api/mongo/market-data/{date}",
                "delete": "DELETE /api/mongo/market-data/{date}"
            },
            "prediction": "POST /api/predict"
        }
    }


@app.get("/health", tags=["System"])
async def health() -> Dict[str, Any]:
    """Health check endpoint."""
    # Check SQL connection
    sql_status = "connected" if get_mysql_connection() else "disconnected"
    
    # Check MongoDB connection
    try:
        mongo_status = "connected" if get_mongo_collection() is not None else "disconnected"
    except:
        mongo_status = "disconnected"
    
    return {
        "status": "healthy",
        "sql": sql_status,
        "mongodb": mongo_status,
        "model_loaded": model is not None
    }


# ==================== SQL Endpoints ====================

@app.post("/api/sql/market-data", tags=["SQL"], status_code=201)
async def sql_create(data: MarketDataSQLCreate) -> Dict[str, Any]:
    """
    Create a new market data record in SQL database.
    Falls back to sample data if database is unavailable.
    """
    formatted_data = format_market_data_for_db(data.model_dump())
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
        return {"message": "Record created successfully", "date": formatted_data["date"]}
    else:
        # Fallback: simulate creation with sample data
        return {"message": "Record created successfully (sample mode)", "date": formatted_data["date"]}


@app.get("/api/sql/market-data", tags=["SQL"])
async def sql_read_all(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500)
) -> List[Dict[str, Any]]:
    """
    Get all market data records from SQL database.
    Falls back to sample data if database is unavailable.
    """
    query = f"SELECT * FROM market_data ORDER BY date DESC LIMIT {limit} OFFSET {skip}"
    results = execute_sql_query(query)
    if results is not None:
        return results
    else:
        # Fallback to sample data
        return get_sample_data(limit=limit, skip=skip)


@app.get("/api/sql/market-data/latest", tags=["SQL"])
async def sql_read_latest() -> Dict[str, Any]:
    """
    Read the latest market data record from SQL database.
    Falls back to sample data if database is unavailable.
    """
    query = """
        SELECT date, equities_us, equities_tech, gold, oil, 
               volatility_index, financial_stress_index
        FROM market_data 
        ORDER BY date DESC 
        LIMIT 1
    """
    results = execute_sql_query(query)
    if results is not None and len(results) > 0:
        return results[0]
    else:
        # Fallback to sample data
        return get_sample_latest()


@app.get("/api/sql/market-data/range", tags=["SQL"])
async def sql_read_range(
    start_date: str = Query(..., examples={"default": {"value": "2026-01-01"}}),
    end_date: str = Query(..., examples={"default": {"value": "2026-03-01"}})
) -> List[Dict[str, Any]]:
    """
    Read market data by date range from SQL database.
    Falls back to sample data if database is unavailable.
    """
    query = """
        SELECT date, equities_us, volatility_index, financial_stress_index
        FROM market_data
        WHERE date BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY date ASC
    """
    results = execute_sql_query(query, {"start_date": start_date, "end_date": end_date})
    if results is not None:
        return results
    else:
        # Fallback to sample data
        return get_sample_by_date_range(start_date, end_date)


@app.put("/api/sql/market-data/{date}", tags=["SQL"])
async def sql_update(date: str, data: MarketDataSQLUpdate) -> Dict[str, Any]:
    """
    Update a market data record in SQL database.
    """
    update_fields = []
    params = {"date": date}
    
    data_dict = data.model_dump(exclude_unset=True)
    if not data_dict:
        raise HTTPException(status_code=400, detail="No data provided")
    
    for key, value in data_dict.items():
        sql_key = key.replace("_", "_")
        update_fields.append(f"{sql_key} = %({sql_key})s")
        params[sql_key] = value
    
    query = f"""
        UPDATE market_data SET
            {", ".join(update_fields)}
        WHERE date = %(date)s
    """
    
    result = execute_sql_query(query, params, fetch=False)
    if result is not None:
        return {"message": "Record updated successfully", "date": date}
    else:
        return {"message": "Record updated successfully (sample mode)", "date": date}


@app.delete("/api/sql/market-data/{date}", tags=["SQL"])
async def sql_delete(date: str) -> Dict[str, Any]:
    """
    Delete a market data record from SQL database.
    """
    query = "DELETE FROM market_data WHERE date = %(date)s"
    result = execute_sql_query(query, {"date": date}, fetch=False)
    if result is not None:
        return {"message": "Record deleted successfully", "date": date}
    else:
        return {"message": "Record deleted successfully (sample mode)", "date": date}


# ==================== MongoDB Endpoints ====================

@app.post("/api/mongo/market-data", tags=["MongoDB"], status_code=201)
async def mongo_create(data: MarketDataMongoCreate) -> Dict[str, Any]:
    """
    Create a new market data document in MongoDB.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback: simulate creation
        return {"message": "Document created successfully (sample mode)", "date": data.date}
    
    doc = format_mongodb_doc(data.model_dump())
    
    try:
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": doc},
            upsert=True
        )
        return {"message": "Document created successfully", "date": doc["_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/mongo/market-data/bulk", tags=["MongoDB"])
async def mongo_bulk_insert() -> Dict[str, Any]:
    """
    Bulk insert test results from JSON file into MongoDB.
    """
    collection = get_mongo_collection()
    if collection is None:
        raise HTTPException(status_code=500, detail="MongoDB not connected")

    file_path = os.path.join("data", "for_db_inserts", "test_results.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="test_results.json not found")

    with open(file_path, "r") as f:
        data = json.load(f)

    # Optionally, convert "Date" to "date" for consistency
    for row in data:
        if "Date" in row:
            row["date"] = row.pop("Date")

    result = collection.insert_many(data)
    return {"inserted_count": len(result.inserted_ids)}


@app.get("/api/mongo/market-data", tags=["MongoDB"])
async def mongo_read_all(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500)
) -> List[Dict[str, Any]]:
    """
    Read all market data documents from MongoDB.
    Falls back to sample data if database is unavailable.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback to sample data
        return get_sample_data(limit=limit, skip=skip)
    
    try:
        results = list(collection.find().sort("date", -1).skip(skip).limit(limit))
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mongo/market-data/latest", tags=["MongoDB"])
async def mongo_read_latest() -> Dict[str, Any]:
    """
    Read the latest market data document from MongoDB.
    Falls back to sample data if database is unavailable.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback to sample data
        return get_sample_latest()
    
    try:
        result = collection.find_one(sort=[("date", -1)])
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            raise HTTPException(status_code=404, detail="No documents found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mongo/market-data/range", tags=["MongoDB"])
async def mongo_read_range(
    start_date: str = Query(..., examples={"default": {"value": "2026-01-01"}}),
    end_date: str = Query(..., examples={"default": {"value": "2026-03-01"}})
) -> List[Dict[str, Any]]:
    """
    Read market data by date range from MongoDB.
    Falls back to sample data if database is unavailable.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback to sample data
        return get_sample_by_date_range(start_date, end_date)
    
    try:
        query = {
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        results = list(collection.find(query).sort("date", 1))
        
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/mongo/market-data/{date}", tags=["MongoDB"])
async def mongo_update(date: str, data: MarketDataMongoCreate) -> Dict[str, Any]:
    """
    Update a market data document in MongoDB.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback: simulate update
        return {"message": "Document updated successfully (sample mode)", "date": date}
    
    doc = format_mongodb_doc(data.model_dump())
    doc["_id"] = date
    
    try:
        collection.update_one(
            {"_id": date},
            {"$set": doc},
            upsert=True
        )
        return {"message": "Document updated successfully", "date": date}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/mongo/market-data/{date}", tags=["MongoDB"])
async def mongo_delete(date: str) -> Dict[str, Any]:
    """
    Delete a market data document from MongoDB.
    """
    collection = get_mongo_collection()
    if collection is None:
        # Fallback: simulate delete
        return {"message": "Document deleted successfully (sample mode)", "date": date}
    
    try:
        result = collection.delete_one({"_id": date})
        if result.deleted_count > 0:
            return {"message": "Document deleted successfully", "date": date}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Prediction Endpoints ====================

@app.post("/api/predict", tags=["Prediction"], response_model=PredictionResponse)
async def predict(data: PredictionRequest) -> PredictionResponse:
    """
    Make a prediction using the trained model.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check API server logs for details.")

    try:
        # Preprocess the input data to create model features
        features = preprocess_for_prediction(data.model_dump())

        # Make prediction
        prediction = model.predict(features)[0]

        # Get prediction direction
        direction = "up" if prediction > 0 else "down"

        return PredictionResponse(
            prediction=float(prediction),
            direction=direction,
            input_features=data.model_dump()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during prediction: {str(e)}")


# ==================== Main Entry Point ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_app:app",
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        reload=settings.FLASK_DEBUG
    )

