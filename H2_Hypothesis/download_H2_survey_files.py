"""
download_data.py
================
Run this script once before starting any analysis notebook.
It automatically downloads the Stack Overflow Developer Survey data
for 2023, 2024, and 2025 into the data/ folder.

once all three files are downloaded and extracted, run the 'H2_data_cleanup.py'.

Usage:
    python download_data.py
"""

import time
import os
import ssl
import zipfile
import urllib.request
import certifi

# ── SSL context using certifi certificates ────────────────────────
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

# ── Correct download links (from survey.stackoverflow.co) ─────────
SURVEYS = {
    2023: "https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-2023.zip",
    2024: "https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-2024.zip",
    2025: "https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-2025.zip",
}

# ── Target filenames after extraction ────────────────────────────
EXPECTED_FILES = {
    2023: "data/survey_results_public_2023.csv",
    2024: "data/survey_results_public_2024.csv",
    2025: "data/survey_results_public_2025.csv",
}

# ── Create data folder if it doesn't exist ────────────────────────
os.makedirs("data", exist_ok=True)


def download_and_extract(year, url, target_path):
    """Download a zip file and extract the survey CSV."""

    # Skip if already downloaded
    if os.path.exists(target_path):
        print(f"✓ {year} survey already exists — skipping download")
        return

    zip_path = f"data/survey_{year}.zip"

    # ── Download ──────────────────────────────────────────────────
    print(f"Downloading {year} survey... ", end="", flush=True)
    try:
        with urllib.request.urlopen(url, context=SSL_CONTEXT) as response:
            with open(zip_path, "wb") as f:
                f.write(response.read())
        print("done")
    except Exception as e:
        print(f"\n✗ Failed to download {year} survey: {e}")
        print(f"  Please download it manually from:")
        print(f"  https://survey.stackoverflow.co/{year}/")
        print(f"  and save the CSV as: {target_path}")
        return

    # ── Extract ───────────────────────────────────────────────────
    print(f"Extracting {year} survey... ", end="", flush=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            # Find the main survey CSV inside the zip
            csv_files = [f for f in z.namelist()
                         if f.endswith(".csv") and "results_public" in f.lower()]

            if not csv_files:
                # Fallback — grab the largest CSV in the zip
                csv_files = sorted(
                    [f for f in z.namelist() if f.endswith(".csv")],
                    key=lambda f: z.getinfo(f).file_size,
                    reverse=True
                )

            if csv_files:
                source = csv_files[0]
                z.extract(source, "data/tmp")
                extracted = os.path.join("data/tmp", source)
                os.rename(extracted, target_path)
                import shutil
                shutil.rmtree("data/tmp", ignore_errors=True)
                print("done")
            else:
                print(f"\n✗ Could not find survey CSV inside the zip for {year}")

    except zipfile.BadZipFile:
        print(f"\n✗ Downloaded file for {year} is not a valid zip")
        print(f"  Please download manually from: https://survey.stackoverflow.co/{year}/")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def verify_downloads():
    """Check all files downloaded correctly and print a summary."""
    print("\n" + "=" * 50)
    print("Download Summary")
    print("=" * 50)

    all_good = True
    for year, path in EXPECTED_FILES.items():
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✓ {year}: {path} ({size_mb:.1f} MB)")
        else:
            print(f"✗ {year}: {path} — NOT FOUND")
            all_good = False

    print("=" * 50)
    if all_good:
        print("All surveys downloaded! You can now run the notebooks.")
    else:
        print("Some files are missing. See instructions above.")


# ── Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Stack Overflow Developer Survey Downloader")
    print("=" * 50)

    for year, url in SURVEYS.items():
        download_and_extract(year, url, EXPECTED_FILES[year])
        time.sleep(10)  # wait 5 seconds between downloads

    verify_downloads()