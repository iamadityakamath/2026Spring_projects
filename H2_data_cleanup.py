import pandas as pd
import numpy as np

################ combine 2023-2025 year data with relevant columns #############

# ── Load each year ────────────────────────────────────────────────
df2023 = pd.read_csv('survey_results_public_2023.csv')
df2024 = pd.read_csv('survey_results_public_2024.csv')
df2025 = pd.read_csv('survey_results_public_2025.csv', low_memory=False)

# # ── Add year column ───────────────────────────────────────────────
# df2023['year'] = 2023
# df2024['year'] = 2024
# df2025['year'] = 2025
#
# # ── Normalize 2025 columns to match 2023/2024 naming ─────────────
# # YearsCodePro → WorkExp in 2025
# df2025.rename(columns={'WorkExp': 'YearsCodePro'}, inplace=True)
#
# # AIToolCurrently Using → combine both partial and mostly AI columns
# df2025['AIToolCurrently Using'] = df2025.apply(
#     lambda r: ';'.join(filter(pd.notna, [
#         r.get('AIToolCurrently mostly AI', ''),
#         r.get('AIToolCurrently partially AI', '')
#     ])), axis=1
# )
#
# # AIBen is gone in 2025 — fill with NaN so column still exists
# df2025['AIBen'] = float('nan')
#
# # ── Select only the columns we need ──────────────────────────────
# ALL_COLS = [
#     'year',
#     # Seniority / role
#     'YearsCodePro', 'DevType', 'EdLevel', 'Employment',
#     # Location / company
#     'Country', 'OrgSize',
#     # Salary (H1, H3)
#     'ConvertedCompYearly',
#     # Remote work (H3)
#     'RemoteWork',
#     # AI columns (H2)
#     'AISelect', 'AISent', 'AIBen', 'AIToolCurrently Using',
#     # Job satisfaction (H2)
#     'JobSat',
# ]
#
# def safe_select(df, cols):
#     return df[[c for c in cols if c in df.columns]].copy()
#
# combined = pd.concat(
#     [safe_select(df2023, ALL_COLS),
#      safe_select(df2024, ALL_COLS),
#      safe_select(df2025, ALL_COLS)],
#     ignore_index=True
# )
#
# # ── Summary ───────────────────────────────────────────────────────
# print(f"Shape: {combined.shape}")
# print(f"\nColumns: {combined.columns.tolist()}")
# print(f"\nRows per year:\n{combined['year'].value_counts().sort_index()}")
# print(f"\nNull counts:\n{combined.isnull().sum()}")
#
# # ── Save ──────────────────────────────────────────────────────────
# combined.to_csv('so_combined_2023_2025.csv', index=False)
# print("\nSaved to so_combined_2023_2025.csv")



############# ================== Code cleanup ======================= ##################
# comment the above code except the imports to execute this part

