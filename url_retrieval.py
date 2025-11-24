import argparse
import os
import sys

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.io.path_definition import get_project_dir
from src.logic_v2 import retrieve_case_by_day

path_to_exe = os.path.join(get_project_dir(), "chromedriver-win64", "chromedriver.exe")

if os.path.isfile(path_to_exe):
    service = Service(path_to_exe)
else:
    raise FileNotFoundError(f"File {path_to_exe} not found")

driver = webdriver.Chrome(service=service,
                          #options=chrome_options
                         )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True, help='year, 民國年')
    parser.add_argument('--month', type=int, required=True, help='month')
    parser.add_argument('--day', type=int, required=True, help='day')
    parser.add_argument('--force', action='store_true', help='force re-download')

    args = parser.parse_args()

    directory = os.path.join(get_project_dir(), "data")
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, f"cases_{args.year}_{args.month}_{args.day}.csv")

    print(f"Start retrieving data... on {args.year}-{args.month}-{args.day}")

    if args.force:
        output = retrieve_case_by_day(driver, year=args.year, month=args.month, day=args.day)
    else:
        if os.path.isfile(filename):
            sys.exit(f"File {filename} already exists")
        else:
            output = retrieve_case_by_day(driver, args.year, args.month, args.day)

    df = pd.DataFrame(output)

    df.to_csv(filename, index=True, encoding="utf-8-sig")

    driver.quit()
