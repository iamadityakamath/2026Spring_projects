"""
Download and extract Stack Overflow Developer Surveys (2020-2025).
Skips years that have already been downloaded and extracted.
"""

import os
import zipfile

import requests

BASE_URL = "https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-{year}.zip"
OUTPUT_DIR = "so_surveys"
YEARS = range(2020, 2026)


# Helpers

def make_dirs(path):
    """Create directory (and parents) if it does not already exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def already_downloaded(year):
    """Return True if the extracted folder for *year* exists and is non-empty."""
    folder = os.path.join(OUTPUT_DIR, str(year))
    return os.path.isdir(folder) and bool(os.listdir(folder))


def get_zip_path(year):
    """Return the local zip file path for *year*."""
    return os.path.join(OUTPUT_DIR, "survey_{}.zip".format(year))


def get_extract_dir(year):
    """Return the local extraction directory for *year*."""
    return os.path.join(OUTPUT_DIR, str(year))

def download(year, session):
    """Download the survey zip for year. Returns zip path or None on error."""
    url = BASE_URL.format(year=year)
    zip_path = get_zip_path(year)

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

    with open(zip_path, "wb") as fh:
        for chunk in response.iter_content(chunk_size=8192):
            fh.write(chunk)
            received += len(chunk)
            if total:
                print("\r  {:.1f}%  ({:,} / {:,} bytes)".format(
                    received / total * 100, received, total), end="")

    print("\r  Done  ({:,} bytes){}".format(received, " " * 20))
    return zip_path


def extract(zip_path, year):
    """Extract *zip_path* into the year subfolder and remove the zip."""
    extract_dir = get_extract_dir(year)
    make_dirs(extract_dir)

    print("  Extracting to {}/".format(extract_dir))
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
        files = zf.namelist()

    os.remove(zip_path)
    print("  Extracted {} file(s): {}".format(len(files), ", ".join(files)))


def print_summary(results):
    """Print a formatted download summary."""
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    if results["success"]:
        print("  + Downloaded : {}".format(results["success"]))
    if results["skipped"]:
        print("  - Skipped    : {}".format(results["skipped"]))
    if results["failed"]:
        print("  x Failed     : {}".format(results["failed"]))

    print("\nOutput folder: {}".format(os.path.abspath(OUTPUT_DIR)))
    print("\nFolder structure:")
    for year in sorted(results["success"] + results["skipped"]):
        files = os.listdir(get_extract_dir(year))
        print("  {}/  ->  {}".format(year, ", ".join(files)))

    if results["failed"]:
        print("\nRetry in 30 seconds -- the following URLs had issues:")
        for year in results["failed"]:
            print("  {}".format(BASE_URL.format(year=year)))


def main():
    make_dirs(OUTPUT_DIR)
    print("Saving surveys to: {}/".format(os.path.abspath(OUTPUT_DIR)))
    print("=" * 60)

    results = {"success": [], "skipped": [], "failed": []}

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        for year in YEARS:
            if already_downloaded(year):
                files = os.listdir(get_extract_dir(year))
                print("\n[{}] Already exists -- skipping ({})".format(year, ", ".join(files)))
                results["skipped"].append(year)
                continue

            zip_path = download(year, session)
            if zip_path:
                extract(zip_path, year)
                results["success"].append(year)
            else:
                results["failed"].append(year)

    print_summary(results)


if __name__ == "__main__":
    main()