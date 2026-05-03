from __future__ import print_function

import gc
import os
import warnings
import numpy as np
import pandas as pd

from Helper.helper import check_file_exists
from Helper.H1_constants import (
    YEAR_FILES, FINAL_COLS, COLUMN_OVERRIDES,
    KEEP_EMPLOYMENT, SALARY_LOW, SALARY_HIGH,
    DEV_CATEGORY_MAP, ORG_SIZE_MAP,
    TIER1, TIER2, TIER3,
)

# warnings.filterwarnings("ignore")


def _build_col_map(year):
    """
    Description: 
        Build a mapping of column names to raw column names for a given year.
        This accounts for any differences in column names across survey years.
    Args:
        year (int): The survey year for which to build the column mapping.
    Returns:
        dict: A mapping of column names to raw column names for the specified year. 
        Values are None when that column was not collected in the given year.
    """
    col_map = {col: col for col in FINAL_COLS}
    col_map.update(COLUMN_OVERRIDES.get(year, {}))
    return col_map


def load_year(year):
    """
    Description: Load and map columns of a single survey year's CSV into a DataFrame.
        Missing files are skipped. columns absent in a given year are filled with NaN.
    Args:
        year (int): The survey year to load (must be a key in YEAR_FILES).
    Returns:
        pd.DataFrame: Rows from that year with canonical column names and a leading Year column,
            or an empty DataFrame if the source file does not exist.
    """
    path = YEAR_FILES[year]
    if not os.path.exists(path):
        print("{}: file not found -> {}".format(year, path))
        return pd.DataFrame()

    col_map = _build_col_map(year)
    raw_cols = {v for v in col_map.values() if v is not None}
    df_raw = pd.read_csv(path, usecols=lambda c: c in raw_cols)

    df = pd.DataFrame()
    for canonical, raw in col_map.items():
        df[canonical] = df_raw[raw] if (raw and raw in df_raw.columns) else np.nan

    del df_raw
    gc.collect()

    df.insert(0, "Year", year)
    return df


def load_all_years():
    """
    Description: Load and concatenate all available survey years into one DataFrame.
        Years whose files are missing are silently skipped.
    Args:
        None
    Returns:
        pd.DataFrame: Combined rows from all years with a reset integer index.
    """
    frames = [load_year(yr) for yr in sorted(YEAR_FILES)]
    combined = pd.concat([f for f in frames if not f.empty], ignore_index=True)
    del frames
    gc.collect()
    return combined


# Filtering

def filter_professional_developers(df):
    """
    Description: Retain only respondents who identify as professional developers and are currently employed.
        Filters on MainBranch containing "developer by profession" and Employment being in KEEP_EMPLOYMENT.
    Args:
        df (pd.DataFrame): Combined survey data with at least MainBranch and Employment columns.
    Returns:
        pd.DataFrame: Subset of df where both conditions are satisfied.
    """
    is_prof = df["MainBranch"].str.contains("developer by profession", na=False)
    is_employed = df["Employment"].isin(KEEP_EMPLOYMENT)
    return df[is_prof & is_employed].copy()


# Salary

def clean_salary(df):
    """
    Description: Parse the salary column, remove outliers outside [SALARY_LOW, SALARY_HIGH],
    Args:
        df (pd.DataFrame): DataFrame with a ConvertedCompYearly column (may be string or numeric).
    Returns:
        pd.DataFrame: Filtered rows with ConvertedCompYearly as numeric
    """
    df["ConvertedCompYearly"] = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce")
    mask = df["ConvertedCompYearly"].between(SALARY_LOW, SALARY_HIGH)
    df = df[mask].copy()
    return df


# Seniority

def _clean_years_col(series):
    """
    Description: Normalise a raw years-of-experience column to a numeric float Series.
        Converts strings ("Less than 1 year", "More than 50 years") to representative
        floats and converts all remaining non-numeric values to NaN.
    Args:
        series (pd.Series): Raw years column as read from the survey CSV.
    Returns:
        pd.Series: Float Series with strings replaced and unparseable values as NaN.
    """
    return (
        series.astype(str)
        .str.strip()
        .replace({"Less than 1 year": "0.5", "More than 50 years": "51", "nan": np.nan, "NA": np.nan})
        .pipe(pd.to_numeric, errors="coerce")
    )


