"""
H2 Analysis: Do AI Tools Boost Job Satisfaction — And Does Seniority Change That?
==================================================================================
Hypothesis:
    Developers who use AI tools report higher job satisfaction overall,
    but this gap shrinks (or reverses) for senior developers who may rely
    less on AI since their own experience compensates.

Author      : Shivani, Shivani
Dataset     : Data/h2_clean.csv (pre-cleaned Stack Overflow 2024 + 2025)
Constants   : Helper/H2_constants.py
Outputs     : Data/Analysis Plots/H2_Analysis/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from Helper.H2_constants import SENIORITY_BANDS, PLOTS_DIR
from Helper.helper import make_dirs, check_file_exists

# ── Plot style ────────────────────────────────────────────────────
sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['figure.dpi'] = 130

SENIORITY_ORDER = [label for _, label in SENIORITY_BANDS]
CLEAN_DATA_PATH = "Data/h2_clean.csv"


# ══════════════════════════════════════════════════════════════════
# STEP 0 — Load & Filter
# ══════════════════════════════════════════════════════════════════

def load_and_filter(filepath=CLEAN_DATA_PATH):
    """
    Load pre-cleaned H2 dataset and filter to rows needed for analysis.

    H2 requires:
      - year >= 2024 (JobSat only exists from 2024 onwards)
      - JobSat not null
      - AIUser not null
      - SeniorityBand not null

    Args:
        filepath (str): Path to the cleaned CSV file. Defaults to CLEAN_DATA_PATH.

    Returns:
        pd.DataFrame: Filtered H2-ready dataframe.
    """
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

    h2 = df[
        (df['year'] >= 2024) &
        (df['JobSat'].notna()) &
        (df['AIUser'].notna()) &
        (df['SeniorityBand'].notna())
    ].copy()

    print(f"\nH2 working dataset: {h2.shape[0]:,} rows")
    print(f"Years: {sorted(h2['year'].unique())}")
    print(f"\nAI Users vs Non-users:")
    print(h2['AIUser'].value_counts().rename({1.0: 'AI User', 0.0: 'Non-AI User'}))
    print(f"\nSeniority bands:")
    print(h2['SeniorityBand'].value_counts())
    return h2


# ══════════════════════════════════════════════════════════════════
# STEP 1 — Descriptive Statistics
# ══════════════════════════════════════════════════════════════════

def descriptive_stats(h2):
    """
    Print descriptive statistics for H2 analysis.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
    """
    print("\n" + "=" * 60)
    print("STEP 1: Descriptive Statistics")
    print("=" * 60)

    desc = h2.groupby('AIUser')['JobSat'].agg(['mean', 'median', 'std', 'count'])
    desc.index = ['Non-AI User', 'AI User']
    print("\nJobSat by AI Usage:")
    print(desc.round(3).to_string())

    desc2 = h2.groupby('SeniorityBand')['JobSat'].agg(['mean', 'median', 'std', 'count'])
    print("\nJobSat by Seniority Band:")
    print(desc2.round(3).to_string())

    desc3 = h2.groupby(['SeniorityBand', 'AIUser'])['JobSat'].mean().unstack()
    desc3.columns = ['Non-AI User', 'AI User']
    desc3['Gap (AI - Non-AI)'] = desc3['AI User'] - desc3['Non-AI User']
    print("\nMean JobSat by Seniority x AI Usage (key table):")
    print(desc3.round(3).to_string())


# ══════════════════════════════════════════════════════════════════
# STEP 2 — Overall Statistical Test
# ══════════════════════════════════════════════════════════════════

def cohens_d(group1, group2):
    """
    Calculate Cohen's d effect size between two groups.

    Args:
        group1 (pd.Series): First group values.
        group2 (pd.Series): Second group values.

    Returns:
        float: Cohen's d value.

    >>> round(cohens_d(pd.Series([1, 2, 3]), pd.Series([4, 5, 6])), 2)
    -3.0
    """
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(
        ((n1 - 1) * group1.std() ** 2 + (n2 - 1) * group2.std() ** 2) / (n1 + n2 - 2)
    )
    return (group1.mean() - group2.mean()) / pooled_std


def overall_test(h2):
    """
    Run Mann-Whitney U test comparing AI users vs non-users overall.

    Uses Mann-Whitney U (not t-test) because JobSat is an ordinal 0-10
    scale and is not normally distributed.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Overall Mann-Whitney U Test (AI users vs Non-users)")
    print("=" * 60)

    ai_users     = h2[h2['AIUser'] == 1]['JobSat']
    non_ai_users = h2[h2['AIUser'] == 0]['JobSat']

    stat, p_value = stats.mannwhitneyu(ai_users, non_ai_users, alternative='two-sided')
    d = cohens_d(ai_users, non_ai_users)

    print(f"\nMann-Whitney U statistic : {stat:,.0f}")
    print(f"P-value                  : {p_value:.6f}")
    print(f"Significant at α=0.05    : {'Yes' if p_value < 0.05 else 'No'}")
    print(f"Cohen's d (effect size)  : {d:.4f}")
    print(f"Effect size magnitude    : "
          f"{'Small' if abs(d) < 0.2 else 'Medium' if abs(d) < 0.5 else 'Large'}")


