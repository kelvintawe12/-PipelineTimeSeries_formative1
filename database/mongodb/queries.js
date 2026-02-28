// MongoDB Queries for Time Series Data
// Author: Michael Kimani

// Query 1: Find latest record
db.market_timeseries.find()
  .sort({ date: -1 })
  .limit(1)

// Expected Result: Document with _id "2026-02-25"


// Query 2: Find records by date range
db.market_timeseries.find({
  date: {
    $gte: ISODate("2026-02-23T00:00:00Z"),
    $lte: ISODate("2026-02-25T00:00:00Z")
  }
}).sort({ date: 1 })

// Expected Result: 2 documents between 2026-02-23 and 2026-02-25


// Query 3: Aggregate average volatility during high stress periods
db.market_timeseries.aggregate([
  {
    $match: {
      "indicators.financial_stress_index": { $lt: -0.5 }
    }
  },
  {
    $group: {
      _id: { $year: "$date" },
      avg_volatility: { $avg: "$indicators.volatility_index" },
      max_stress: { $max: "$indicators.financial_stress_index" },
      count: { $sum: 1 }
    }
  },
  {
    $sort: { _id: -1 }
  }
])

// Expected Result:
// { "_id": 2026, "avg_volatility": 20.04, "max_stress": -0.6208, "count": 2 }
