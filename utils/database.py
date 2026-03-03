"""
Database utilities for SQL (MySQL) and MongoDB connections.
"""
import mysql.connector
from pymongo import MongoClient
import config.settings as settings


# ==================== MySQL/SQL Functions ====================

def get_mysql_connection():
    """
    Create and return a MySQL database connection.
    Returns None if connection fails.
    """
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
        print(f"MySQL Connection Error: {err}")
        return None


def init_mysql_database():
    """
    Initialize MySQL database and tables if they don't exist.
    """
    try:
        # First connect without database to create it
        conn = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}")
        cursor.close()
        conn.close()
        
        # Now connect to the database and create tables
        connection = get_mysql_connection()
        if connection:
            cursor = connection.cursor()
            
            # Create assets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id INT PRIMARY KEY AUTO_INCREMENT,
                    asset_name VARCHAR(100) NOT NULL,
                    asset_type ENUM('equity', 'bond', 'commodity', 'crypto', 'index') NOT NULL,
                    ticker_symbol VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create market_data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
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
                )
            """)
            
            # Create predictions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
                    date DATE NOT NULL,
                    model_name VARCHAR(100) NOT NULL,
                    predicted_value DECIMAL(10, 4),
                    actual_value DECIMAL(10, 4),
                    prediction_error DECIMAL(10, 4),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_model (model_name),
                    INDEX idx_prediction_date (date)
                )
            """)
            
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL database initialized successfully")
            return True
    except Exception as e:
        print(f"Error initializing MySQL database: {e}")
        return False


def execute_sql_query(query, params=None, fetch=True):
    """
    Execute a SQL query and return results.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (True for SELECT)
    
    Returns:
        List of results or affected row count
    """
    connection = get_mysql_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            results = cursor.fetchall()
        else:
            results = cursor.lastrowid
            connection.commit()
        
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        print(f"SQL Query Error: {e}")
        return None


# ==================== MongoDB Functions ====================

def get_mongo_client():
    """
    Create and return a MongoDB client.
    """
    try:
        client = MongoClient(settings.MONGODB_URI)
        return client
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return None


# Aliases for compatibility
get_sql_connection = get_mysql_connection


def get_mongo_db():
    """
    Get the MongoDB database instance.
    """
    client = get_mongo_client()
    if client:
        return client[settings.MONGODB_DATABASE]
    return None


def get_mongo_collection():
    """
    Get the MongoDB collection for market timeseries data.
    """
    db = get_mongo_db()
    if db:
        return db[settings.MONGODB_COLLECTION]
    return None


def init_mongodb_collection():
    """
    Initialize MongoDB collection with sample data and indexes.
    """
    try:
        collection = get_mongo_collection()
        if collection is None:
            print("Failed to connect to MongoDB")
            return False
        
        # Create indexes
        collection.create_index("date")
        collection.create_index([("indicators.financial_stress_index", 1)])
        
        print("MongoDB collection initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        return False


def execute_mongo_query(collection_name, query, projection=None):
    """
    Execute a MongoDB query.
    
    Args:
        collection_name: Name of the collection
        query: MongoDB query dictionary
        projection: Fields to include/exclude (optional)
    
    Returns:
        List of documents
    """
    collection = get_mongo_collection()
    if collection is None:
        return None
    
    try:
        if projection:
            results = list(collection.find(query, projection))
        else:
            results = list(collection.find(query))
        return results
    except Exception as e:
        print(f"MongoDB Query Error: {e}")
        return None

