import os
import tempfile
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from Analysis.h3_analysis import (
    plot_pooled_salary_by_work_model,
    plot_salary_trends_by_work_model,
    plot_covid_vs_post_comparison,
    plot_salary_distribution_by_era,
    run_regression_analysis,
    run_h3_analysis,
)


# ── Shared fixture ────────────────────────────────────────────────

@pytest.fixture
def sample_h3_df():
    """Minimal fake H3 dataframe."""
    return pd.DataFrame({
        'work_year':      [2020, 2020, 2021, 2022, 2023, 2024] * 3,
        'work_models':    (['Remote'] * 6 + ['On-site'] * 6 + ['Hybrid'] * 6),
        'salary_in_usd':  [100000, 110000, 105000, 115000, 120000, 118000] * 3,
        'experience_level': ['SE', 'MI', 'SE', 'EX', 'MI', 'SE'] * 3,
        'job_title':      ['Data Scientist'] * 18,
    })


@pytest.fixture
def output_dir():
    """Temporary directory for saving plots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


# ── Test 1: plot_pooled_salary_by_work_model ─────────────────────

def test_plot_pooled_saves_file(sample_h3_df, output_dir):
    plot_pooled_salary_by_work_model(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_pooled_salary_by_work_model.png')
    )


def test_plot_pooled_no_error_without_output_dir(sample_h3_df):
    plot_pooled_salary_by_work_model(sample_h3_df, output_dir=None)


def test_plot_pooled_handles_missing_salary(sample_h3_df, output_dir):
    df = sample_h3_df.copy()
    df.loc[0, 'salary_in_usd'] = np.nan
    plot_pooled_salary_by_work_model(df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_pooled_salary_by_work_model.png')
    )


# ── Test 2: plot_salary_trends_by_work_model ─────────────────────

def test_plot_trends_saves_file(sample_h3_df, output_dir):
    plot_salary_trends_by_work_model(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_salary_trends_by_work_model.png')
    )


def test_plot_trends_no_error_without_output_dir(sample_h3_df):
    plot_salary_trends_by_work_model(sample_h3_df, output_dir=None)


# ── Test 3: plot_covid_vs_post_comparison ─────────────────────────

def test_plot_covid_comparison_saves_file(sample_h3_df, output_dir):
    plot_covid_vs_post_comparison(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_covid_vs_post_comparison.png')
    )


def test_plot_covid_comparison_no_error_without_output_dir(sample_h3_df):
    plot_covid_vs_post_comparison(sample_h3_df, output_dir=None)


def test_plot_covid_comparison_era_split(sample_h3_df, output_dir):
    # Data has both COVID (2020-2022) and post-COVID (2023-2024) years
    plot_covid_vs_post_comparison(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_covid_vs_post_comparison.png')
    )


# ── Test 4: plot_salary_distribution_by_era ───────────────────────

def test_plot_distribution_saves_file(sample_h3_df, output_dir):
    plot_salary_distribution_by_era(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_salary_distribution_by_era.png')
    )


def test_plot_distribution_no_error_without_output_dir(sample_h3_df):
    plot_salary_distribution_by_era(sample_h3_df, output_dir=None)


# ── Test 5: run_regression_analysis ──────────────────────────────

def test_regression_saves_summary_file(sample_h3_df, output_dir):
    run_regression_analysis(sample_h3_df, output_dir=output_dir)
    assert os.path.exists(
        os.path.join(output_dir, 'h3_regression_summary.txt')
    )


def test_regression_no_error_without_output_dir(sample_h3_df):
    run_regression_analysis(sample_h3_df, output_dir=None)


def test_regression_summary_contains_ols(sample_h3_df, output_dir):
    run_regression_analysis(sample_h3_df, output_dir=output_dir)
    path = os.path.join(output_dir, 'h3_regression_summary.txt')
    with open(path) as f:
        content = f.read()
    assert 'OLS' in content


# ── Test 6: run_h3_analysis ───────────────────────────────────────

def test_run_h3_analysis_skips_if_plots_exist():
    with patch('Analysis.h3_analysis.check_file_exists', return_value='exists'):
        result = run_h3_analysis()
        assert 'Skipping' in result


def test_run_h3_analysis_returns_string():
    with patch('Analysis.h3_analysis.check_file_exists', return_value='exists'):
        result = run_h3_analysis()
        assert isinstance(result, str)