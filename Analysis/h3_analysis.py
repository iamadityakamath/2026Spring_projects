"""
Team: Aditya, Shivani, Kritika
Description: H3 Analysis — Remote Work Salary Premium Over Time.
Tests whether the salary advantage of remote roles (2020-2022) has faded
by 2023-2024, and whether pooling all years together is misleading.
"""

from __future__ import print_function

import os

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings

from Helper.helper import make_dirs, check_file_exists
from Helper.H3_constants import PLOTS_DIR, WORK_MODELS

warnings.filterwarnings('ignore')


def load_h3_data(filepath):
    """
    Description: Load the cleaned H3 CSV and print row count and year range.
    Args:
        filepath (str): Path to the cleaned CSV file (e.g. h3_clean.csv).
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(filepath)
    print("Rows: {:,}  |  Years: {}".format(
        len(df), sorted(int(y) for y in df['work_year'].unique())
    ))
    return df


def plot_pooled_salary_by_work_model(df, output_dir=None):
    """
    Description: Plot median salary by work model (pooling all years).
        This shows the naive/misleading view that ignores time trends.
    Args:
        df (pd.DataFrame): H3 data with work_models and salary_in_usd columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    data = (
        df.dropna(subset=['salary_in_usd', 'work_models'])
        .groupby('work_models')['salary_in_usd']
        .agg(Median='median', Count='count')
        .reindex([m for m in WORK_MODELS if m in df['work_models'].values])
    )

    values = data['Median'].values
    colors = plt.cm.Set2(np.linspace(0.1, 0.7, len(data)))

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(data.index, values, color=colors, edgecolor='white', width=0.5)
    for bar, val, n in zip(bars, data['Median'], data['Count']):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1500,
                '${:.0f}K\n(n={:,})'.format(val / 1000, n),
                ha='center', va='bottom', fontsize=9)

    ax.set_ylabel('Median Annual Salary (USD)')
    ax.set_xlabel('Work Model')
    ax.set_title('Pooled Median Salary by Work Model (2020-2024)\n(Misleading — ignores time trends)', pad=12)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_ylim(0, values.max() * 1.25)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h3_pooled_salary_by_work_model.png'),
                    dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_trends_by_work_model(df, output_dir=None):
    """
    Description: Plot median salary trends from 2020 to 2024 for each work model
        as a multi-line chart. This reveals how the remote premium has changed over time.
    Args:
        df (pd.DataFrame): H3 data with work_year, work_models, and salary_in_usd columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    grouped = (
        df.dropna(subset=['salary_in_usd', 'work_models'])
        .groupby(['work_year', 'work_models'])['salary_in_usd']
        .median()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=grouped, x='work_year', y='salary_in_usd',
                 hue='work_models', marker='o', ax=ax)

    ax.set_xlabel('Year')
    ax.set_ylabel('Median Salary (USD)')
    ax.set_title('Salary Trends by Work Model (2020-2024)', pad=12)
    ax.set_xticks(sorted(df['work_year'].unique()))
    ax.grid(axis='both', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(title='Work Model')
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h3_salary_trends_by_work_model.png'),
                    dpi=150, bbox_inches='tight')
    plt.close()


def plot_covid_vs_post_comparison(df, output_dir=None):
    """
    Description: Compare median salaries for Remote vs On-site in two eras:
        COVID (2020-2022) and post-COVID (2023-2024) side by side.
        This directly tests H3: whether the remote premium has faded.
    Args:
        df (pd.DataFrame): H3 data with work_year, work_models, and salary_in_usd columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    df = df.dropna(subset=['salary_in_usd', 'work_models']).copy()
    df['Era'] = df['work_year'].apply(
        lambda y: 'COVID (2020-2022)' if y <= 2022 else 'Post-COVID (2023-2024)'
    )

    era_model = (
        df.groupby(['Era', 'work_models'])['salary_in_usd']
        .agg(Median='median', Count='count')
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    eras = ['COVID (2020-2022)', 'Post-COVID (2023-2024)']
    models = [m for m in WORK_MODELS if m in era_model['work_models'].values]
    x = np.arange(len(models))
    width = 0.35

    colors = {'COVID (2020-2022)': '#85B7EB', 'Post-COVID (2023-2024)': '#ED93B1'}

    for i, era in enumerate(eras):
        subset = era_model[era_model['Era'] == era].set_index('work_models').reindex(models)
        vals = subset['Median'].values
        counts = subset['Count'].values
        bars = ax.bar(x + i * width, vals, width, label=era,
                      color=colors[era], edgecolor='white')
        for bar, val, n in zip(bars, vals, counts):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width() / 2, val + 1500,
                        '${:.0f}K\n(n={:,})'.format(val / 1000, int(n)),
                        ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('Median Annual Salary (USD)')
    ax.set_xlabel('Work Model')
    ax.set_title('Remote Salary Premium: COVID vs Post-COVID Era', pad=12)
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_ylim(0, era_model['Median'].max() * 1.25)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h3_covid_vs_post_comparison.png'),
                    dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_distribution_by_era(df, output_dir=None):
    """
    Description: Box plot showing the salary distribution for each work model,
        split by COVID vs post-COVID era, to visualize spread and outliers.
    Args:
        df (pd.DataFrame): H3 data with work_year, work_models, and salary_in_usd columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    df = df.dropna(subset=['salary_in_usd', 'work_models']).copy()
    df['Era'] = df['work_year'].apply(
        lambda y: 'COVID (2020-2022)' if y <= 2022 else 'Post-COVID (2023-2024)'
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='work_models', y='salary_in_usd', hue='Era',
                order=[m for m in WORK_MODELS if m in df['work_models'].values],
                palette={'COVID (2020-2022)': '#85B7EB', 'Post-COVID (2023-2024)': '#ED93B1'},
                ax=ax, showfliers=False)

    ax.set_ylabel('Annual Salary (USD)')
    ax.set_xlabel('Work Model')
    ax.set_title('Salary Distribution by Work Model and Era', pad=12)
    ax.legend(title='Era')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h3_salary_distribution_by_era.png'),
                    dpi=150, bbox_inches='tight')
    plt.close()


def run_regression_analysis(df, output_dir=None):
    """
    Description: Run two OLS regressions and save a summary text file:
        1. Naive model: salary ~ work_models (ignoring time — misleading)
        2. Correct model: salary ~ work_models * work_year + experience_level
        The comparison shows that pooling years masks the fading remote premium.
    Args:
        df (pd.DataFrame): H3 data with work_models, salary_in_usd, work_year, experience_level.
        output_dir (str or None): Directory to save the summary. Skips saving if None.
    Returns:
        None
    """
    import statsmodels.formula.api as smf

    df = df.dropna(subset=['salary_in_usd', 'work_models', 'work_year', 'experience_level']).copy()

    model_naive = smf.ols(
        'salary_in_usd ~ C(work_models)',
        data=df
    ).fit()

    model_correct = smf.ols(
        'salary_in_usd ~ C(work_models) * work_year + experience_level',
        data=df
    ).fit()

    summary_text = (
        "=== Naive Model ===\n" + model_naive.summary().as_text() +
        "\n\n=== Corrected Model ===\n" + model_correct.summary().as_text()
    )

    if output_dir:
        with open(os.path.join(output_dir, 'h3_regression_summary.txt'), 'w') as f:
            f.write(summary_text)


def run_h3_analysis(filepath='Data/h3_clean.csv'):
    """
    Description: Run the full H3 analysis pipeline: load data, create the output directory,
        and produce all charts and the regression summary. Skips if plots already exist.
    Args:
        filepath (str): Path to the cleaned H3 CSV. Defaults to 'Data/h3_clean.csv'.
    Returns:
        str: Message indicating whether plots were saved or already existed.
    """
    result = check_file_exists(PLOTS_DIR)
    if result:
        return "Files already exist in '{}'. Skipping analysis.".format(os.path.abspath(PLOTS_DIR))

    make_dirs(PLOTS_DIR)
    df = load_h3_data(filepath)

    plot_pooled_salary_by_work_model(df, output_dir=PLOTS_DIR)
    plot_salary_trends_by_work_model(df, output_dir=PLOTS_DIR)
    plot_covid_vs_post_comparison(df, output_dir=PLOTS_DIR)
    plot_salary_distribution_by_era(df, output_dir=PLOTS_DIR)
    run_regression_analysis(df, output_dir=PLOTS_DIR)

    return "All H3 plots and regression saved to '{}'.".format(os.path.abspath(PLOTS_DIR))


if __name__ == '__main__':
    run_h3_analysis()