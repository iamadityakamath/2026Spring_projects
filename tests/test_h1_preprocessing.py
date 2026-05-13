import pytest
import numpy as np
import pandas as pd
from Preprocessing.h1_preprocessing import (
    _assign_tier,
    _clean_years_col,
    filter_professional_developers,
    clean_salary,
    engineer_seniority,
    engineer_dev_type,
)


# ── Test 1: _assign_tier ──────────────────────────────────────────

def test_assign_tier_returns_unknown_for_nan():
    assert _assign_tier(np.nan) == 'Unknown'

def test_assign_tier_returns_unknown_for_none():
    assert _assign_tier(None) == 'Unknown'

def test_assign_tier_returns_string():
    assert isinstance(_assign_tier('Brazil'), str)

def test_assign_tier_usa_is_tier1():
    assert _assign_tier('United States of America') == 'Tier1_High'

def test_assign_tier_india_is_tier4():
    assert _assign_tier('India') == 'Tier4_Lower'


# ── Test 2: _clean_years_col ──────────────────────────────────────

def test_clean_years_col_less_than_1_year():
    result = _clean_years_col(pd.Series(['Less than 1 year']))
    assert float(result.iloc[0]) == 0.5

def test_clean_years_col_more_than_50_years():
    result = _clean_years_col(pd.Series(['More than 50 years']))
    assert float(result.iloc[0]) == 51.0

def test_clean_years_col_numeric_string():
    result = _clean_years_col(pd.Series(['5']))
    assert float(result.iloc[0]) == 5.0

def test_clean_years_col_na_returns_nan():
    import math
    result = _clean_years_col(pd.Series(['NA']))
    assert math.isnan(result.iloc[0])