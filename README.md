# 台灣司法院判決下載

This repository provides a tool to download judicial verdicts from Taiwan's Judicial Yuan website.

## 命令提示字元執行:

### 使用以下命令來下載指定日期的判決書 url：
```bash
conda activate env
python -m url_retrieval --year [YEAR] --month [MONTH] --day [DAY]
```

The above command downloads verdicts for the specified date. Replace `[YEAR]`, `[MONTH]`, and `[DAY]` with the desired values.
The result will be saved in the `data` directory as a CSV file named `cases_[YEAR]_[MONTH]_[DAY].csv`.

### 使用以下命令來下載指定日期的判決書內容：
```bash
conda activate env
python -m access_url_content --pool_size 4 --batch_size 100 --date 114_11_20 
```

The code will load the verdicts for the specified date. Replace `114_11_20` with the desired date in the format `YYY_MM_DD`.
The result will be saved in the `data_processed` directory as a CSV file named `cases_processed_[DATE].csv`.

## Chrome Driver 下載 :

https://github.com/dreamshao/chromedriver

## 環境安裝

- conda create -n env python=3.10
- conda activate env
- pip install -r requirements.txt

## Jupyter Notebook Demo:

- demo.ipynb