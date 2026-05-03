from __future__ import print_function

import gc
import os
import pandas as pd

from Helper.helper import check_file_exists
from Helper.H3_constants import (
    DATA_FILE, ALL_COLS,
    YEAR_MIN, YEAR_MAX,
)

OUTPUT_PATH = "Data/h3_clean.csv"


# ── Load ──────────────────────────────────────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Data file not found -> {}".format(DATA_FILE))
        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)
    available = [c for c in ALL_COLS if c in df.columns]
    df = df[available].copy()
    print("  Loaded: {:,} rows".format(len(df)))
    return df


# ── Clean / Filter ────────────────────────────────────────────────

def filter_years(df):
    before = len(df)
    df = df[df['work_year'].between(YEAR_MIN, YEAR_MAX)].copy()
    print("  After year filter ({}-{}): {:,} rows (dropped {:,})".format(
        YEAR_MIN, YEAR_MAX, len(df), before - len(df)
    ))
    return df


def clean_salary(df):
    before = len(df)
    df = df.dropna(subset=['salary_in_usd']).copy()
    print("  After salary drop: {:,} rows (dropped {:,})".format(
        len(df), before - len(df)
    ))
    return df


# ── Pipeline ──────────────────────────────────────────────────────

def run_preprocessing_h3(output_path=OUTPUT_PATH):
    result = check_file_exists(output_path)
    if result:
        return "File already exists at '{}'. Skipping preprocessing.".format(
            os.path.abspath(output_path)
        )

    print("Loading data...")
    df = load_data()
    if df.empty:
        return "Preprocessing aborted: source file not found."

    df = filter_years(df)
    df = clean_salary(df)

    print("  Final shape: {}".format(df.shape))

    gc.collect()
    df.to_csv(output_path, index=False)
    return "File saved to '{}'.".format(output_path)


if __name__ == "__main__":
    print(run_preprocessing_h3())
