# Time Series Pipeline - Formative 1

## Project Overview
This project builds an end-to-end machine learning pipeline for time-series data analysis using the **Global Market Stress and Liquidity Regimes** dataset from Kaggle.

## Team Members
- **Kelvin**: Task 1 - EDA, Preprocessing, and Model Training
- **Michael**: Task 2 - Database Design (SQL & MongoDB)
- **Team**: Task 3 - API Development (CRUD Endpoints)
- **Team**: Task 4 - Prediction Script Integration

## Dataset
**Source**: [Kaggle - Global Market Stress and Liquidity Regimes](https://www.kaggle.com/datasets/kanchana1990/algorithmic-trading-macro-stress-and-asset-regimes)

**Description**: Daily financial market data from 2014-2026 including:
- US Equities, Tech Stocks, Emerging Markets
- Bonds, Gold, Oil, Bitcoin
- Volatility Index, Financial Stress Index
- Technical indicators (RSI, rolling volatility, correlations)

## Project Structure
```
├── notebooks/
│   └── timeseries_analysis.ipynb        # Task 1: EDA and modeling
├── database/
│   ├── sql/
│   │   ├── schema.sql                   # SQL database schema (3 tables)
│   │   └── queries.sql                  # SQL query examples
│   └── mongodb/
│       ├── collection_design.json       # MongoDB schema design
│       └── queries.js                   # MongoDB query examples
├── api/
│   └── app.py                           # Flask API application
├── scripts/
│   ├── predict.py                       # Prediction script
│   └── save_model.py                    # Model saving utility
├── models/
│   └── trained_model.pkl                # Saved ML models
├── config/
│   └── settings.py                      # Configuration settings
├── utils/
│   ├── database.py                      # Database utilities
│   └── preprocessing.py                 # Preprocessing utilities
├── data/
│   └── for_db_inserts/                 # Sample data for database
├── docs/
│   └── erd_diagram.md                   # ERD documentation
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Tasks

### Task 1: Time-Series Preprocessing and Exploratory Analysis ✅
- Dataset exploration and statistical analysis
- Time range and frequency analysis
- Missing value handling (forward-fill)
- Feature engineering (lag features, moving averages, rolling correlations)
- Model training (Linear Regression, Random Forest)
- Hyperparameter tuning and experiment comparison
- 5+ analytical questions with visualizations

### Task 2: Database Design (SQL & MongoDB) ✅
- SQL schema with 3 tables (assets, market_data, predictions)
- ERD diagram
- MongoDB collection design with nested structure
- 3+ queries per database

### Task 3: API Development ✅
- CRUD endpoints for both SQL and MongoDB:
  - POST /api/sql/market-data - Create record
  - GET /api/sql/market-data - Read all records
  - GET /api/sql/market-data/latest - Get latest record
  - GET /api/sql/market-data/range - Get records by date range
  - PUT /api/sql/market-data/<date> - Update record
  - DELETE /api/sql/market-data/<date> - Delete record
  - Same endpoints for MongoDB at /api/mongo/
- Prediction endpoint: POST /api/predict

### Task 4: Prediction Script ✅
- Fetch data from API
- Preprocess data
- Load trained model
- Generate predictions
- Full end-to-end pipeline demonstration

## Installation

### Prerequisites
```bash
# Python 3.8+
python --version

# MySQL (optional for local testing)
brew install mysql

# MongoDB (optional for local testing)
brew install mongodb-community
```

### Setup
```bash
# Clone the repository
git clone https://github.com/kelvintawe12/-PipelineTimeSeries_formative1.git
cd -PipelineTimeSeries_formative1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running Notebooks
```bash
jupyter notebook notebooks/timeseries_analysis.ipynb
```

### Running API Server
```bash
python api/app.py
```

### Making Predictions
```bash
# Run prediction with sample data
python scripts/predict.py

# Run prediction with API data
python scripts/predict.py --api
```

## API Endpoints

### Root
- `GET /` - API information

### SQL Database
- `POST /api/sql/market-data` - Create record
- `GET /api/sql/market-data` - Get all records
- `GET /api/sql/market-data/latest` - Get latest record
- `GET /api/sql/market-data/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` - Get by date range
- `PUT /api/sql/market-data/<date>` - Update record
- `DELETE /api/sql/market-data/<date>` - Delete record

### MongoDB Database
- `POST /api/mongo/market-data` - Create document
- `GET /api/mongo/market-data` - Get all documents
- `GET /api/mongo/market-data/latest` - Get latest document
- `GET /api/mongo/market-data/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` - Get by date range
- `PUT /api/mongo/market-data/<date>` - Update document
- `DELETE /api/mongo/market-data/<date>` - Delete document

### Prediction
- `POST /api/predict` - Make prediction with input data

### Health Check
- `GET /health` - Check API and database connections

## Database Setup

### MySQL
1. Create a free database on [Railway](https://railway.app) or [PlanetScale](https://planetscale.com)
2. Update connection credentials in `.env` file (copy from `.env.example`)
3. Run schema: `mysql -u <user> -p < database/sql/schema.sql`

### MongoDB
1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Update connection string in `.env` file
3. Import sample data:
   ```bash
   mongoimport --uri <your_uri> --db timeseries_db --collection market_timeseries --file data/for_db_inserts/sample_market_data.json --jsonArray
   ```

## Model Features

The trained model uses the following features:
- `lag_1` - Previous day's equity value
- `lag_7` - Equity value from 7 days ago
- `ma_7` - 7-day moving average
- `vol_7` - 7-day volatility (annualized)
- `rolling_corr_30` - 30-day rolling correlation with financial stress
- `Financial_Stress_Index`
- `Volatility_Index`
- `Yield_Curve_Spread`
- `High_Yield_Spread`

## Contributing

Each team member should:
1. Create a feature branch: `git checkout -b <name>-<task>`
2. Make changes and commit regularly (minimum 4 commits)
3. Push to GitHub: `git push origin <branch-name>`
4. Create a Pull Request when complete

## License
MIT License - Academic Project

