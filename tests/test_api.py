import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from src.api import FredAPI


def test_fetch_dtb3_full_series():
    api = FredAPI()
    df = api.get_series("DTB3")
    
    assert isinstance(df, pd.DataFrame)
    assert 'date' in df.columns
    assert 'value' in df.columns
    assert len(df) > 0
    assert df['date'].dtype == 'datetime64[ns]'


def test_fetch_dgs2_full_series():
    api = FredAPI()
    df = api.get_series("DGS2")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_invalid_series_xxxx():
    api = FredAPI()
    
    with pytest.raises(ValueError, match="not found"):
        api.get_series("XXXX")


def test_fetch_with_date_range():
    api = FredAPI()
    df = api.get_series("DTB3", start_date="2020-01-01", end_date="2020-12-31")
    
    assert len(df) > 0
    assert df['date'].min() >= pd.Timestamp("2020-01-01")
    assert df['date'].max() <= pd.Timestamp("2020-12-31")


def test_fetch_with_specific_dates():
    api = FredAPI()
    dates_list = ["2020-01-01", "2020-06-01", "2020-12-31"]
    df = api.get_series("DTB3", dates=dates_list)
    
    assert len(df) == 3


def test_conflicting_parameters():
    api = FredAPI()
    
    with pytest.raises(ValueError, match="Cannot specify both"):
        api.get_series("DTB3", dates=["2020-01-01"], start_date="2020-01-01")


def test_invalid_date_format():
    api = FredAPI()
    
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        api.get_series("DTB3", start_date="01/01/2020")


def test_start_date_after_end_date():
    api = FredAPI()
    
    with pytest.raises(ValueError, match="cannot be after"):
        api.get_series("DTB3", start_date="2020-12-31", end_date="2020-01-01")


def test_empty_series_id():
    api = FredAPI()
    
    with pytest.raises(ValueError, match="cannot be empty"):
        api.get_series("")


def test_invalid_series_id_type():
    api = FredAPI()
    
    with pytest.raises(TypeError, match="must be a string"):
        api.get_series(123)