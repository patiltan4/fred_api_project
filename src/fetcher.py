
import requests
import logging
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fetch_fred_data(series_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
  
    logger.info(f"Fetching data for series_id: {series_id}")
    if start_date:
        logger.debug(f"Start date: {start_date}")
    if end_date:
        logger.debug(f"End date: {end_date}")
    
    # Build URL with optional date parameters
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    
    # Add date parameters if provided
    if start_date:
        url += f"&cosd={start_date}"
    if end_date:
        url += f"&coed={end_date}"
    
    logger.debug(f"Request URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        
        # Check if request was successful
        if response.status_code == 404:
            logger.error(f"Series {series_id} not found (404)")
            raise ValueError(f"Series '{series_id}' not found on FRED")
        
        response.raise_for_status()
        
        # Validate that we got CSV data
        if not response.text or len(response.text) < 10:
            logger.error(f"Invalid or empty response for series {series_id}")
            raise ValueError(f"Series '{series_id}' returned no data")
        
        # Check if it's an error page (HTML instead of CSV)
        if response.text.strip().startswith('<!DOCTYPE') or response.text.strip().startswith('<html'):
            logger.error(f"Series {series_id} returned HTML error page")
            raise ValueError(f"Series '{series_id}' not found or invalid")
        
        logger.info(f"Successfully fetched data for {series_id}")
        logger.debug(f"Response length: {len(response.text)} characters")
        logger.debug(f"First 200 chars: {response.text[:200]}")
        
        return response.text
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching {series_id}")
        raise ConnectionError(f"Timeout connecting to FRED for series '{series_id}'")
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        raise ConnectionError(f"Failed to connect to FRED: {str(e)}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise ConnectionError(f"Error fetching data from FRED: {str(e)}")


if __name__ == "__main__":
    # Quick test
    try:
        print("Testing CLVMEURSCAB1GQEA19 (full data)...")
        data = fetch_fred_data("CLVMEURSCAB1GQEA19")
        print(data[:500])
        print("\n" + "="*50 + "\n")
        
        print("Testing CLVMEURSCAB1GQEA19 with date range (2020-2021)...")
        data = fetch_fred_data("CLVMEURSCAB1GQEA19", start_date="2021-01-01", end_date="2021-12-31")
        print(data[:500])
        print("\n" + "="*50 + "\n")
        
        print("Testing invalid series XXXX...")
        data = fetch_fred_data("XXXX")
    except (ValueError, ConnectionError) as e:
        print(f"Expected error: {e}")