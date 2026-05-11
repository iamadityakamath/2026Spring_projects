"""
Download Stack Overflow Developer Surveys (2020-2025) as CSV files.
Skips years that have already been downloaded.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# BASE_URL = os.getenv("BASE_URL", "https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-{year}.zip")
BASE_URL = os.getenv("BASE_URL", "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive/{year}/results.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "Data/so_surveys")
YEARS = range(int(os.getenv("YEAR_START", 2020)), int(os.getenv("YEAR_END", 2026)))

def download(year, session):
    """Download the survey CSV for year. Returns file path or None on error."""
    url = BASE_URL.format(year=year)
    year_dir = os.path.join(OUTPUT_DIR, str(year))
    os.makedirs(year_dir, exist_ok=True)
    csv_path = os.path.join(year_dir, "survey_results_public.csv")

    print("\n[{}] Downloading {}".format(year, url))
    try:
        response = session.get(url, stream=True, timeout=60)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("  x HTTP error: {}".format(exc))
        return None
    except requests.RequestException as exc:
        print("  x Request failed: {}".format(exc))
        return None

    total = int(response.headers.get("content-length", 0))
    received = 0

    with open(csv_path, "wb") as fh:
        for chunk in response.iter_content(chunk_size=8192):
            fh.write(chunk)
            received += len(chunk)
            if total:
                print("\r  {:.1f}%  ({:,} / {:,} bytes)".format(
                    received / total * 100, received, total), end="")

    print("\r  Done  ({:,} bytes){}".format(received, " " * 20))
    return csv_path


def print_summary(results):
    """Print a formatted download summary."""
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    if results["success"]:
        print("Downloaded : {}".format(results["success"]))
    if results["skipped"]:
        print("Skipped    : {}".format(results["skipped"]))
    if results["failed"]:
        print("Failed     : {}".format(results["failed"]))

    print("\nOutput folder: {}".format(os.path.abspath(OUTPUT_DIR)))
    print("\nDownloaded CSV files:")
    for year in sorted(results["success"] + results["skipped"]):
        csv_file = os.path.join(str(year), "survey_results_public.csv")
        print("  {}".format(csv_file))

    if results["failed"]:
        print("\nRetry in 30 seconds -- the following URLs had issues:")
        for year in results["failed"]:
            print("  {}".format(BASE_URL.format(year=year)))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Saving surveys to: {}/".format(os.path.abspath(OUTPUT_DIR)))
    print("=" * 60)

    results = {"success": [], "skipped": [], "failed": []}

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        for year in YEARS:
            csv_file = os.path.join(OUTPUT_DIR, str(year), "survey_results_public.csv")
            if os.path.exists(csv_file):
                print("\n[{}] Already exists -- skipping".format(year))
                results["skipped"].append(year)
                continue

            csv_path = download(year, session)
            if csv_path:
                results["success"].append(year)
            else:
                results["failed"].append(year)
    print_summary(results)

if __name__ == "__main__":
    main()