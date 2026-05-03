from __future__ import print_function

import os

import matplotlib
matplotlib.use('Agg')   # non-interactive backend; remove this line to display charts interactively

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings

from Helper.helper import make_dirs, load_data, check_file_exists
from Helper.H1_constants import PLOTS_DIR, COUNTRY_SHORT

warnings.filterwarnings('ignore')


def plot_salary_by_title(df, output_dir=None):
    """
    Description: Plot median annual salary by developer category as a gradient horizontal bar chart.
        Bars are colored on a blue gradient from lowest to highest median salary.
        Saves the figure to output_dir if provided.
    Args:
        df (pd.DataFrame): Survey data with DevCategory and ConvertedCompYearly columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    data = (
        df.dropna(subset=['ConvertedCompYearly', 'DevCategory'])
        .groupby('DevCategory')['ConvertedCompYearly']
        .median()
        .sort_values()
    )
    values = data.values
    colors = plt.cm.Blues(plt.Normalize(values.min(), values.max())(values))

    fig, ax = plt.subplots(figsize=(8, 10))
    bars = ax.barh(data.index, values, color=colors, edgecolor='white')
    for bar, val in zip(bars, values):
        ax.text(val + 1000, bar.get_y() + bar.get_height() / 2,
                '${:.0f}K'.format(val / 1000), va='center', fontsize=9)

    ax.set_xlabel('Median Annual Salary (USD)')
    ax.set_title('Median Salary by Job Title (2020-2025)', pad=12)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h1_salary_by_title.png'), dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_by_country(df, min_count=200, output_dir=None):
    """
    Description: Plot the top 20 countries by median annual salary as a gradient horizontal bar chart.
        Countries with fewer than min_count responses are excluded.
        Saves the figure to output_dir if provided.
    Args:
        df (pd.DataFrame): Survey data with Country and ConvertedCompYearly columns.
        min_count (int): Minimum responses required to include a country. Defaults to 200.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    data = df.dropna(subset=['ConvertedCompYearly', 'Country'])
    valid_countries = data['Country'].value_counts()
    valid_countries = valid_countries[valid_countries >= min_count].index
    data = data[data['Country'].isin(valid_countries)]

    country_agg = (
        data.groupby('Country')['ConvertedCompYearly']
        .agg(Median='median', Count='count')
        .sort_values('Median', ascending=False)
        .head(20)
        .sort_values('Median')
    )

    values = country_agg['Median'].values
    colors = plt.cm.viridis(plt.Normalize(values.min(), values.max())(values))

    fig, ax = plt.subplots(figsize=(9, 10))
    bars = ax.barh(country_agg.index, values, color=colors, edgecolor='white')
    for bar, val, n in zip(bars, country_agg['Median'], country_agg['Count']):
        ax.text(val + 1500, bar.get_y() + bar.get_height() / 2,
                '${:.0f}K  (n={:,})'.format(val / 1000, n), va='center', fontsize=9)

    ax.set_xlabel('Median Annual Salary (USD)')
    ax.set_title(
        'Top 20 Countries by Median Salary\n(Responses >= {} | 2020-2025)'.format(min_count),
        pad=12,
    )
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_xlim(0, values.max() * 1.15)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h1_salary_by_country.png'), dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_by_seniority(df, output_dir=None):
    """
    Description: Plot median annual salary by seniority bucket as a gradient vertical bar chart.
        Bars are colored on a plasma gradient from lowest to highest seniority.
        Saves the figure to output_dir if provided.
    Args:
        df (pd.DataFrame): Survey data with SeniorityBucket and ConvertedCompYearly columns.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    data = (
        df.dropna(subset=['ConvertedCompYearly', 'SeniorityBucket'])
        .groupby('SeniorityBucket')['ConvertedCompYearly']
        .agg(Median='median', Count='count')
        .sort_values('Median')
    )
    values = data['Median'].values
    colors = plt.cm.plasma(plt.Normalize(values.min(), values.max())(values))

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(data.index.astype(str), values, color=colors, edgecolor='white')
    for bar, val, n in zip(bars, data['Median'], data['Count']):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1500,
                '${:.0f}K\n(n={:,})'.format(val / 1000, n),
                ha='center', va='bottom', fontsize=9)

    ax.set_ylabel('Median Annual Salary (USD)')
    ax.set_xlabel('Seniority Level')
    ax.set_title('Salary Progression by Seniority (2020-2025)', pad=12)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_ylim(0, values.max() * 1.2)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h1_salary_by_seniority.png'), dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_heatmap(df, n_titles=6, n_countries=8, output_dir=None):
    """
    Description: Plot a heatmap of median salary ($K) for the top developer categories
        across the top countries, showing how the same job title pays differently by location.
        Saves the figure to output_dir if provided.
    Args:
        df (pd.DataFrame): Survey data with Country, DevCategory, and ConvertedCompYearly columns.
        n_titles (int): Number of top developer categories to include. Defaults to 6.
        n_countries (int): Number of top countries by response count to include. Defaults to 8.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    top_titles = (
        df.dropna(subset=['DevCategory'])['DevCategory']
        .value_counts().head(n_titles).index.tolist()
    )
    top_countries = (
        df.dropna(subset=['Country'])['Country']
        .value_counts().head(n_countries).index.tolist()
    )

    heat_df = (
        df[df['DevCategory'].isin(top_titles) & df['Country'].isin(top_countries)]
        .dropna(subset=['ConvertedCompYearly'])
        .groupby(['Country', 'DevCategory'])['ConvertedCompYearly']
        .median()
        .unstack('DevCategory')
        .div(1000)
        .round(1)
    )
    heat_df.index = [COUNTRY_SHORT.get(c, c) for c in heat_df.index]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        heat_df, annot=True, fmt='.0f', cmap='YlOrRd',
        linewidths=0.5, linecolor='white', ax=ax,
        cbar_kws={'label': 'Median Salary ($K USD)', 'shrink': 0.8},
        annot_kws={'size': 10},
    )
    ax.set_xlabel('Job Title', labelpad=10)
    ax.set_ylabel('Country', labelpad=10)
    ax.set_title('Median Salary ($K) - Same Title, Different Country (2020-2025)', pad=14)
    ax.tick_params(axis='x', rotation=20, labelsize=10)
    ax.tick_params(axis='y', rotation=0, labelsize=10)
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h1_salary_heatmap.png'), dpi=150, bbox_inches='tight')
    plt.close()


