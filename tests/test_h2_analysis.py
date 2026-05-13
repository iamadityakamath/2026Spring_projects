import pytest
import numpy as np
import pandas as pd
from Analysis.h2_analysis import cohens_d


# ── Test 1: cohens_d ──────────────────────────────────────────────

def test_cohens_d_negative_when_group1_lower():
    group1 = pd.Series([1, 2, 3])
    group2 = pd.Series([4, 5, 6])
    result = cohens_d(group1, group2)
    assert result < 0


def test_cohens_d_positive_when_group1_higher():
    group1 = pd.Series([4, 5, 6])
    group2 = pd.Series([1, 2, 3])
    result = cohens_d(group1, group2)
    assert result > 0


def test_cohens_d_symmetric():
    group1 = pd.Series([1, 2, 3])
    group2 = pd.Series([4, 5, 6])
    assert float(round(cohens_d(group1, group2), 4)) == float(round(-cohens_d(group2, group1), 4))


def test_cohens_d_returns_float():
    group1 = pd.Series([1, 2, 3])
    group2 = pd.Series([4, 5, 6])
    assert isinstance(float(cohens_d(group1, group2)), float)


from Analysis.h2_analysis import per_seniority_tests

# ── Test 2: per_seniority_tests ───────────────────────────────────

@pytest.fixture
def sample_h2_df():
    """Create a minimal fake H2 dataframe for testing."""
    return pd.DataFrame({
        'SeniorityBand': (
            ['Junior (0-2 yrs)'] * 20 +
            ['Mid-level (3-7 yrs)'] * 20 +
            ['Senior (8-15 yrs)'] * 20 +
            ['Expert (16+ yrs)'] * 20
        ),
        'AIUser': [1] * 10 + [0] * 10 +   # Junior
                  [1] * 10 + [0] * 10 +   # Mid
                  [1] * 10 + [0] * 10 +   # Senior
                  [1] * 10 + [0] * 10,    # Expert
        'JobSat': (
            [8] * 10 + [6] * 10 +   # Junior: AI=8, non=6
            [8] * 10 + [6] * 10 +   # Mid
            [8] * 10 + [6] * 10 +   # Senior
            [8] * 10 + [6] * 10     # Expert
        )
    })


def test_per_seniority_tests_returns_dataframe(sample_h2_df):
    result = per_seniority_tests(sample_h2_df)
    assert isinstance(result, pd.DataFrame)


def test_per_seniority_tests_has_expected_columns(sample_h2_df):
    result = per_seniority_tests(sample_h2_df)
    assert 'Band' in result.columns
    assert 'Gap' in result.columns
    assert 'sig' in result.columns


def test_per_seniority_tests_gap_is_positive(sample_h2_df):
    result = per_seniority_tests(sample_h2_df)
    assert (result['Gap'] > 0).all()


def test_per_seniority_tests_returns_one_row_per_band(sample_h2_df):
    result = per_seniority_tests(sample_h2_df)
    assert len(result) == 4


from Analysis.h2_analysis import sentiment_correlation

# ── Test 3: sentiment_correlation ────────────────────────────────

@pytest.fixture
def sample_sentiment_df():
    """Fake dataframe with AI sentiment and JobSat columns."""
    return pd.DataFrame({
        'AISent': ['Very favorable'] * 10 +
                  ['Favorable'] * 10 +
                  ['Indifferent'] * 10 +
                  ['Unfavorable'] * 10 +
                  ['Very unfavorable'] * 10,
        'JobSat': [9] * 10 + [7] * 10 + [5] * 10 + [3] * 10 + [1] * 10,
        'AIUser': [1] * 50,
        'SeniorityBand': ['Expert (16+ yrs)'] * 50,
        'year': [2024] * 50
    })


def test_sentiment_correlation_runs_without_error(sample_sentiment_df):
    # Should run without raising any exception
    sentiment_correlation(sample_sentiment_df)


def test_sentiment_correlation_positive_with_aligned_data(sample_sentiment_df, capsys):
    sentiment_correlation(sample_sentiment_df)
    captured = capsys.readouterr()
    assert 'Positive' in captured.out


def test_sentiment_correlation_significant_with_aligned_data(sample_sentiment_df, capsys):
    sentiment_correlation(sample_sentiment_df)
    captured = capsys.readouterr()
    assert 'Yes' in captured.out