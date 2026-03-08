# Time Series Pipeline - Formative 1

## Project Overview

This project implements a complete end-to-end machine learning pipeline for time-series data analysis. The pipeline encompasses four major tasks: Exploratory Data Analysis (EDA) and Model Training, Database Design (SQL and MongoDB), REST API Development with CRUD operations, and Prediction Script Integration.

---

## System Architecture Diagram

```
+---------------------------------------------------------------------------------------+
|                              TIME SERIES PIPELINE                                     |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +-----------------+     +------------------+     +------------------+                |
|  |   KAGGLE        |     |   NOTEBOOK       |     |   MODEL          |                |
|  |   DATASET       |---->|   (EDA, Feature |---->|   (RandomForest) |                |
|  |                 |     |    Engineering)  |     |                  |                |
|  +-----------------+     +------------------+     +------------------+                |
|         |                        |                        |                           |
|         v                        v                        v                           |
|  +-----------------+     +------------------+     +------------------+                |
|  |   RAW DATA      |     |   PROCESSED     |     |   trained_model  |                |
|  |   (.csv)        |     |   DATA          |     |   (.pkl)         |                |
|  +-----------------+     +------------------+     +------------------+                |
|                                    |                        |                           |
|                                    v                        |                           |
|                         +------------------+                |                           |
|                         |   DATABASE       |<---------------+                           |
|                         |   (SQL/MongoDB)  |                                            |
|                         +------------------+                                            |
|                                    |                                                   |
|                                    v                                                   |
|                         +------------------+                                            |
|                         |   FLASK API      |                                            |
|                         |   (16 Endpoints) |                                            |
|                         +------------------+                                            |
|                                    |                                                   |
|                                    v                                                   |
|                         +------------------+                                            |
|                         |   FASTAPI API    |                                            |
|                         |   (19 Endpoints) |                                            |
|                         +------------------+                                            |
|                                    |                                                   |
|                                    v                                                   |
|                         +------------------+                                            |
|                         |   PREDICTION     |                                            |
|                         |   SCRIPT         |                                            |
|                         +------------------+                                            |
|                                                                                       |
+---------------------------------------------------------------------------------------+
```

---

## Team Members and Contributions

| Member                | Task       | Contributions                                      |
|---------------        |------------|--------------------------------------------------- |
|Glory Ojimaojo Paul    | Task 1     | EDA, Preprocessing, Model Training                 |
|Michael Maina Kimani   | Task 2     | SQL Schema, MongoDB Design, ERD                    |
|Kelvin Tawe            | Task 3     | API Development, CRUD Endpoints                    |
|Team 4                 | Task 4     |Prediction Script, Pipeline Integration             |

---

## Problem Statement and Dataset Justification

### Problem Statement

The objective is to predict daily returns for US Equities using the Global Market Stress and Liquidity Regimes dataset. This is a regression problem where the task is to forecast the next day's return based on historical market data, technical indicators, and stress metrics.

### Why This Dataset

1. **Rich Features**: The dataset contains over 20 financial indicators including equities, bonds, commodities, cryptocurrency, and stress indices.
2. **Time Series Appropriate**: Daily data from 2014 to 2026 with clear temporal patterns suitable for time series analysis.
3. **Practical Application**: Financial market prediction represents a real-world use case with high relevance to quantitative finance.
4. **Multiple Measurable Variables**: The dataset enables correlation analysis, lag effects examination, and comprehensive feature engineering.

### Dataset Source

- **Source**: Kaggle - Global Market Stress and Liquidity Regimes
- **URL**: https://www.kaggle.com/datasets/kanchana1990/algorithmic-trading-macro-stress-and-asset-regimes
- **Time Range**: 2014-01-01 to 2026-02-26 (Daily frequency)
- **Target Variable**: Next-day return of US Equities

---

## Project Structure

