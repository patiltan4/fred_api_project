import pandas as pd
import logging
from typing import List, Optional
import warnings

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_fred_csv(csv_data: str) -> pd.DataFrame:
    logger.info("Parsing CSV data from FRED")
    
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        logger.debug(f"CSV parsed. Shape: {df.shape}, Columns: {df.columns.tolist()}")
        
        if len(df.columns) != 2:
            logger.error(f"Expected 2 columns, got {len(df.columns)}")
            raise ValueError(f"Invalid CSV format: expected 2 columns, got {len(df.columns)}")
        
        df.columns = ['date', 'value']
        
        df['date'] = pd.to_datetime(df['date'])
        logger.debug(f"Date column converted to datetime. Date range: {df['date'].min()} to {df['date'].max()}")
        
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        logger.info(f"Successfully parsed {len(df)} rows")
        logger.debug(f"NaN values in 'value' column: {df['value'].isna().sum()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to parse CSV: {str(e)}")
        raise ValueError(f"Failed to parse FRED data: {str(e)}")


def check_all_none(df: pd.DataFrame) -> None:
    if df['value'].isna().all():
        logger.error("All values in the series are None/NaN")
        raise ValueError("All values from FRED API are None")


def filter_by_dates(df: pd.DataFrame, dates: List[str], series_start_date: pd.Timestamp) -> pd.DataFrame:
    logger.info(f"Filtering by specific dates: {len(dates)} dates requested")
    
    requested_dates = pd.to_datetime(dates)
    logger.debug(f"Requested date range: {requested_dates.min()} to {requested_dates.max()}")
    
    dates_before_inception = requested_dates[requested_dates < series_start_date]
    if len(dates_before_inception) > 0:
        logger.error(f"Dates before series inception: {dates_before_inception.tolist()}")
        raise ValueError(
            f"Requested dates {dates_before_inception.tolist()} are before series inception date {series_start_date}"
        )
    
    result_df = pd.DataFrame({'date': requested_dates})
    result_df = result_df.merge(df, on='date', how='left')
    
    missing_dates = result_df[result_df['value'].isna()]['date'].tolist()
    
    if len(missing_dates) > 0:
        logger.warning(f"Missing data for {len(missing_dates)} dates, forward filling")
        warnings.warn(
            f"Missing data for dates: {missing_dates}. Forward filling from previous values.",
            UserWarning
        )
        
        result_df['value'] = result_df['value'].ffill()
        result_df['value'] = result_df['value'].bfill()
    
    logger.info(f"Filtered to {len(result_df)} dates")
    
    return result_df


def filter_by_date_range(df: pd.DataFrame, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> pd.DataFrame:
    logger.info(f"Filtering by date range: start={start_date}, end={end_date}")
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        df = df[df['date'] >= start_dt]
        logger.debug(f"After start_date filter: {len(df)} rows")
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        df = df[df['date'] <= end_dt]
        logger.debug(f"After end_date filter: {len(df)} rows")
    
    logger.info(f"Date range filter complete: {len(df)} rows remaining")
    
    return df


if __name__ == "__main__":
    sample_csv = """observation_date,CLVMEURSCAB1GQEA19
2021-01-01,2625533.6
2021-04-01,2682855.3
2021-07-01,2729932.7
2021-10-01,2751696.4"""
    
    print("Testing CSV parsing...")
    df = parse_fred_csv(sample_csv)
    print(df)
    print("\n" + "="*50 + "\n")
    
    print("Testing date filtering...")
    filtered = filter_by_dates(df, ['2021-01-01', '2021-05-01', '2021-10-01'], pd.Timestamp('2021-01-01'))
    print(filtered)