# ── Load combined file ────────────────────────────────────────────
df = pd.read_csv('so_combined_2023_2025.csv', low_memory=False)
print(f"Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

# ═════════════════════════════════════════════════════════════════
# 1. YEARS CODE PRO — clean text values to numeric
# YearsCodePro — converts "Less than 1 year" → 0.5, "More than 50 years" → 51, everything else to float. Caps at 50.
# ═════════════════════════════════════════════════════════════════

def clean_years(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip()
    if val.lower() == 'less than 1 year':
        return 0.5
    if val.lower() == 'more than 50 years':
        return 51.0
    try:
        return float(val)
    except:
        return np.nan

df['YearsCodePro'] = df['YearsCodePro'].apply(clean_years)

# Cap extreme outliers (> 50 years professional experience is unreliable)
df['YearsCodePro'] = df['YearsCodePro'].clip(upper=50)

print(f"\nYearsCodePro — min: {df['YearsCodePro'].min()}, "
      f"max: {df['YearsCodePro'].max()}, "
      f"nulls: {df['YearsCodePro'].isna().sum():,}")

# ═════════════════════════════════════════════════════════════════
# 2. SENIORITY BANDS — group YearsCodePro into levels for H2
# SeniorityBand — groups into Junior/Mid-level/Senior/Expert bands for H2 grouping
# ═════════════════════════════════════════════════════════════════
def seniority_band(years):
    if pd.isna(years):
        return np.nan
    if years <= 2:
        return 'Junior (0-2 yrs)'
    elif years <= 7:
        return 'Mid-level (3-7 yrs)'
    elif years <= 15:
        return 'Senior (8-15 yrs)'
    else:
        return 'Expert (16+ yrs)'

df['SeniorityBand'] = df['YearsCodePro'].apply(seniority_band)
print(f"\nSeniority distribution:\n{df['SeniorityBand'].value_counts()}")

# ═════════════════════════════════════════════════════════════════
# 3. EMPLOYMENT — simplify multi-select to primary status
# Employment — simplifies 181 messy multi-select combinations into 5 clean categories
# ═════════════════════════════════════════════════════════════════
def simplify_employment(val):
    if pd.isna(val):
        return np.nan
    if 'Employed, full-time' in str(val):
        return 'Full-time'
    if 'Independent contractor' in str(val):
        return 'Freelancer/Contractor'
    if 'Student' in str(val):
        return 'Student'
    if 'part-time' in str(val).lower():
        return 'Part-time'
    if 'not employed' in str(val).lower():
        return 'Not employed'
    return 'Other'

df['EmploymentSimple'] = df['Employment'].apply(simplify_employment)
print(f"\nEmployment distribution:\n{df['EmploymentSimple'].value_counts()}")

# ═════════════════════════════════════════════════════════════════
# 4. AI USAGE — simplify AISelect to binary + frequency
# AIUser + AIFrequency — creates a binary AIUser flag (1/0) and a frequency column from AISelect
# ═════════════════════════════════════════════════════════════════
def ai_user(val):
    if pd.isna(val):
        return np.nan
    if str(val).startswith('Yes'):
        return 1
    return 0

df['AIUser'] = df['AISelect'].apply(ai_user)

# AI frequency — how often they use it
def ai_frequency(val):
    if pd.isna(val):
        return np.nan
    val = str(val)
    if 'daily' in val.lower():
        return 'Daily'
    if 'weekly' in val.lower():
        return 'Weekly'
    if 'monthly' in val.lower():
        return 'Monthly/Infrequently'
    if val == 'Yes':
        return 'Yes (unspecified)'
    return 'Non-user'

df['AIFrequency'] = df['AISelect'].apply(ai_frequency)
print(f"\nAI Usage distribution:\n{df['AIUser'].value_counts()}")
print(f"\nAI Frequency distribution:\n{df['AIFrequency'].value_counts()}")

# ═════════════════════════════════════════════════════════════════
# 5. REMOTE WORK — simplify to 3 clean categories for H3
# RemoteWorkSimple — collapses 7 remote work variants into Remote/Hybrid/In-person for H3
# ═════════════════════════════════════════════════════════════════
def simplify_remote(val):
    if pd.isna(val):
        return np.nan
    val = str(val).lower()
    if 'remote' in val and 'hybrid' not in val and 'in-person' not in val:
        return 'Remote'
    if 'in-person' in val and 'hybrid' not in val and 'remote' not in val:
        return 'In-person'
    if 'hybrid' in val or 'choice' in val or 'flexible' in val:
        return 'Hybrid'
    return np.nan

df['RemoteWorkSimple'] = df['RemoteWork'].apply(simplify_remote)
print(f"\nRemote work distribution:\n{df['RemoteWorkSimple'].value_counts()}")

# ═════════════════════════════════════════════════════════════════
# 6. SALARY — remove extreme outliers
# Salary — removes unrealistic salaries (below $10k or above $1M)
# ═════════════════════════════════════════════════════════════════
# Keep only salaries between $10k and $1M (reasonable range)
salary_mask = (
    df['ConvertedCompYearly'].between(10000, 1000000) |
    df['ConvertedCompYearly'].isna()
)
removed = (~salary_mask).sum()
df = df[salary_mask].copy()
print(f"\nSalary outliers removed: {removed:,} rows")
print(f"Salary range: ${df['ConvertedCompYearly'].min():,.0f} "
      f"– ${df['ConvertedCompYearly'].max():,.0f}")

# ═════════════════════════════════════════════════════════════════
# 7. DEVTYPE — take first role for multi-select responses
# DevTypePrimary — takes the first role from multi-select DevType strings
# ═════════════════════════════════════════════════════════════════
df['DevTypePrimary'] = df['DevType'].apply(
    lambda x: str(x).split(';')[0].strip() if pd.notna(x) else np.nan
)
print(f"\nTop 10 DevTypes:\n{df['DevTypePrimary'].value_counts().head(10)}")

# ═════════════════════════════════════════════════════════════════
# 8. FINAL SHAPE + NULL SUMMARY
# ═════════════════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"Final shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
print(f"\nNull counts after cleaning:")
print(df.isnull().sum())

# ═════════════════════════════════════════════════════════════════
# 9. SAVE
# ═════════════════════════════════════════════════════════════════
df.to_csv('so_cleaned_2023_2025.csv', index=False)
print(f"\n✓ Saved to so_cleaned_2023_2025.csv")