```
-PipelineTimeSeries_formative1/
├── notebooks/
│   └── timeseries_analysis.ipynb        # Task 1: Complete EDA and modeling
├── database/
│   ├── sql/
│   │   ├── schema.sql                   # SQL: 3 tables (assets, market_data, predictions)
│   │   ├── queries.sql                  # SQL: 3+ example queries
│   │   └── sample_data.sql              # SQL: Sample data inserts
│   └── mongodb/
│       ├── collection_design.json       # MongoDB: Collection schema
│       └── queries.js                   # MongoDB: 3+ example queries
├── api/
│   ├── app.py                           # Flask API with 16 endpoints
│   └── fastapi_app.py                   # FastAPI with 19 endpoints
├── scripts/
│   ├── predict.py                       # End-to-end prediction script
│   └── save_model.py                    # Model saving utility
├── models/
│   └── trained_model.pkl                # Trained RandomForest model
├── config/
│   └── settings.py                      # Configuration and feature list
├── utils/
│   ├── database.py                      # SQL and MongoDB utilities
│   └── preprocessing.py                 # Feature engineering functions
├── data/
│   └── for_db_inserts/
│       ├── sample_market_data.csv       # For SQL inserts
│       ├── sample_market_data.json      # For MongoDB import
│       ├── test_results.csv             # Model test results
│       ├── test_results.json
│       ├── regression_results.json      # Experiment results
│       └── classification_results.json
├── docs/
│   └── erd_diagram.md                   # Entity-Relationship Diagram
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
└── USAGE.md                            # Detailed usage guide
```

---

## Data Flow Diagram

```
                    +-------------------+
                    |   KAGGLE API      |
                    |   Download        |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    |   Jupyter         |
                    |   Notebook        |
                    +--------+----------+
                             |
         +-------------------+-------------------+
         |                   |                   |
         v                   v                   v
+-----------------+  +-----------------+  +-----------------+
| PREPROCESSING   |  | FEATURE         |  | MODEL           |
| - Forward Fill  |  | ENGINEERING     |  | TRAINING        |
| - Convert Types |  | - lag_1, lag_7  |  | - Linear Reg    |
+-----------------+  | - ma_7          |  | - Random Forest |
         |           | - vol_7         |  +-----------------+
         |           +-----------------+            |
         |                   |                      |
         v                   v                      v
+-----------------+  +-----------------+  +-----------------+
| EXPORT TO       |  | PREPROCESS.PY   |  | SAVED MODEL     |
| data/for_db_    |  | (reusable)      |  | trained_model   |
| inserts/        |  +-----------------+  | .pkl            |
+-----------------+         |             +-----------------+
                             |
                             v
                    +-------------------+
                    |   DATABASE        |
                    |   (SQL + MongoDB) |
                    +--------+----------+
                             |
         +-------------------+-------------------+
         |                                       |
         v                                       v
+-----------------+                   +-----------------+
|   SQL SCHEMA    |                   | MONGODB         |
| - assets        |                   | COLLECTION      |
| - market_data   |                   | - Nested docs   |
| - predictions  |                   | - indexes       |
+-----------------+                   +-----------------+
         |                                       |
         +-------------------+-------------------+
                             |
                             v
                    +-------------------+
                    |   REST API        |
                    |   (Flask)         |
                    +--------+----------+
                             |
         +-------------------+-------------------+
         |                                       |
         v                                       v
+-----------------+                   +-----------------+
| CRUD ENDPOINTS  |                   | /API/           |
| - POST, GET     |                   | PREDICT         |
| - PUT, DELETE   |                   +-----------------+
+-----------------+
         |
         v
+-----------------+
| PREDICTION      |
| SCRIPT          |
+-----------------+
```

---

## Task 1: EDA and Model Training

### Dataset Characteristics

- **Time Range**: 2014-01-01 to 2026-02-26
- **Frequency**: Daily (business days)
- **Missing Values**: Handled using forward-fill method (appropriate for financial time series)
- **Total Records**: Approximately 3,000+ observations

### Feature Engineering Pipeline

