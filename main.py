"""
Team: Aditya, Shivani, Kritika
Description: Main script to run the full analysis pipeline for Stack Overflow survey data. 
Steps include:
1. checking/downloading data
2. running preprocessing
3. running analysis to produce results
4. generating PDF reports with embedded results and visualizations.
"""

import sys
from multiprocessing import Pool

from Helper.config import BASE
from Helper.helper import (
    check_data_status,
    print_data_status,
    ask_confirmation,
    run_download_attempt,
    wait_before_retry,
)
from Preprocessing.h1_preprocessing import run_preprocessing_h1
from Preprocessing.h2_preprocessing import run_preprocessing_h2
from Preprocessing.h3_preprocessing import run_preprocessing_h3
from Analysis.h1_analysis import run_h1_analysis
from Analysis.h2_analysis import run_h2_analysis
from Analysis.h3_analysis import run_h3_analysis
from download_report import generate_report


def _run(fn):
    return fn()


def _run_parallel(items, worker):
    with Pool(processes=3) as pool:
        return pool.map(worker, items)


def _run_report(args):
    filename, title, hypothesis = args
    return generate_report(filename=filename, title=title, hypothesis=hypothesis)


def main():
    print(f"Data directory: {BASE}")
    while True:
        downloaded, missing = check_data_status()
        print_data_status(downloaded, missing)

        # If every year is already present, move straight into the downstream steps.
        if not missing:
            print("\n All survey data (2020-2025) is already downloaded!")

            if ask_confirmation("\nProceed with preprocessing? (yes/no): "):
                # Run each hypothesis preprocessing task in parallel.
                results = _run_parallel([run_preprocessing_h1, run_preprocessing_h2, run_preprocessing_h3], _run)
                for r in results:
                    print("\n" + r)
                print("\nPreprocessing completed successfully.")
            else:
                print("\nSkipping preprocessing.")

            if ask_confirmation("\nProceed with analysis? (yes/no): "):
                # Run the three hypothesis analyses concurrently.
                results = _run_parallel([run_h1_analysis, run_h2_analysis, run_h3_analysis], _run)
                for r in results:
                    print("\n" + r)
                print("\nAnalysis completed successfully.")
            else:
                print("\nSkipping analysis.")

            if ask_confirmation("\nProceed with report generation? (yes/no): "):
                # Generate one PDF report per hypothesis in parallel.
                report_args = [
                    ("report_h1.pdf", "H1 Analysis Report", "h1"),
                    ("report_h2.pdf", "H2 Analysis Report", "h2"),
                    ("report_h3.pdf", "H3 Analysis Report", "h3"),
                ]
                _run_parallel(report_args, _run_report)
                print("\nReport generation completed successfully.")
            else:
                print("\nSkipping report generation.")

            sys.exit(0)

        print("\n{} year(s) of survey data are missing.".format(len(missing)))

        # Ask before downloading because this can take time and may retry failed years.
        if not ask_confirmation("\nDownload missing data for {}? (yes/no): ".format(", ".join(map(str, missing)))):
            print("\nSkipping download. You can run this script again later.")
            sys.exit(0)

        print("\nStarting download process...\n")
        failed_now, missing = run_download_attempt(missing, "Download Result")
        if not missing:
            print("\nAll missing years were downloaded successfully.")
            continue

        print("\nSome years are still missing: {}".format(", ".join(map(str, missing))))
        print("This may be due to repeated calls to Stack Overflow servers which may block multiple requests.")
        if not failed_now:
            continue
        # Retry only the years that failed in the previous attempt.
        if not ask_confirmation("\nRetry failed years {}? (yes/no): ".format(", ".join(map(str, failed_now)))):
            print("\nExiting...")
            sys.exit(0)

        # Pause before retrying so repeated requests are less likely to be blocked.
        wait_before_retry(60)
        _, missing = run_download_attempt(failed_now, "Retry Result")
        if not missing:
            print("\nAll missing years were downloaded successfully.")
            continue


if __name__ == "__main__":
    main()
