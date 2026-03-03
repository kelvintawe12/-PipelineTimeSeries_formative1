# Time Series Pipeline - Usage Guide

This document provides detailed instructions on how to run each component of the Time Series Pipeline project.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Running the Jupyter Notebook](#running-the-jupyter-notebook)
4. [Running the Prediction Script](#running-the-prediction-script)
5. [Running the API Server](#running-the-api-server)
6. [Database Setup](#database-setup)
7. [Testing the API Endpoints](#testing-the-api-endpoints)
8. [Running Individual Tests](#running-individual-tests)

---

## Prerequisites

### System Requirements
- Python 3.8 or higher
- MySQL (optional, for database features)
- MongoDB (optional, for database features)

### Python Dependencies
All required packages are listed in `requirements.txt`:
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
flask>=2.3.0
flask-cors>=4.0.0
pymongo>=4.5.0
mysql-connector-python>=8.1.0
python-dotenv>=1.0.0
joblib>=1.3.0
requests>=2.31.0
```

---

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kelvintawe12/-PipelineTimeSeries_formative1.git
cd -PipelineTimeSeries_formative1
```

### 2. Create Virtual Environment
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Create Environment Variables
Create a `.env` file in the project root:
```bash
# Copy the example
cp .env.example .env

# Edit .env with the database credentials
```

Example `.env` file:
```env
# Flask Settings
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# MySQL Settings (optional)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=timeseries_db

# MongoDB Settings (optional)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=timeseries_db
MONGODB_COLLECTION=market_timeseries

# Model Settings
MODEL_PATH=models/trained_model.pkl
```

---

## Running the Jupyter Notebook

### Task 1: EDA and Model Training

The notebook contains:
- Data exploration and statistical analysis
- Missing value handling
- Feature engineering (lag features, moving averages)
- Model training and evaluation

**To run:**
```bash
jupyter notebook notebooks/timeseries_analysis.ipynb
```

Or use VS Code:
1. Open `notebooks/timeseries_analysis.ipynb`
2. Click "Run All Cells" or run cells individually

---

## Running the Prediction Script

### Task 4: Prediction Script

The script performs end-to-end prediction:
1. Loads input data (sample or from API)
2. Preprocesses data (creates features)
3. Loads trained model
4. Makes prediction

**To run with sample data:**
```bash
python scripts/predict.py
```

**Expected output:**
```
============================================================
TIME SERIES PREDICTION SCRIPT
============================================================

[1] INPUT DATA
----------------------------------------
  Date: 2026-02-26
  Equities_US: 690.5
  ...

[2] PREPROCESSING
----------------------------------------
  • Converting to numeric...
  • Forward filling missing values...
  ✓ Preprocessing complete. Shape: (1, 17)

[3] FEATURE EXTRACTION
----------------------------------------
  • Features extracted: ['lag_1', 'lag_7', 'ma_7', ...]
  • Feature vector shape: (1, 9)

[4] MODEL LOADING
----------------------------------------
✓ Model loaded from models/trained_model.pkl

[5] MAKING PREDICTION
----------------------------------------

============================================================
PREDICTION RESULTS
============================================================
  Predicted Return:    -0.0472 (-4.72%)
  Direction:           DOWN
  Confidence:          4.7%
  Model Loaded:        True
============================================================
```

**To run with custom data:**
Edit the `sample_data` dictionary in `scripts/predict.py`:
```python
sample_data = {
    'Date': '2026-02-27',
    'Equities_US': 700.0,
    'Equities_Tech': 620.0,
    # ... add more features
}
```

---

## Running the API Server

### Task 3: CRUD Endpoints

The Flask API provides REST endpoints for:
- SQL database operations
- MongoDB database operations
- Making predictions

**To start the server:**
```bash
python api/app.py
```

**Expected output:**
```
Model loaded from models/trained_model.pkl
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**To test the API is running:**
```bash
curl http://localhost:5000/health
```

---

## Database Setup

### MySQL Setup

1. **Create MySQL database** (using Railway, PlanetScale, or local MySQL)

2. **Run the schema:**
```bash
mysql -u <username> -p <database_name> < database/sql/schema.sql
```

3. **Insert sample data:**
```bash
mysql -u <username> -p <database_name> < data/for_db_inserts/sample_market_data.csv
```

Or use the API to insert data:
```bash
curl -X POST http://localhost:5000/api/sql/market-data \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-25",
    "equities_us": 687.35,
    "equities_tech": 607.87,
    "equities_emerging": 62.62,
    "bonds_longterm": 89.90,
    "gold": 474.61,
    "oil": 80.76,
    "volatility_index": 19.55,
    "crypto_bitcoin": 65568.49,
    "yield_curve_spread": 0.61,
    "high_yield_spread": 2.95,
    "financial_stress_index": -0.6208
  }'
```

### MongoDB Setup

1. **Create MongoDB cluster** on MongoDB Atlas

2. **Import sample data:**
```bash
mongoimport --uri "<your_mongodb_uri>" \
  --db timeseries_db \
  --collection market_timeseries \
  --file data/for_db_inserts/sample_market_data.json \
  --jsonArray
```

Or use MongoDB Compass to import the JSON file.

---

## Testing the API Endpoints

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Get Latest Record (SQL)
```bash
curl http://localhost:5000/api/sql/market-data/latest
```

### 3. Get Records by Date Range (SQL)
```bash
curl "http://localhost:5000/api/sql/market-data/range?start_date=2026-02-20&end_date=2026-02-25"
```

### 4. Get All Records (SQL)
```bash
curl http://localhost:5000/api/sql/market-data
```

### 5. Create Record (SQL)
```bash
curl -X POST http://localhost:5000/api/sql/market-data \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-26",
    "equities_us": 690.5,
    "financial_stress_index": -0.58
  }'
```

### 6. Update Record (SQL)
```bash
curl -X PUT http://localhost:5000/api/sql/market-data/2026-02-26 \
  -H "Content-Type: application/json" \
  -d '{
    "equities_us": 695.0
  }'
```

### 7. Delete Record (SQL)
```bash
curl -X DELETE http://localhost:5000/api/sql/market-data/2026-02-26
```

### 8. MongoDB Endpoints (same as SQL but with `/api/mongo/` prefix)
```bash
# Get latest
curl http://localhost:5000/api/mongo/market-data/latest

# Get by date range
curl "http://localhost:5000/api/mongo/market-data/range?start_date=2026-02-20&end_date=2026-02-25"
```

### 9. Make Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Equities_US": 690.5,
    "Equities_Tech": 610.25,
    "Financial_Stress_Index": -0.58,
    "Volatility_Index": 18.5,
    "Yield_Curve_Spread": 0.58,
    "High_Yield_Spread": 2.85
  }'
```

---

## Running Individual Tests

### Test All Imports
```bash
python -c "
from config.settings import Config
from utils.preprocessing import preprocess_data, create_features
from utils.database import get_sql_connection, get_mongo_client
print('All imports successful!')
"
```

### Test Model Loading
```bash
python -c "
import joblib
model = joblib.load('models/trained_model.pkl')
print(f'Model type: {type(model).__name__}')
"
```

### Test Preprocessing
```bash
python -c "
import pandas as pd
from utils.preprocessing import create_features

data = {
    'Date': ['2026-02-25', '2026-02-24', '2026-02-23'],
    'Equities_US': [687.35, 682.39, 680.50],
    'Financial_Stress_Index': [-0.6208, -0.6180, -0.6150],
    'Volatility_Index': [19.55, 21.01, 20.50]
}
df = pd.DataFrame(data).set_index('Date')
features = create_features(df)
print(f'Features shape: {features.shape}')
print(f'Feature columns: {list(features.columns)}')
"
```

### Test Full Pipeline
```bash
python scripts/predict.py
```

---

## Troubleshooting

### Import Errors
If you encounter import errors, ensure:
1. Virtual environment is activated: `source venv/bin/activate`
2. All dependencies are installed: `pip install -r requirements.txt`

### Database Connection Errors
1. Check `.env` file has correct credentials
2. Verify MySQL/MongoDB servers are running
3. For cloud databases, check network access settings

### Model Not Found Error
Ensure `models/trained_model.pkl` exists. If not, run the notebook to train and save the model.

### Port Already in Use
If port 5000 is in use, change the port in `.env`:
```
FLASK_PORT=5001
```

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/sql/market-data` | Create SQL record |
| GET | `/api/sql/market-data` | Get all SQL records |
| GET | `/api/sql/market-data/latest` | Get latest SQL record |
| GET | `/api/sql/market-data/range` | Get SQL records by date range |
| PUT | `/api/sql/market-data/<date>` | Update SQL record |
| DELETE | `/api/sql/market-data/<date>` | Delete SQL record |
| POST | `/api/mongo/market-data` | Create MongoDB document |
| GET | `/api/mongo/market-data` | Get all MongoDB documents |
| GET | `/api/mongo/market-data/latest` | Get latest MongoDB document |
| GET | `/api/mongo/market-data/range` | Get MongoDB documents by date range |
| PUT | `/api/mongo/market-data/<date>` | Update MongoDB document |
| DELETE | `/api/mongo/market-data/<date>` | Delete MongoDB document |
| POST | `/api/predict` | Make prediction |

---

## Additional Resources

- **Dataset**: [Kaggle - Global Market Stress and Liquidity Regimes](https://www.kaggle.com/datasets/kanchana1990/algorithmic-trading-macro-stress-and-asset-regimes)
- **Flask Documentation**: https://flask.palletsprojects.com/
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
- **MySQL**: https://www.mysql.com/