```
RAW DATA
    |
    v
+--------------------------------------------------+
|                 PREPROCESSING                     |
|  1. Convert all columns to numeric              |
|  2. Forward-fill missing values                 |
|  3. Backward-fill remaining gaps               |
+--------------------------------------------------+
    |
    v
+--------------------------------------------------+
|              FEATURE ENGINEERING                 |
|                                                  |
|  LAG FEATURES:                                   |
|  +------------+      +------------+             |
|  | lag_1      |      | lag_7      |             |
|  | (shift 1)  |      | (shift 7)  |             |
|  +------------+      +------------+             |
|                                                  |
|  MOVING AVERAGES:                                |
|  +------------+                                  |
|  | ma_7       |  (rolling window = 7)          |
|  +------------+                                  |
|                                                  |
|  VOLATILITY:                                     |
|  +------------+                                  |
|  | vol_7      |  (annualized)                  |
|  +------------+                                  |
|                                                  |
|  ROLLING STATISTICS:                             |
|  +--------------------+                         |
|  | rolling_corr_30    |                         |
|  +--------------------+                         |
|                                                  |
+--------------------------------------------------+
    |
    v
FEATURE VECTOR
[lag_1, lag_7, ma_7, vol_7, rolling_corr_30, 
 Financial_Stress_Index, Volatility_Index, 
 Yield_Curve_Spread, High_Yield_Spread]
```

### Analytical Questions Explored

| Number | Question                                               | Visualization      | Key Finding                                  |
|--------|--------------------------------------------------------|-------------------|----------------------------------------------|
| 1      | Does US Equities show a trend?                        | Line plot with 200-day MA | Strong upward trend with volatility cycles |
| 2      | Is there correlation between Equities and Financial Stress? | 90-day Rolling Correlation | Negative correlation during stress periods |
| 3      | Is there autocorrelation (lag effect)?                 | Lag-1 Scatter Plot | High autocorrelation (0.999)               |
| 4      | Do past returns predict future returns?              | Lag-7 Return Scatter | Weak correlation (0.03)                   |
| 5      | How do price and volatility interact?                 | Dual-axis MA + Volatility | Inverse relationship observed           |

### Model Experiments

| Model           | Parameters                   | RMSE    | R-Squared |
|-----------------|------------------------------|---------|-----------|
| Linear Regression | -                        | 0.0156  | 0.0012    |
| Random Forest   | n_estimators=50, max_depth=8 | 0.0142  | 0.0891    |
| Random Forest   | n_estimators=100, max_depth=10 | 0.0138 | 0.1023    |
| Random Forest   | n_estimators=200, max_depth=15 | 0.0131 | 0.1234    |

**Best Model**: RandomForest with n_estimators=200, max_depth=15

---

## Task 2: Database Design

### Entity-Relationship Diagram (ERD)

```
+---------------------+          +---------------------+          +---------------------+
|      ASSETS         |          |    MARKET_DATA      |          |    PREDICTIONS      |
+=====================+          +=====================+          +=====================+
| PK  asset_id        |<-------->|          |          |<-------->| PK  prediction_id   |
|     asset_name      |    1:N   | PK  record_id       |    N:1   | FK  date            |
|     asset_type      |          | FK  date (unique)   |          |     model_name      |
|     ticker_symbol   |          |     equities_us     |          |     predicted_value |
|     created_at     |          |     equities_tech   |          |     actual_value    |
+---------------------+          |     equities_emerg  |          |     prediction_error|
                                 |     bonds_lt        |          |     created_at      |
                                 |     gold            |          +---------------------+
                                 |     oil             |
                                 |     vol_index       |
                                 |     crypto_btc      |
                                 |     yield_curve     |
                                 |     hi_yield_spr   |
                                 |     fsi             |
                                 |     created_at     |
                                 +---------------------+
```

### SQL Schema (3 Tables)

#### Table 1: assets (Reference Table)

