###### This is filtering data taking 2021-2024 filtering the columns relevant to the hypotheses #############

import pandas as pd

## to get all the columns from all 4 datasets make sure to match the file names.
# files = {
#     2021: 'survey_results_public_2021.csv',  # update filenames to match yours
#     2022: 'survey_results_public_2022.csv',
#     2023: 'survey_results_public_2023.csv',
#     2024: 'survey_results_public_2024.csv',
# }
# for year, path in files.items():
#     df = pd.read_csv(path, nrows=1)
#     print(f"\n=== {year} — {len(df.columns)} columns ===")
#     print(df.columns.tolist())

######## COMMENT EVERYTHING BELOW TO EXECUTE THE ABOVE CODE ##############

#### COMMON CODE FOR BOTH PARTS KEEP UNCOMMENTED TO RUN THE CODE BELOW ###########
dfs = {}
dfs[2021] = pd.read_csv('survey_results_public_2021.csv')
dfs[2022] = pd.read_csv('survey_results_public_2022.csv')
dfs[2023] = pd.read_csv('survey_results_public_2023.csv')
dfs[2024] = pd.read_csv('survey_results_public_2024.csv')
#####################################################################################


## PART 1 =================relevant columns only for particular year=========================

# # Add year column to each
# for year, df in dfs.items():
#     df['year'] = year
#
# # ── Columns needed per hypothesis ────────────────────────────────
# # H1: salary ~ job title + country + seniority (all 4 years)
# H1_cols = ['year', 'DevType', 'Country', 'YearsCodePro',
#            'ConvertedCompYearly', 'EdLevel', 'OrgSize', 'Employment']
#
# # H2: AI usage vs job satisfaction by seniority (2023-2024 only)
# H2_cols = ['year', 'YearsCodePro', 'AISelect', 'AISent', 'AIBen',
#            'AIToolCurrently Using', 'JobSat', 'DevType', 'Country']
#
# # H3: remote work salary trend (2022-2024 only)
# H3_cols = ['year', 'RemoteWork', 'ConvertedCompYearly',
#            'YearsCodePro', 'Country', 'DevType']
#
# # ── Build each combined dataset ───────────────────────────────────
# def safe_select(df, cols):
#     """Only keep columns that exist in this df"""
#     return df[[c for c in cols if c in df.columns]].copy()
#
# # H1 — all 4 years
# h1 = pd.concat([safe_select(df, H1_cols) for df in dfs.values()], ignore_index=True)
#
# # H2 — 2023 and 2024 only
# h2 = pd.concat([safe_select(dfs[y], H2_cols) for y in [2023, 2024]], ignore_index=True)
#
# # H3 — 2022, 2023, 2024 only
# h3 = pd.concat([safe_select(dfs[y], H3_cols) for y in [2022, 2023, 2024]], ignore_index=True)
#
# # ── Quick summary ─────────────────────────────────────────────────
# for name, df in [('H1', h1), ('H2', h2), ('H3', h3)]:
#     print(f"\n{name}: {df.shape}")
#     print(f"  Columns: {df.columns.tolist()}")
#     print(f"  Years:   {sorted(df['year'].unique())}")
#     print(f"  Nulls:\n{df.isnull().sum()}")


## ============== Combing all the relevant columns in one big dataset ===================

# Add year column to each
for year, df in dfs.items():
    df['year'] = year

# ── All columns we need across all hypotheses ─────────────────────
ALL_COLS = [
    'year',
    # Identity / seniority
    'YearsCodePro', 'DevType', 'EdLevel', 'Employment',
    # Location / company
    'Country', 'OrgSize',
    # Salary
    'ConvertedCompYearly',
    # Remote work (H3)
    'RemoteWork',
    # AI columns (H2) — only exist in 2023/2024
    'AISelect', 'AISent', 'AIBen',
    'AIToolCurrently Using',
    # Job satisfaction (H2) — only exists in 2024
    'JobSat',
]

# ── Combine — keep only columns that exist in each year ───────────
def safe_select(df, cols):
    return df[[c for c in cols if c in df.columns]].copy()

combined = pd.concat(
    [safe_select(df, ALL_COLS) for df in dfs.values()],
    ignore_index=True
)

# ── Summary ───────────────────────────────────────────────────────
print(f"Shape: {combined.shape}")
print(f"\nColumns: {combined.columns.tolist()}")
print(f"\nYears: {sorted(combined['year'].unique())}")
print(f"\nNull counts:\n{combined.isnull().sum()}")

# ── Save ──────────────────────────────────────────────────────────
combined.to_csv('so_combined_2021_2024.csv', index=False)
print("\nSaved to so_combined_2021_2024.csv")