def plot_salary_trends(df, n_titles=6, output_dir=None):
    """
    Description: Plot median salary trends from 2020 to 2025 for the top developer categories
        as a multi-line chart with one line per category.
        Saves the figure to output_dir if provided.
    Args:
        df (pd.DataFrame): Survey data with Year, DevCategory, and ConvertedCompYearly columns.
        n_titles (int): Number of top developer categories to include. Defaults to 6.
        output_dir (str or None): Directory to save the figure. Skips saving if None.
    Returns:
        None
    """
    top = df['DevCategory'].value_counts().head(n_titles).index
    trend = (
        df.dropna(subset=['ConvertedCompYearly', 'DevCategory'])
        .query('DevCategory in @top')
        .groupby(['Year', 'DevCategory'])['ConvertedCompYearly']
        .median()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=trend, x='Year', y='ConvertedCompYearly',
                 hue='DevCategory', marker='o', ax=ax)
    ax.set_xlabel('Survey Year')
    ax.set_ylabel('Median Annual Salary (USD)')
    ax.set_title('Salary Trends by Job Title (2020-2025)')
    plt.tight_layout()

    if output_dir:
        fig.savefig(os.path.join(output_dir, 'h1_salary_trends.png'), dpi=150, bbox_inches='tight')
    plt.close()


def run_analysis(filepath='Data/h1_clean.csv'):
    """
    Description: Run the full H1 analysis pipeline: load data, create the output directory
        using make_dirs, and produce and save all five charts. Skips if plots already exist.
    Args:
        filepath (str): Path to the cleaned survey CSV. Defaults to 'Data/h1_clean.csv'.
    Returns:
        str: Message indicating whether plots were saved or already existed.
    """
    result = check_file_exists(PLOTS_DIR)
    if result:
        return "files already exist in '{}'. Skipping analysis.".format(os.path.abspath(PLOTS_DIR))

    make_dirs(PLOTS_DIR)
    df = load_data(filepath)
    plot_salary_by_title(df, output_dir=PLOTS_DIR)
    plot_salary_by_country(df, output_dir=PLOTS_DIR)
    plot_salary_by_seniority(df, output_dir=PLOTS_DIR)
    plot_salary_heatmap(df, output_dir=PLOTS_DIR)
    plot_salary_trends(df, output_dir=PLOTS_DIR)

    return "All plots saved to '{}'.".format(os.path.abspath(PLOTS_DIR))

if __name__ == '__main__':
    run_analysis()
