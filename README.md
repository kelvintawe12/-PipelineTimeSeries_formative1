# Time Series Pipeline - Formative 1

## Project Overview
This project builds an end-to-end machine learning pipeline for time-series data analysis using the **Global Market Stress and Liquidity Regimes** dataset from Kaggle.

## Team Members
- **Member 1 (Kelvin)**: Task 1 - EDA, Preprocessing, and Model Training
- **Member 2 (Michael)**: Task 2 - Database Design (SQL & MongoDB)
- **Member 3**: Task 3 - API Development (CRUD Endpoints)
- **Member 4**: Task 4 - Prediction Script Integration

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
│   └── task1_eda_modeling.ipynb          # Task 1: EDA and modeling
├── database/
│   ├── sql/
│   │   ├── schema.sql                    # SQL database schema
│   │   ├── queries.sql                   # SQL query examples
│   │   └── sample_data.sql               # Sample data inserts
│   ├── mongodb/
│   │   ├── collection_design.json        # MongoDB schema design
│   │   └── queries.js                    # MongoDB query examples
│   └── erd_diagram.png                   # Entity-Relationship Diagram
├── src/
│   └── api/
│       └── app.py                        # Flask/FastAPI application
├── scripts/
│   └── predict.py                        # Prediction script
├── models/
│   └── trained_model.pkl                 # Saved ML models
├── requirements.txt                       # Python dependencies
└── README.md                             # This file
```

## Tasks

### Task 1: Time-Series Preprocessing and Exploratory Analysis ✅
- Dataset exploration and statistical analysis
- Feature engineering (lag features, moving averages)
- Model training (Linear Regression, Random Forest)
- Hyperparameter tuning and experiment comparison

### Task 2: Database Design (SQL & MongoDB) 🚧
- Design normalized SQL schema (3+ tables)
- Create ERD diagram
- Design MongoDB collection structure
- Implement and test queries

### Task 3: API Development 📝
- CRUD endpoints for both SQL and MongoDB
- Time-series specific endpoints (latest record, date range queries)
- REST API using Flask/FastAPI

### Task 4: Prediction Script 📝
- Fetch data from API
- Preprocess data
- Load trained model
- Generate predictions

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
jupyter notebook notebooks/task1_eda_modeling.ipynb
```

### Running API Server
```bash
python src/api/app.py
```

### Making Predictions
```bash
python scripts/predict.py
```

## Database Setup

### MySQL
1. Create a free database on [Railway](https://railway.app) or [PlanetScale](https://planetscale.com)
2. Update connection credentials in `.env` file
3. Run schema: `mysql -u <user> -p < database/sql/schema.sql`

### MongoDB
1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Update connection string in `.env` file
3. Import sample data using MongoDB Compass or CLI

## Contributing

Each team member should:
1. Create a feature branch: `git checkout -b <name>-<task>`
2. Make changes and commit regularly (minimum 4 commits)
3. Push to GitHub: `git push origin <branch-name>`
4. Create a Pull Request when complete

## License
MIT License - Academic Project
