# FRED Python API

A Python API client for fetching economic data from the Federal Reserve Economic Data (FRED) repository maintained by the Federal Reserve Bank of St. Louis.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Requirements](#requirements)

## ✨ Features

- ✅ Fetch economic data by FRED series ID
- ✅ Filter by date range (`start_date`, `end_date`)
- ✅ Filter by specific dates list
- ✅ Automatic forward fill for missing dates with warnings
- ✅ Comprehensive input validation
- ✅ Type hints for better IDE support
- ✅ Detailed logging for debugging
- ✅ Robust error handling
- ✅ Full test coverage

## 🚀 Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/fred_api.git
cd fred_api
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Verify installation
```bash
pytest tests/ -v
```

## 🎯 Quick Start
```python
from src.api import FredAPI

# Initialize the API
api = FredAPI()

# Fetch full series
df = api.get_series("DTB3")
print(df.head())

# Fetch with date range
df = api.get_series("DTB3", start_date="2020-01-01", end_date="2021-12-31")
print(df)

# Fetch specific dates
df = api.get_series("DTB3", dates=["2020-01-01", "2020-06-01", "2020-12-31"])
print(df)
```

## 📚 API Reference

### `FredAPI`

Main class for interacting with the FRED API.

#### `get_series(series_id, dates=None, start_date=None, end_date=None)`

Fetch data for a given FRED series.

**Parameters:**

- `series_id` (str, required): FRED series identifier
  - Example: `"DTB3"`, `"DGS10"`, `"UNRATE"`
  
- `dates` (List[str], optional): List of specific dates to fetch
  - Format: `["YYYY-MM-DD", "YYYY-MM-DD", ...]`
  - Example: `["2020-01-01", "2020-06-01", "2020-12-31"]`
  
- `start_date` (str, optional): Start date for date range
  - Format: `"YYYY-MM-DD"`
  - Example: `"2020-01-01"`
  
- `end_date` (str, optional): End date for date range
  - Format: `"YYYY-MM-DD"`
  - Example: `"2021-12-31"`

**Returns:**

- `pd.DataFrame`: DataFrame with columns:
  - `date` (datetime64[ns]): Date of observation
  - `value` (float64): Value of the economic indicator

**Raises:**

- `ValueError`: Invalid series ID, incorrect date format, or logical errors
- `TypeError`: Incorrect parameter types
- `ConnectionError`: Network or FRED connection issues

**Notes:**

- Either use `dates` OR `start_date`/`end_date`, not both
- If no date parameters provided, returns full series
- Missing dates are forward-filled with a warning
- Dates before series inception raise an error

## 💡 Examples

### Example 1: Fetch 3-Month Treasury Bill (DTB3)
```python
from src.api import FredAPI

api = FredAPI()

# Get full historical data
df = api.get_series("DTB3")
print(f"Total records: {len(df)}")
print(df.head())
```

**Output:**
```
        date  value
0 1954-01-04   1.33
1 1954-01-05   1.28
2 1954-01-06   1.28
3 1954-01-07   1.31
4 1954-01-08   1.31
```

### Example 2: Fetch 10-Year Treasury Yield for Specific Year
```python
api = FredAPI()

# Get data for 2023
df = api.get_series("DGS10", start_date="2023-01-01", end_date="2023-12-31")
print(df.head())
```

### Example 3: Fetch Unemployment Rate for Specific Dates
```python
api = FredAPI()

# Get quarterly data
dates = ["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01"]
df = api.get_series("UNRATE", dates=dates)
print(df)
```

**Output:**
```
        date  value
0 2020-01-01   3.60
1 2020-04-01  14.70
2 2020-07-01  10.20
3 2020-10-01   6.90
```

### Example 4: Fetch Euro Area GDP
```python
api = FredAPI()

# Get quarterly GDP data for 2020-2021
df = api.get_series("CLVMEURSCAB1GQEA19", 
                    start_date="2020-01-01", 
                    end_date="2021-12-31")
print(df)
```

## 🛡️ Error Handling

The API provides specific exceptions for different error scenarios:

### ValueError

Raised for invalid input values or logical errors:
```python
api = FredAPI()

# Empty series ID
try:
    df = api.get_series("")
except ValueError as e:
    print(f"Error: {e}")  # "series_id cannot be empty"

# Invalid date format
try:
    df = api.get_series("DTB3", start_date="01/01/2020")
except ValueError as e:
    print(f"Error: {e}")  # "start_date must be in YYYY-MM-DD format"

# Unknown series
try:
    df = api.get_series("INVALID_SERIES")
except ValueError as e:
    print(f"Error: {e}")  # "Series 'INVALID_SERIES' not found on FRED"

# Conflicting parameters
try:
    df = api.get_series("DTB3", dates=["2020-01-01"], start_date="2020-01-01")
except ValueError as e:
    print(f"Error: {e}")  # "Cannot specify both 'dates' and 'start_date'/'end_date'"
```

### TypeError

Raised for incorrect parameter types:
```python
api = FredAPI()

# series_id must be string
try:
    df = api.get_series(123)
except TypeError as e:
    print(f"Error: {e}")  # "series_id must be a string, got int"
```

### ConnectionError

Raised for network or FRED connection issues:
```python
api = FredAPI()

try:
    df = api.get_series("DTB3")
except ConnectionError as e:
    print(f"Error: {e}")  # Connection-related error message
```

### UserWarning

Warning for missing dates (with automatic forward fill):
```python
import warnings

api = FredAPI()

# Requesting dates that don't exist in the series
with warnings.catch_warnings(record=True) as w:
    df = api.get_series("DTB3", dates=["2020-01-01", "2020-01-02"])
    if w:
        print(f"Warning: {w[-1].message}")
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
# Unit tests
pytest tests/test_api.py -v

# Integration tests
pytest tests/test_integration.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite covers:

- ✅ Fetching full series data (DTB3, DGS2)
- ✅ Date range filtering
- ✅ Specific dates filtering with forward fill
- ✅ Invalid series error handling (XXXX)
- ✅ All ValueError scenarios
- ✅ All TypeError scenarios
- ✅ ConnectionError handling
- ✅ Dates before series inception
- ✅ All-None values check
- ✅ Input validation

## 📁 Project Structure
```
fred_api/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── api.py               # Main FredAPI class
│   ├── fetcher.py           # HTTP requests to FRED
│   ├── processor.py         # Data parsing and processing
│   └── validator.py         # Input validation
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── test_api.py          # Unit tests
│   └── test_integration.py  # Integration tests
├── requirements.txt         # Project dependencies
├── README.md               # This file
└── conftest.py             # Pytest configuration (optional)
```

## 📦 Requirements

- Python 3.8 or higher
- pandas >= 2.0.0
- requests >= 2.31.0
- pytest >= 7.4.0 (for testing)

## 🔍 Popular FRED Series IDs

### Interest Rates
- **DTB3**: 3-Month Treasury Bill
- **DGS2**: 2-Year Treasury Constant Maturity Rate
- **DGS5**: 5-Year Treasury Constant Maturity Rate
- **DGS10**: 10-Year Treasury Constant Maturity Rate
- **DGS30**: 30-Year Treasury Constant Maturity Rate

### Employment
- **UNRATE**: Unemployment Rate
- **PAYEMS**: All Employees, Total Nonfarm
- **CIVPART**: Civilian Labor Force Participation Rate

### GDP & Economic Output
- **GDP**: Gross Domestic Product
- **GDPC1**: Real Gross Domestic Product
- **CLVMEURSCAB1GQEA19**: Euro Area Real GDP

### Inflation
- **CPIAUCSL**: Consumer Price Index for All Urban Consumers
- **PCEPI**: Personal Consumption Expenditures Price Index
- **CPILFESL**: Consumer Price Index for All Urban Consumers: All Items Less Food and Energy

### More series available at: https://fred.stlouisfed.org/

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Data provided by [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/)
- FRED® API documentation: https://fred.stlouisfed.org/docs/api/fred/

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ for economic data analysis**