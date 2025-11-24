import argparse
import os
from multiprocessing.pool import ThreadPool

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from src.io.path_definition import get_project_dir


path_to_exe = os.path.join(get_project_dir(), "chromedriver-win64", "chromedriver.exe")

if os.path.isfile(path_to_exe):
    service = Service(path_to_exe)
else:
    raise FileNotFoundError(f"File {path_to_exe} not found")


def access_url_content(url: str) -> None:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=service,
                              options=options
                              )
    driver.get(url)

    related_law = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class="rela-law"]'))
    )

    related_law = related_law.text

    htmlcontent = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="htmlcontent"]'))
    )

    htmlcontent = htmlcontent.text

    history = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'JudHis'))
    )

    history = history.text

    return {"url": url,
            "related_law": related_law,
            "htmlcontent": htmlcontent,
            "history": history}


# -----------------------------
#  Batching helper
# -----------------------------
def chunk_list(data, chunk_size):
    """Yield chunks of list with max size = chunk_size."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--pool_size', type=int, default=2, help='多線程下載的線程數量')
    parser.add_argument('--batch_size', type=int, default=10, help='每個批次處理的 URL 數量')
    parser.add_argument('--date', type=str, help='判決書日期編號 民國年_月_日', required=True)

    args = parser.parse_args()

    file_path = os.path.join(get_project_dir(), "data", f"cases_{args.date}.csv")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    folder_processed = os.path.join(get_project_dir(), "data_processed")
    if not os.path.exists(folder_processed):
        os.makedirs(folder_processed)

    output_filepath = os.path.join(folder_processed, f"cases_processed_{args.date}.csv")

    if os.path.isfile(output_filepath):
        raise FileExistsError(f"File {output_filepath} already exists")

    POOL_SIZE = args.pool_size
    BATCH_SIZE = args.batch_size
    # We only need 2 for this case

    all_results = []

    df_raw = pd.read_csv(file_path, index_col=0)
    all_urls = df_raw['url'].tolist()

    for batch_index, url_batch in enumerate(chunk_list(all_urls, BATCH_SIZE), start=1):
        print(f"Processing batch {batch_index} with {len(url_batch)} URLs...")

        pool = ThreadPool(POOL_SIZE)
        async_results = [pool.apply_async(access_url_content, args=(u,)) for u in url_batch]

        pool.close()
        pool.join()

        # Collect results
        batch_results = [r.get() for r in async_results]
        all_results.extend(batch_results)

        print(f"Completed batch {batch_index}.")

    df_output = pd.DataFrame(all_results)
    df_output = df_raw.merge(df_output, on="url", how="left")

    df_output.to_csv(output_filepath, index=False)