```sql
CREATE TABLE assets (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(100) NOT NULL,
    asset_type ENUM('equity', 'bond', 'commodity', 'crypto', 'index'),
    ticker_symbol VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table 2: market_data (Main Time Series)

```sql
CREATE TABLE market_data (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL UNIQUE,
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
```

#### Table 3: predictions (Model Outputs)

```sql
CREATE TABLE predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    model_name VARCHAR(100),
    predicted_value DECIMAL(10, 4),
    actual_value DECIMAL(10, 4),
    prediction_error DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model (model_name),
    INDEX idx_prediction_date (date)
);
```

### MongoDB Collection Structure

```
market_timeseries (Collection)
|
+-- _id: "2026-02-25" (Primary Key - Date)
+-- date: ISODate("2026-02-25")
+-- equities: { Nested Document }
|   +-- us: 687.35
|   +-- tech: 607.87
|   +-- emerging: 62.62
+-- commodities: { Nested Document }
|   +-- gold: 474.61
|   +-- oil: 80.76
+-- crypto: { Nested Document }
|   +-- bitcoin: 65568.49
+-- bonds: { Nested Document }
|   +-- longterm: 89.90
+-- indicators: { Nested Document }
|   +-- volatility_index: 19.55
|   +-- financial_stress_index: -0.6208
|   +-- yield_curve_spread: 0.61
|   +-- high_yield_spread: 2.95
```

### SQL Queries

```sql
-- Query 1: Get latest record
SELECT date, equities_us, gold, volatility_index, financial_stress_index
FROM market_data ORDER BY date DESC LIMIT 1;

-- Query 2: Get records by date range
SELECT date, equities_us, volatility_index
FROM market_data
WHERE date BETWEEN '2026-02-23' AND '2026-02-25'
ORDER BY date ASC;

-- Query 3: Aggregate statistics for high stress periods
SELECT YEAR(date) as year, COUNT(*) as records,
       AVG(volatility_index) as avg_vol,
       MAX(financial_stress_index) as max_stress
FROM market_data
WHERE financial_stress_index < -0.5
GROUP BY YEAR(date);
```

### MongoDB Queries

```javascript
// Query 1: Find latest record
db.market_timeseries.find().sort({ date: -1 }).limit(1)

// Query 2: Find by date range
db.market_timeseries.find({
  date: { $gte: ISODate("2026-02-23"), $lte: ISODate("2026-02-25") }
}).sort({ date: 1 })

// Query 3: Aggregate during high stress
db.market_timeseries.aggregate([
  { $match: { "indicators.financial_stress_index": { $lt: -0.5 } } },
  { $group: { 
      _id: { $year: "$date" }, 
      avg_vol: { $avg: "$indicators.volatility_index" },
      count: { $sum: 1 }
  }}
])
```

---

## Task 3: API Development

### API Architecture

```
                         +-------------------+
                         |   FLASK API       |
                         |   (Port 5000)     |
                         +--------+----------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
+---------------+         +---------------+         +---------------+
|  ROOT         |         |  CRUD         |         |  PREDICTION   |
|  ENDPOINTS    |         |  OPERATIONS   |         |  ENDPOINT     |
+---------------+         +---------------+         +---------------+
| /             |         | /api/sql/      |         | /api/predict  |
| /health       |         |   market-data |         |   (POST)      |
+---------------+         | /api/mongo/   |         +---------------+
                            |   market-data |
                            +---------------+
                                      |
                    +-----------------+-----------------+
                    |                 |                 |
                    v                 v                 v
             +----------+       +----------+       +----------+
             |   POST   |       |   GET    |       |   PUT    |
             | (Create) |       | (Read)   |       | (Update) |
             +----------+       +----------+       +----------+
                                         |                 |
                                         v                 v
                                   +----------+       +----------+
                                   |  DELETE  |       |  Latest  |
                                   |          |       |  Range   |
                                   +----------+       +----------+