# ══════════════════════════════════════════════════════════════════
# STEP 3 — Per Seniority Band Tests
# ══════════════════════════════════════════════════════════════════

def per_seniority_tests(h2):
    """
    Run Mann-Whitney U test per seniority band.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.

    Returns:
        pd.DataFrame: Results with band, means, gap, p-value, effect size, significance.
    """
    print("\n" + "=" * 60)
    print("STEP 3: Mann-Whitney U Test Per Seniority Band")
    print("=" * 60)

    print(f"\n{'Band':<25} {'AI Mean':>10} {'Non-AI Mean':>12} "
          f"{'Gap':>8} {'p-value':>10} {'Cohen d':>10} {'Sig':>5}")
    print("-" * 82)

    results = []
    for band in SENIORITY_ORDER:
        band_df = h2[h2['SeniorityBand'] == band]
        ai_grp  = band_df[band_df['AIUser'] == 1]['JobSat']
        non_grp = band_df[band_df['AIUser'] == 0]['JobSat']

        if len(ai_grp) < 10 or len(non_grp) < 10:
            continue

        stat_b, p_b = stats.mannwhitneyu(ai_grp, non_grp, alternative='two-sided')
        d_b = cohens_d(ai_grp, non_grp)
        sig = '***' if p_b < 0.001 else '**' if p_b < 0.01 else '*' if p_b < 0.05 else 'ns'

        print(f"{band:<25} {ai_grp.mean():>10.3f} {non_grp.mean():>12.3f} "
              f"{(ai_grp.mean() - non_grp.mean()):>+8.3f} "
              f"{p_b:>10.4f} {d_b:>10.3f} {sig:>5}")

        results.append({
            'Band':       band,
            'AI_Mean':    ai_grp.mean(),
            'NonAI_Mean': non_grp.mean(),
            'Gap':        ai_grp.mean() - non_grp.mean(),
            'p_value':    p_b,
            'cohens_d':   d_b,
            'sig':        sig,
        })

    return pd.DataFrame(results)


# ══════════════════════════════════════════════════════════════════
# STEP 4 — Visualizations
# ══════════════════════════════════════════════════════════════════

