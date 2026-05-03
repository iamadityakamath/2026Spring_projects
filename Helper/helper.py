"""
Utility functions for the Stack Overflow Survey Data Manager.
Handles data status checks, user prompts, downloads, and retry logic.
"""

import os
import time
import pandas as pd
import requests
from data_download import OUTPUT_DIR, YEARS, download, extract


def check_file_exists(path):
    """
    Description: Check whether a file or directory already exists at the given path.
    Args:
        path (str): File or directory path to check.
    Returns:
        str or None: A message string if the path exists, None otherwise.
    """
    if os.path.exists(path):
        return "File already exists at '{}'.".format(path)
    return None


def make_dirs(path):
    """
    Description: Create a directory and all intermediate parents if they do not already exist.
    Args:
        path (str): Directory path to create.
    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_zip_path(year):
    """
    Description: Return the local file path where the zip for a given survey year is saved.
    Args:
        year (int): The survey year.
    Returns:
        str: Full path to the zip file.
    """
    return os.path.join(OUTPUT_DIR, "survey_{}.zip".format(year))


def get_extract_dir(year):
    """
    Description: Return the local directory path where a survey year is extracted.
    Args:
        year (int): The survey year.
    Returns:
        str: Full path to the extraction directory.
    """
    return os.path.join(OUTPUT_DIR, str(year))


def already_downloaded(year):
    """
    Description: Check whether the survey data for a given year has already been downloaded
        and extracted by verifying the folder exists and is non-empty.
    Args:
        year (int): The survey year to check.
    Returns:
        bool: True if the year folder exists and contains files, False otherwise.
    """
    folder = get_extract_dir(year)
    return os.path.isdir(folder) and bool(os.listdir(folder))


def check_data_status():
    """
    Description: Check which survey years have been downloaded and which are still missing.
    Args:
        None
    Returns:
        tuple: (downloaded, missing) — two lists of year integers.
    """
    downloaded = []
    missing = []
    for year in YEARS:
        if already_downloaded(year):
            downloaded.append(year)
        else:
            missing.append(year)
    return downloaded, missing


def print_data_status(downloaded, missing):
    """
    Description: Print a formatted table showing downloaded and missing survey years.
    Args:
        downloaded (list): Years that are already downloaded.
        missing (list): Years that are not yet downloaded.
    Returns:
        None
    """
    print("\n" + "=" * 100)
    print("Data Status")
    print("=" * 100)
    if downloaded:
        print("Downloaded: {}".format(", ".join(map(str, downloaded))))
    if missing:
        print("Missing   : {}".format(", ".join(map(str, missing))))
    print("=" * 100)


def ask_confirmation(prompt):
    """
    Description: Prompt the user with a yes/no question and return their answer.
    Args:
        prompt (str): The question to display to the user.
    Returns:
        bool: True if the user answered yes, False if no.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "y","YES", "Y"]:
            return True
        elif response in ["no", "n","NO", "N"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")



def download_missing_years(missing_years):
    """
    Description: Download and extract survey zip files for all missing years.
    Args:
        missing_years (list): Year integers to download.
    Returns:
        tuple: (downloaded, failed) — two lists of year integers.
    """
    downloaded = []
    failed = []

    make_dirs(OUTPUT_DIR)

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0"})
        for year in missing_years:
            zip_path = download(year, session)
            if zip_path:
                extract(zip_path, year)
                downloaded.append(year)
            else:
                failed.append(year)
    return downloaded, failed


def print_download_result(label, downloaded, failed):
    """
    Description: Print a formatted table showing the outcome of a download attempt.
    Args:
        label (str): Section heading (e.g. "Download Result" or "Retry Result").
        downloaded (list): Years that were successfully downloaded.
        failed (list): Years that failed to download.
    Returns:
        None
    """
    print("\n" + "=" * 100)
    print(label)
    print("=" * 100)
    print("Downloaded : {}".format(downloaded or "None"))
    print("Failed     : {}".format(failed or "None"))


def wait_before_retry(seconds=60):
    """
    Description: Display a visible countdown in the terminal before retrying downloads.
    Args:
        seconds (int): Number of seconds to wait. Defaults to 60.
    Returns:
        None
    """
    print("\nWaiting {} seconds before retrying...".format(seconds))
    for remaining in range(seconds, 0, -1):
        print("  Retrying in {:2d} second(s)...".format(remaining), end="\r", flush=True)
        time.sleep(1)
    print("Retrying now...")


def run_download_attempt(years, label):
    """
    Description: Download survey data for the given years, print the result, and return
        the failed years and updated missing years after re-checking data status.
    Args:
        years (list): Year integers to attempt downloading.
        label (str): Section heading for the result table (e.g. "Download Result").
    Returns:
        tuple: (failed, missing) — failed years from this attempt and still-missing years overall.
    """
    downloaded, failed = download_missing_years(years)
    print_download_result(label, downloaded, failed)
    _, missing = check_data_status()
    return failed, missing


def load_data(filepath):
    """
    Description: Load the cleaned H1 survey CSV and print the row count and survey years.
    Args:
        filepath (str): Path to the cleaned CSV file (e.g. h1_clean.csv).
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(filepath)
    print("Rows: {:,}  |  Years: {}".format(
        len(df), sorted(int(y) for y in df['Year'].unique())
    ))
    return df