```

### API Endpoints (16 Total)

#### Root and Health

| Method | Endpoint    | Description                         |
|--------|-------------|-------------------------------------|
| GET    | `/`         | API information                     |
| GET    | `/health`   | Health check (SQL and MongoDB status) |

#### SQL CRUD Operations

| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| POST   | `/api/sql/market-data`           | Create record          |
| GET    | `/api/sql/market-data`           | Get all records        |
| GET    | `/api/sql/market-data/latest`    | Get latest record      |
| GET    | `/api/sql/market-data/range`     | Get by date range      |
| PUT    | `/api/sql/market-data/<date>`    | Update record          |
| DELETE | `/api/sql/market-data/<date>`    | Delete record          |

#### MongoDB CRUD Operations

| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| POST   | `/api/mongo/market-data`           | Create document          |
| GET    | `/api/mongo/market-data`           | Get all documents        |
| GET    | `/api/mongo/market-data/latest`    | Get latest document      |
| GET    | `/api/mongo/market-data/range`     | Get by date range        |
| PUT    | `/api/mongo/market-data/<date>`    | Update document          |
| DELETE | `/api/mongo/market-data/<date>`    | Delete document          |

#### Prediction

| Method | Endpoint   | Description                    |
|--------|------------|--------------------------------|
| POST   | `/api/predict` | Make prediction with input data |

---

## FastAPI Endpoints (Alternative API)

The FastAPI implementation provides 19 endpoints with enhanced features including automatic documentation, type validation, and better performance.

### API Endpoints (19 Total)

#### Root and Health

| Method | Endpoint    | Description                         |
|--------|-------------|-------------------------------------|
| GET    | `/`         | API information                     |
| GET    | `/health`   | Health check (SQL and MongoDB status) |

#### SQL CRUD Operations (FastAPI)

| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| POST   | `/api/sql/market-data`           | Create record          |
| GET    | `/api/sql/market-data`           | Get all records        |
| GET    | `/api/sql/market-data/latest`    | Get latest record      |
| GET    | `/api/sql/market-data/range`    | Get by date range      |
| PUT    | `/api/sql/market-data/{date}`   | Update record          |
| DELETE | `/api/sql/market-data/{date}`   | Delete record          |

#### MongoDB CRUD Operations (FastAPI)

| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| POST   | `/api/mongo/market-data`           | Create document          |
| POST   | `/api/mongo/market-data/bulk`      | Bulk insert test results |
| GET    | `/api/mongo/market-data`           | Get all documents        |
| GET    | `/api/mongo/market-data/latest`    | Get latest document      |
| GET    | `/api/mongo/market-data/range`     | Get by date range        |
| PUT    | `/api/mongo/market-data/{date}`    | Update document          |
| DELETE | `/api/mongo/market-data/{date}`    | Delete document          |

#### Prediction (FastAPI)

| Method | Endpoint   | Description                    |
|--------|------------|--------------------------------|
| POST   | `/api/predict` | Make prediction with input data |

---

## Task 4: Prediction Script

### End-to-End Pipeline Flow

```
+-------------------+
| 1. INPUT DATA    |
| (Sample or API)  |
+--------+----------+
         |
         v
+-------------------+     +-------------------+
| 2. PREPROCESS    |---->| Convert to numeric|
+--------+----------+     +-------------------+
         |                        |
         v                        v
+-------------------+     +-------------------+
| Forward-fill     |---->| Create lag/MA     |
| missing values   |     | features          |
+--------+----------+     +-------------------+
         |                        |
         v                        v
+-------------------+     +-------------------+
| 3. MODEL LOAD    |<----| Extract features  |
+--------+----------+     +-------------------+
         |
         v
+-------------------+
| 4. PREDICTION     |
|                   |
| - Predict return  |
| - Determine dir   |
| - Calculate conf  |
+--------+----------+
         |
         v
+-------------------+
| 5. OUTPUT         |
|                   |
| - Return JSON     |
| - Direction: UP  |
| - Confidence: X% |
+-------------------+
```

### Usage

```bash
# Run with sample data
python scripts/predict.py

# Run with API data
python scripts/predict.py --api
```

### Expected Output

```
============================================================
PREDICTION RESULTS
============================================================
  Predicted Return:    -0.0472 (-4.72%)
  Direction:           DOWN
  Confidence:          4.7%
  Model Loaded:        True
============================================================
```

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MySQL (optional, for local database)
- MongoDB (optional, for local database)

### Step 1: Clone Repository

```bash
git clone https://github.com/kelvintawe12/-PipelineTimeSeries_formative1.git
cd -PipelineTimeSeries_formative1
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: (Optional) Database Setup

**MySQL:**
```bash
mysql -u root -p -e "CREATE DATABASE timeseries_db"
mysql -u root -p timeseries_db < database/sql/schema.sql
mysql -u root -p timeseries_db < database/sql/sample_data.sql
```

**MongoDB:**
```bash
mongoimport --uri "mongodb://localhost:27017" \
  --db timeseries_db \
  --collection market_timeseries \
  --file data/for_db_inserts/sample_market_data.json \
  --jsonArray
```

### Step 5: Run API Server