def plot_overall_boxplot(h2, output_dir):
    """
    Generate and save box plot of overall JobSat by AI usage.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
        output_dir (str): Directory to save the plot.
    """
    h2_plot = h2.copy()
    h2_plot['AI Usage'] = h2_plot['AIUser'].map({1.0: 'AI User', 0.0: 'Non-AI User'})

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(
        data=h2_plot, x='AI Usage', y='JobSat', hue='AI Usage',
        ax=ax, palette=['#E8534A', '#4A90D9'], legend=False
    )
    ax.set_title('Overall: JobSat by AI Usage')
    ax.set_ylabel('Job Satisfaction (0-10)')
    ax.set_xlabel('')

    plt.tight_layout()
    out_path = os.path.join(output_dir, 'H2_plot1_overall_boxplot.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_seniority_gap(results_df, output_dir):
    """
    Generate and save bar chart of JobSat gap by seniority band.

    Args:
        results_df (pd.DataFrame): Per-seniority test results from per_seniority_tests().
        output_dir (str): Directory to save the plot.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ['#2ECC71' if g > 0 else '#E74C3C' for g in results_df['Gap']]
    bars = ax.bar(
        results_df['Band'], results_df['Gap'],
        color=colors, edgecolor='white', width=0.5
    )
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title('JobSat Gap (AI User − Non-User) by Seniority')
    ax.set_ylabel('Mean JobSat Difference')
    ax.tick_params(axis='x', rotation=20)
    for bar, row in zip(bars, results_df.itertuples()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.003,
            row.sig, ha='center', fontsize=12, fontweight='bold'
        )

    plt.tight_layout()
    out_path = os.path.join(output_dir, 'H2_plot2_seniority_gap.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_grouped_bar(h2, output_dir):
    """
    Generate and save grouped bar chart of mean JobSat by seniority x AI usage.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
        output_dir (str): Directory to save the plot.
    """
    h2_plot = h2.copy()
    h2_plot['AI Usage'] = h2_plot['AIUser'].map({1.0: 'AI User', 0.0: 'Non-AI User'})

    plot_data = (
        h2_plot
        .groupby(['SeniorityBand', 'AI Usage'])['JobSat']
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=plot_data, x='SeniorityBand', y='JobSat',
        hue='AI Usage', ax=ax,
        palette={'AI User': '#4A90D9', 'Non-AI User': '#E8534A'},
        order=SENIORITY_ORDER
    )
    ax.set_title('Mean JobSat by Seniority × AI Usage')
    ax.set_ylabel('Mean Job Satisfaction')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=20)
    ax.legend(title='', loc='lower right')

    plt.tight_layout()
    out_path = os.path.join(output_dir, 'H2_plot3_grouped_bar.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def generate_plots(h2, results_df):
    """
    Generate and save all three H2 plots as separate PNG files.

    Plots saved to PLOTS_DIR defined in H2_constants.py:
      - H2_plot1_overall_boxplot.png
      - H2_plot2_seniority_gap.png
      - H2_plot3_grouped_bar.png

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
        results_df (pd.DataFrame): Per-seniority test results from per_seniority_tests().
    """
    print("\n" + "=" * 60)
    print("STEP 4: Generating Plots")
    print("=" * 60)

    make_dirs(PLOTS_DIR)
    plot_overall_boxplot(h2, output_dir=PLOTS_DIR)
    plot_seniority_gap(results_df, output_dir=PLOTS_DIR)
    plot_grouped_bar(h2, output_dir=PLOTS_DIR)


# ══════════════════════════════════════════════════════════════════
# STEP 5 — AI Sentiment Correlation
# ══════════════════════════════════════════════════════════════════

def sentiment_correlation(h2):
    """
    Run Spearman correlation between AI sentiment and job satisfaction.

    Uses Spearman (not Pearson) because AISent is ordinal and
    JobSat is not normally distributed.

    Args:
        h2 (pd.DataFrame): H2-filtered dataframe.
    """
    print("\n" + "=" * 60)
    print("STEP 5: AI Sentiment vs Job Satisfaction (Spearman Correlation)")
    print("=" * 60)

    sent_map = {
        'Very unfavorable': 1,
        'Unfavorable':      2,
        'Indifferent':      3,
        'Favorable':        4,
        'Very favorable':   5,
    }
    h2 = h2.copy()
    h2['AISentNumeric'] = h2['AISent'].map(sent_map)
    h2_sent_valid = h2[h2['AISentNumeric'].notna()]

    corr, p_corr = stats.spearmanr(
        h2_sent_valid['AISentNumeric'],
        h2_sent_valid['JobSat']
    )

    print(f"\nSpearman r  : {corr:.3f}")
    print(f"P-value     : {p_corr:.6f}")
    print(f"Significant : {'Yes' if p_corr < 0.05 else 'No'}")
    print(f"Direction   : {'Positive' if corr > 0 else 'Negative'} correlation")
    print(f"\nInterpretation: Developers with more favorable AI sentiment tend to "
          f"report {'higher' if corr > 0 else 'lower'} job satisfaction.")


# ══════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ══════════════════════════════════════════════════════════════════

def run_h2_analysis(filepath='Data/h2_clean.csv'):
    """
    Description: Run the full H2 analysis pipeline: load data, run statistical
        tests, and produce and save all plots. Skips if plots already exist.
    Args:
        filepath (str): Path to the cleaned survey CSV. Defaults to 'Data/h2_clean.csv'.
    Returns:
        str: Message indicating whether plots were saved or already existed.
    """
    result = check_file_exists(PLOTS_DIR)
    if result:
        return "Files already exist in '{}'. Skipping analysis for h2.".format(os.path.abspath(PLOTS_DIR))

    make_dirs(PLOTS_DIR)

    h2         = load_and_filter(filepath)
    descriptive_stats(h2)
    overall_test(h2)
    results_df = per_seniority_tests(h2)
    generate_plots(h2, results_df)
    sentiment_correlation(h2)

    return "All plots saved to '{}'.".format(os.path.abspath(PLOTS_DIR))


if __name__ == '__main__':
    print(run_h2_analysis())