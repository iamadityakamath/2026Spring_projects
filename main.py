"""
Team: Aditya, Shivani, Kritika
Description: Main script to run the full analysis pipeline for Stack Overflow survey data. 
This includes checking/downloading data, running preprocessing, and running analysis to produce 
charts.
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


def main():
    print(f"Data directory: {BASE}")
    while True:
        downloaded, missing = check_data_status()
        print_data_status(downloaded, missing)

        if not missing:
            print("\n All survey data (2020-2025) is already downloaded!")

            if ask_confirmation("\nProceed with preprocessing? (yes/no): "):
                with Pool(processes=3) as pool:
                    r1 = pool.apply_async(run_preprocessing_h1)
                    r2 = pool.apply_async(run_preprocessing_h2)
                    r3 = pool.apply_async(run_preprocessing_h3)
                    for r in (r1, r2, r3):
                        print("\n" + r.get())
                print("\nPreprocessing completed successfully.")
            else:
                print("\nSkipping preprocessing.")
                

            if ask_confirmation("\nProceed with analysis? (yes/no): "):
                print("\n" + run_h1_analysis())
                print("\n" + run_h2_analysis())
                print("\n" + run_h3_analysis())
            else:
                print("\nSkipping analysis.")

            if ask_confirmation("\nProceed with report generation? (yes/no): "):
                generate_report(filename="report_h1.pdf", title="H1 Analysis Report", hypothesis="h1")
                generate_report(filename="report_h2.pdf", title="H2 Analysis Report", hypothesis="h2")
                generate_report(filename="report_h3.pdf", title="H3 Analysis Report", hypothesis="h3")
            else:
                print("\nSkipping report generation.")

            sys.exit(0)

        print("\n{} year(s) of survey data are missing.".format(len(missing)))

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
        if not ask_confirmation("\nRetry failed years {}? (yes/no): ".format(", ".join(map(str, failed_now)))):
            print("\nExiting...")
            sys.exit(0)

        wait_before_retry(60)
        _, missing = run_download_attempt(failed_now, "Retry Result")
        if not missing:
            print("\nAll missing years were downloaded successfully.")
            continue


if __name__ == "__main__":
    main()
