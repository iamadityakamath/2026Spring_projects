"""
Team: Aditya, Shivani, Kritika
Description: Main script to run the full analysis pipeline for Stack Overflow survey data. 
This includes checking/downloading data, running preprocessing, and running analysis to produce 
charts.
"""

import sys

from Helper.helper import (
    check_data_status,
    print_data_status,
    ask_confirmation,
    run_download_attempt,
    wait_before_retry,
)
from Preprocessing.h1_preprocessing import run_preprocessing_h1
from Preprocessing.h2_preprocessing import run_preprocessing_h2
from Analysis.h1_analysis import run_analysis


def main():
    while True:
        downloaded, missing = check_data_status()
        print_data_status(downloaded, missing)

        if not missing:
            print("\n All survey data (2020-2025) is already downloaded!")

            if ask_confirmation("\nProceed with preprocessing? (yes/no): "):
                print("\n" + run_preprocessing_h1())
                print("\n" + run_preprocessing_h2())
            else:
                print("\nSkipping preprocessing.")
                

            if ask_confirmation("\nProceed with analysis? (yes/no): "):
                print("\n" + run_analysis())
            else:
                print("\nSkipping analysis.")

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