def engineer_seniority(df):
    """
    Description: Derive a continuous SeniorityYears column and a bucketed SeniorityBucket column.
        YearsCodePro is used when available; YearsCode is the fallback.
        Bucket edges (right-inclusive): (0,2], (2,5], (5,10], (10,20], (20, inf).
    Args:
        df (pd.DataFrame): DataFrame with YearsCode, YearsCodePro, and WorkExp columns.
    Returns:
        pd.DataFrame: Input DataFrame with SeniorityYears (float) and SeniorityBucket (Categorical) added.
    """
    df["YearsCode"]    = _clean_years_col(df["YearsCode"])
    df["YearsCodePro"] = _clean_years_col(df["YearsCodePro"])
    df["WorkExp"]      = pd.to_numeric(df["WorkExp"], errors="coerce")

    df["SeniorityYears"] = df["YearsCodePro"].fillna(df["YearsCode"])

    bins   = [0, 2, 5, 10, 20, float("inf")]
    labels = ["0-2 yrs", "3-5 yrs", "6-10 yrs", "11-20 yrs", "20+ yrs"]
    df["SeniorityBucket"] = pd.cut(df["SeniorityYears"], bins=bins, labels=labels)
    return df


# Developer type

def engineer_dev_type(df):
    """
    Description: Extract the primary developer type from the semicolon-delimited DevType column
        and map it to a coarser DevCategory label using DEV_CATEGORY_MAP.
        Types not present in the map are labelled "Other".
    Args:
        df (pd.DataFrame): DataFrame with a DevType column (semicolon-delimited free-text).
    Returns:
        pd.DataFrame: Input DataFrame with DevTypePrimary (str) and DevCategory (str) columns added.
    """
    df["DevTypePrimary"] = (
        df["DevType"].astype(str).str.split(";").str[0].str.strip().replace("nan", np.nan)
    )
    df["DevCategory"] = df["DevTypePrimary"].map(DEV_CATEGORY_MAP).fillna("Other")
    return df


# Country tier

def _assign_tier(country):
    """
    Description: Return the income tier label for a single country name.
        Countries are classified into four tiers based on typical developer salary levels;
        NaN or missing values return "Unknown".
    Args:
        country (str or float): Country name string, or NaN/None if missing.
    Returns:
        str: One of "Tier1_High", "Tier2_UpperMid", "Tier3_Mid", "Tier4_Lower", or "Unknown".
    """
    if pd.isna(country):
        return "Unknown"
    if country in TIER1:
        return "Tier1_High"
    if country in TIER2:
        return "Tier2_UpperMid"
    if country in TIER3:
        return "Tier3_Mid"
    return "Tier4_Lower"


def engineer_country_tier(df):
    """
    Description: Add a CountryTier column by applying _assign_tier to each row's Country value.
    Args:
        df (pd.DataFrame): DataFrame with a Country column.
    Returns:
        pd.DataFrame: Input DataFrame with a new CountryTier (str) column added.
    """
    df["CountryTier"] = df["Country"].apply(_assign_tier)
    return df


# Org size

def clean_org_size(df):
    """
    Description: Map the free-text OrgSize column to a numeric ordinal (1-9) using ORG_SIZE_MAP.
        Unrecognised values and "I don't know" are left as NaN.
    Args:
        df (pd.DataFrame): DataFrame with an OrgSize column containing survey free-text values.
    Returns:
        pd.DataFrame: Input DataFrame with a new OrgSizeNum (float) column added.
    """
    df["OrgSizeNum"] = df["OrgSize"].map(ORG_SIZE_MAP)
    return df


# Pipeline

def run_preprocessing(output_path="Data/h1_clean.csv"):
    """
    Description: Run the full preprocessing pipeline: load all survey years, filter to professional
        developers, clean salary, engineer seniority/dev-type/country-tier/org-size features,
        drop rows missing salary or dev type, and write the result to CSV.
    Args:
        output_path (str): File path for the output CSV. Defaults to "h1_clean.csv".
    Returns:
        str: Message indicating whether the file was saved or already existed.
    """
    result = check_file_exists(output_path)
    if result:
        return "File already exists at '{}'. Skipping preprocessing.".format(os.path.abspath(output_path))

    print("Loading surveys...")
    df = load_all_years()
    print("  Combined: {:,} rows".format(df.shape[0]))

    df = filter_professional_developers(df)
    print("  After professional-dev filter: {:,} rows".format(len(df)))

    df = clean_salary(df)
    print("  After salary filter: {:,} rows".format(len(df)))

    df = engineer_seniority(df)
    df = engineer_dev_type(df)
    df = engineer_country_tier(df)
    df = clean_org_size(df)

    before = len(df)
    df = df.dropna(subset=["ConvertedCompYearly", "DevTypePrimary"])
    print("  Dropped {:,} rows missing salary or DevType".format(before - len(df)))
    print("  Final shape: {}".format(df.shape))

    df.to_csv(output_path, index=False)
    return "File saved to '{}'.".format(output_path)


if __name__ == "__main__":
    run_preprocessing()
