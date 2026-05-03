import gc
import os
import numpy as np
import pandas as pd

from Helper.helper import check_file_exists
from Helper.H2_constants import (
    ALL_COLS, YEAR_FILES, COLUMN_OVERRIDES_2025,
    SALARY_LOW, SALARY_HIGH,
    SENIORITY_BANDS, EMPLOYMENT_MAP, AI_FREQUENCY_MAP, REMOTE_MAP,
)

OUTPUT_PATH = "Data/h2_clean.csv"


# ── Load ──────────────────────────────────────────────────────────

def load_year(year):
    path = YEAR_FILES[year]
    if not os.path.exists(path):
        print("{}: file not found -> {}".format(year, path))
        return pd.DataFrame()

    df = pd.read_csv(path, low_memory=False)
    df['year'] = year

    if year == 2025:
        df.rename(columns=COLUMN_OVERRIDES_2025, inplace=True)
        df['AIToolCurrently Using'] = df.apply(
            lambda r: ';'.join(filter(pd.notna, [
                r.get('AIToolCurrently mostly AI', ''),
                r.get('AIToolCurrently partially AI', '')
            ])), axis=1
        )
        df['AIBen'] = float('nan')

    available = [c for c in ALL_COLS if c in df.columns]
    return df[available].copy()


def load_all_years():
    frames = [load_year(yr) for yr in sorted(YEAR_FILES)]
    combined = pd.concat([f for f in frames if not f.empty], ignore_index=True)
    del frames
    gc.collect()
    return combined


# ── Clean / Engineer ──────────────────────────────────────────────

def _clean_years_col(series):
    return (
        series.astype(str)
        .str.strip()
        .replace({"Less than 1 year": "0.5", "More than 50 years": "51",
                  "nan": np.nan, "NA": np.nan})
        .pipe(pd.to_numeric, errors="coerce")
    )


def engineer_seniority(df):
    df['YearsCodePro'] = _clean_years_col(df['YearsCodePro']).clip(upper=50)

    def _band(years):
        if pd.isna(years):
            return np.nan
        for threshold, label in SENIORITY_BANDS:
            if years <= threshold:
                return label
        return np.nan

    df['SeniorityBand'] = df['YearsCodePro'].apply(_band)
    return df


def clean_employment(df):
    def _simplify(val):
        if pd.isna(val):
            return np.nan
        s = str(val)
        for key, label in EMPLOYMENT_MAP.items():
            if key in s:
                return label
        if 'Student' in s:
            return 'Student'
        if 'part-time' in s.lower():
            return 'Part-time'
        if 'not employed' in s.lower():
            return 'Not employed'
        return 'Other'

    df['EmploymentSimple'] = df['Employment'].apply(_simplify)
    return df


def engineer_ai_features(df):
    def _ai_user(val):
        if pd.isna(val):
            return np.nan
        return 1 if str(val).startswith('Yes') else 0

    def _ai_frequency(val):
        if pd.isna(val):
            return np.nan
        v = str(val)
        for keyword, label in AI_FREQUENCY_MAP.items():
            if keyword in v.lower():
                return label
        if v == 'Yes':
            return 'Yes (unspecified)'
        return 'Non-user'

    df['AIUser'] = df['AISelect'].apply(_ai_user)
    df['AIFrequency'] = df['AISelect'].apply(_ai_frequency)
    return df


def clean_remote_work(df):
    def _simplify(val):
        if pd.isna(val):
            return np.nan
        v = str(val).lower()
        if 'remote' in v and 'hybrid' not in v and 'in-person' not in v:
            return REMOTE_MAP['remote']
        if 'in-person' in v and 'hybrid' not in v and 'remote' not in v:
            return REMOTE_MAP['in-person']
        if 'hybrid' in v or 'choice' in v or 'flexible' in v:
            return REMOTE_MAP['hybrid']
        return np.nan

    df['RemoteWorkSimple'] = df['RemoteWork'].apply(_simplify)
    return df


def clean_salary(df):
    df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
    mask = (
        df['ConvertedCompYearly'].between(SALARY_LOW, SALARY_HIGH) |
        df['ConvertedCompYearly'].isna()
    )
    removed = (~mask).sum()
    df = df[mask].copy()
    print("  Salary outliers removed: {:,} rows".format(removed))
    return df


def engineer_dev_type(df):
    df['DevTypePrimary'] = (
        df['DevType'].astype(str).str.split(';').str[0].str.strip().replace('nan', np.nan)
    )
    return df


# ── Pipeline ──────────────────────────────────────────────────────

def run_preprocessing_h2(output_path=OUTPUT_PATH):
    result = check_file_exists(output_path)
    if result:
        return "File already exists at '{}'. Skipping preprocessing.".format(
            os.path.abspath(output_path)
        )

    print("Loading surveys...")
    df = load_all_years()
    print("  Combined: {:,} rows".format(df.shape[0]))

    df = engineer_seniority(df)
    print("  Seniority engineered")

    df = clean_employment(df)
    print("  Employment simplified")

    df = engineer_ai_features(df)
    print("  AI features engineered")

    df = clean_remote_work(df)
    print("  Remote work simplified")

    df = clean_salary(df)

    df = engineer_dev_type(df)
    print("  Final shape: {}".format(df.shape))

    df.to_csv(output_path, index=False)
    return "File saved to '{}'.".format(output_path)


if __name__ == "__main__":
    print(run_preprocessing_h2())
