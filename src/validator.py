import logging
from typing import Optional, List
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_series_id(series_id: str) -> None:
    logger.debug(f"Validating series_id: {series_id}")
    
    if not isinstance(series_id, str):
        logger.error(f"series_id must be string, got {type(series_id)}")
        raise TypeError(f"series_id must be a string, got {type(series_id).__name__}")
    
    if not series_id or series_id.strip() == "":
        logger.error("series_id is empty")
        raise ValueError("series_id cannot be empty")
    
    logger.debug("series_id validation passed")


def validate_date_format(date_str: str, param_name: str) -> None:
    logger.debug(f"Validating {param_name}: {date_str}")
    
    if not isinstance(date_str, str):
        logger.error(f"{param_name} must be string, got {type(date_str)}")
        raise TypeError(f"{param_name} must be a string, got {type(date_str).__name__}")
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        logger.debug(f"{param_name} format valid")
    except ValueError:
        logger.error(f"{param_name} has invalid format: {date_str}")
        raise ValueError(f"{param_name} must be in YYYY-MM-DD format, got '{date_str}'")


def validate_dates_list(dates: List[str]) -> None:
    logger.debug(f"Validating dates list with {len(dates)} dates")
    
    if not isinstance(dates, list):
        logger.error(f"dates must be list, got {type(dates)}")
        raise TypeError(f"dates must be a list, got {type(dates).__name__}")
    
    if len(dates) == 0:
        logger.error("dates list is empty")
        raise ValueError("dates list cannot be empty")
    
    for i, date in enumerate(dates):
        try:
            validate_date_format(date, f"dates[{i}]")
        except (TypeError, ValueError) as e:
            logger.error(f"Invalid date at index {i}: {date}")
            raise
    
    logger.debug("dates list validation passed")


def validate_date_parameters(dates: Optional[List[str]] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> None:
    logger.info("Validating date parameters")
    
    # Check for conflicting parameters
    if dates is not None and (start_date is not None or end_date is not None):
        logger.error("Cannot specify both 'dates' and 'start_date/end_date'")
        raise ValueError("Cannot specify both 'dates' list and 'start_date'/'end_date'. Use one or the other.")
    
    # Validate dates list if provided
    if dates is not None:
        validate_dates_list(dates)
    
    # Validate start_date if provided
    if start_date is not None:
        validate_date_format(start_date, "start_date")
    
    # Validate end_date if provided
    if end_date is not None:
        validate_date_format(end_date, "end_date")
    
    # Check logical date ordering
    if start_date is not None and end_date is not None:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start_dt > end_dt:
            logger.error(f"start_date {start_date} is after end_date {end_date}")
            raise ValueError(f"start_date ({start_date}) cannot be after end_date ({end_date})")
    
    logger.info("Date parameters validation passed")


if __name__ == "__main__":
    print("Testing series_id validation...")
    try:
        validate_series_id("DTB3")
        print("✓ Valid series_id passed")
        
        validate_series_id("")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing date format validation...")
    try:
        validate_date_format("2021-01-01", "test_date")
        print("✓ Valid date format passed")
        
        validate_date_format("2021/01/01", "test_date")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing conflicting parameters...")
    try:
        validate_date_parameters(dates=["2021-01-01"], start_date="2021-01-01")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing start_date > end_date...")
    try:
        validate_date_parameters(start_date="2021-12-31", end_date="2021-01-01")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing valid parameters...")
    validate_date_parameters(start_date="2021-01-01", end_date="2021-12-31")
    print("✓ Valid date range passed")
    
    validate_date_parameters(dates=["2021-01-01", "2021-06-01"])
    print("✓ Valid dates list passed")