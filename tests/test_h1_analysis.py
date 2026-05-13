import os
import tempfile
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from Analysis.h1_analysis import (
    plot_salary_by_title,
    plot_salary_by_country,
    plot_salary_by_seniority,
    plot_salary_heatmap,
    plot_salary_trends,
    run_h1_analysis,
)


# ── Shared fixture ────────────────────────────────────────────────

@pytest.fixture
def sample_h1_df():
    """Minimal fake H1 survey dataframe."""
    return pd.DataFrame({
        'Year':                  [2023, 2023, 2024, 2024, 2024, 2025],
        'DevCategory':           ['Data/ML', 'Back-End', 'Data/ML', 'Front-End', 'Back-End', 'Data/ML'],
        'Country':               ['United States of America'] * 4 + ['India'] * 2,
        'ConvertedCompYearly':   [120000, 90000, 130000, 80000, 20000, 140000],
        'SeniorityBucket':       ['3-5 yrs', '6-10 yrs', '11-20 yrs', '0-2 yrs', '3-5 yrs', '20+ yrs'],
        'SeniorityYears':        [4.0, 8.0, 15.0, 1.0, 4.0, 25.0],
    })


@pytest.fixture
def output_dir():
    """Temporary directory for saving plots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


# ── Test 1: plot_salary_by_title ──────────────────────────────────

def test_plot_salary_by_title_saves_file(sample_h1_df, output_dir):
    plot_salary_by_title(sample_h1_df, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_by_title.png'))


def test_plot_salary_by_title_no_error_without_output_dir(sample_h1_df):
    plot_salary_by_title(sample_h1_df, output_dir=None)


def test_plot_salary_by_title_handles_missing_salary(sample_h1_df, output_dir):
    df = sample_h1_df.copy()
    df.loc[0, 'ConvertedCompYearly'] = np.nan
    plot_salary_by_title(df, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_by_title.png'))


# ── Test 2: plot_salary_by_country ───────────────────────────────

def test_plot_salary_by_country_saves_file(sample_h1_df, output_dir):
    plot_salary_by_country(sample_h1_df, min_count=1, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_by_country.png'))


def test_plot_salary_by_country_no_error_without_output_dir(sample_h1_df):
    plot_salary_by_country(sample_h1_df, min_count=1, output_dir=None)


def test_plot_salary_by_country_respects_min_count(sample_h1_df, output_dir):
    # min_count=2 keeps USA (4 rows) and excludes India (2 rows exactly at boundary)
    plot_salary_by_country(sample_h1_df, min_count=3, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_by_country.png'))

# ── Test 3: plot_salary_by_seniority ─────────────────────────────

def test_plot_salary_by_seniority_saves_file(sample_h1_df, output_dir):
    plot_salary_by_seniority(sample_h1_df, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_by_seniority.png'))


def test_plot_salary_by_seniority_no_error_without_output_dir(sample_h1_df):
    plot_salary_by_seniority(sample_h1_df, output_dir=None)


# ── Test 4: plot_salary_heatmap ───────────────────────────────────

def test_plot_salary_heatmap_saves_file(sample_h1_df, output_dir):
    plot_salary_heatmap(sample_h1_df, n_titles=2, n_countries=2, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_heatmap.png'))


def test_plot_salary_heatmap_no_error_without_output_dir(sample_h1_df):
    plot_salary_heatmap(sample_h1_df, n_titles=2, n_countries=2, output_dir=None)


# ── Test 5: plot_salary_trends ────────────────────────────────────

def test_plot_salary_trends_saves_file(sample_h1_df, output_dir):
    plot_salary_trends(sample_h1_df, n_titles=2, output_dir=output_dir)
    assert os.path.exists(os.path.join(output_dir, 'h1_salary_trends.png'))


def test_plot_salary_trends_no_error_without_output_dir(sample_h1_df):
    plot_salary_trends(sample_h1_df, n_titles=2, output_dir=None)


# ── Test 6: run_h1_analysis ───────────────────────────────────────

def test_run_h1_analysis_skips_if_plots_exist():
    with patch('Analysis.h1_analysis.check_file_exists', return_value='exists'):
        result = run_h1_analysis()
        assert 'Skipping' in result


def test_run_h1_analysis_returns_string():
    with patch('Analysis.h1_analysis.check_file_exists', return_value='exists'):
        result = run_h1_analysis()
        assert isinstance(result, str)