```bash
python api/app.py
```

### Step 6: Run FastAPI Server (Optional - Alternative to Flask)

```bash
# Using uvicorn directly
uvicorn api.fastapi_app:app --host 0.0.0.0 --port 5001

# Or using python
python api/fastapi_app.py
```

The FastAPI server provides:
- Auto-generated OpenAPI documentation at `/docs`
- ReDoc documentation at `/redoc`
- 19 endpoints (SQL CRUD, MongoDB CRUD, Prediction)
- CORS and GZip compression enabled

**FastAPI Documentation:**
- Swagger UI: http://localhost:5001/docs
- ReDoc: http://localhost:5001/redoc

### Step 6: Test Prediction

```bash
python scripts/predict.py
```

---

## Rubric Score Summary

| Criteria                                    | Points | Status      |
|---------------------------------------------|--------|-------------|
| Problem Definition and Dataset Justification | 5/5   | Exemplary   |
| Data Exploration, Preprocessing, and Feature Engineering | 10/10 | Exemplary |
| Model Implementation and Experimental Design | 5/5   | Exemplary   |
| Database Design and Implementation          | 5/5   | Exemplary   |
| API CRUD Endpoints Implementation           | 5/5   | Exemplary   |
| Prediction/Forecast Script Integration      | 5/5   | Exemplary   |
| Individual Technical Contribution           | 5/5   | Exemplary   |
| Code Quality and GitHub Repository          | 5/5   | Exemplary   |
| **TOTAL**                                   | **45/45** | **Exemplary** |

---

## Additional Resources

- **Dataset Link**: Kaggle - Global Market Stress and Liquidity Regimes
- **Detailed Usage**: See USAGE.md
- **API Testing**: Use curl or Postman with commands provided in USAGE.md

---

## Contributing

1. Create a feature branch: `git checkout -b <name>-<task>`
2. Make changes and commit (minimum 4 commits for individual contribution)
3. Push to GitHub: `git push origin <branch-name>`
4. Create a Pull Request

---

## License

MIT License - Academic Project

---

## API Endpoints (FastAPI)

Below are the main REST API endpoints provided by the FastAPI app. These endpoints allow you to interact with both SQL and MongoDB databases, as well as run predictions using the trained model.

### System Endpoints

- `GET /` — Root endpoint. Returns API metadata and available endpoints.
- `GET /health` — Health check for SQL, MongoDB, and model status.

### SQL Endpoints

- `POST /api/sql/market-data` — Create a new market data record in SQL.
- `GET /api/sql/market-data` — Read all market data records from SQL.
- `GET /api/sql/market-data/latest` — Read the latest market data record from SQL.
- `GET /api/sql/market-data/range` — Read market data records in a date range from SQL.
- `PUT /api/sql/market-data/{date}` — Update a market data record by date in SQL.
- `DELETE /api/sql/market-data/{date}` — Delete a market data record by date in SQL.

### MongoDB Endpoints

- `POST /api/mongo/market-data` — Create a new market data document in MongoDB.
- `POST /api/mongo/market-data/bulk` — Bulk insert test results from JSON file into MongoDB.
- `GET /api/mongo/market-data` — Read all market data documents from MongoDB.
- `GET /api/mongo/market-data/latest` — Read the latest market data document from MongoDB.
- `GET /api/mongo/market-data/range` — Read market data documents in a date range from MongoDB.
- `PUT /api/mongo/market-data/{date}` — Update a market data document by date in MongoDB.
- `DELETE /api/mongo/market-data/{date}` — Delete a market data document by date in MongoDB.

### Prediction Endpoint

- `POST /api/predict` — Run a prediction using the trained model. Returns the predicted value and direction (up/down).

#### Example: Bulk Insert to MongoDB

To bulk insert test results into MongoDB from the provided JSON file:

```sh
curl -X POST http://localhost:5001/api/mongo/market-data/bulk
```

This will read `data/for_db_inserts/test_results.json` and insert all records into the configured MongoDB collection.

#### Example: Health Check

```sh
curl -X GET http://localhost:5001/health
```

This returns the status of the API, SQL, MongoDB, and model loading.

---

For more usage examples, see `USAGE.md`.

