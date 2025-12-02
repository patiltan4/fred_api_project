import pandas as pd
import logging
from typing import Optional, List
from fetcher import fetch_fred_data
from processor import parse_fred_csv, check_all_none, filter_by_dates, filter_by_date_range
from validator import validate_series_id, validate_date_parameters

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FredAPI:
    def __init__(self):
        logger.info("FredAPI initialized")
    
    def get_series(self, 
                   series_id: str,
                   dates: Optional[List[str]] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None) -> pd.DataFrame:
        
        logger.info(f"Getting series: {series_id}")
        logger.debug(f"Parameters - dates: {dates}, start_date: {start_date}, end_date: {end_date}")
        
        # Step 1: Validate inputs
        try:
            validate_series_id(series_id)
            validate_date_parameters(dates, start_date, end_date)
        except (TypeError, ValueError) as e:
            logger.error(f"Validation failed: {str(e)}")
            raise
        
        # Step 2: Fetch data from FRED
        try:
            if dates is None:
                csv_data = fetch_fred_data(series_id, start_date, end_date)
            else:
                csv_data = fetch_fred_data(series_id)
        except (ConnectionError, ValueError) as e:
            logger.error(f"Failed to fetch data: {str(e)}")
            raise
        
        # Step 3: Parse CSV data
        try:
            df = parse_fred_csv(csv_data)
        except ValueError as e:
            logger.error(f"Failed to parse data: {str(e)}")
            raise
        
        # Step 4: Check for all None values
        try:
            check_all_none(df)
        except ValueError as e:
            logger.error(f"Data validation failed: {str(e)}")
            raise
        
        # Step 5: Filter by dates if provided
        if dates is not None:
            series_start_date = df['date'].min()
            logger.debug(f"Series starts at: {series_start_date}")
            try:
                df = filter_by_dates(df, dates, series_start_date)
            except ValueError as e:
                logger.error(f"Date filtering failed: {str(e)}")
                raise
        elif start_date is not None or end_date is not None:
            df = filter_by_date_range(df, start_date, end_date)
        
        logger.info(f"Successfully retrieved {len(df)} rows for series {series_id}")
        
        return df


if __name__ == "__main__":
    api = FredAPI()
    
    print("Test 1: Fetch full series (DTB3)")
    print("="*50)
    try:
        df = api.get_series("DTB3")
        print(f"Retrieved {len(df)} rows")
        print(df.head())
        print(df.tail())
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Test 2: Fetch with date range (CLVMEURSCAB1GQEA19)")
    print("="*50)
    try:
        df = api.get_series("CLVMEURSCAB1GQEA19", start_date="2020-01-01", end_date="2021-12-31")
        print(f"Retrieved {len(df)} rows")
        print(df)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Test 3: Fetch with specific dates (DTB3)")
    print("="*50)
    try:
        df = api.get_series("DTB3", dates=["2020-01-01", "2020-06-01", "2020-12-31"])
        print(f"Retrieved {len(df)} rows")
        print(df)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Test 4: Invalid series (XXXX)")
    print("="*50)
    try:
        df = api.get_series("XXXX")
        print(df)
    except Exception as e:
        print(f"✓ Expected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Test 5: Conflicting parameters")
    print("="*50)
    try:
        df = api.get_series("DTB3", dates=["2020-01-01"], start_date="2020-01-01")
    except Exception as e:
        print(f"✓ Expected error: {e}")