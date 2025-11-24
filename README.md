# 台灣司法院判決下載

This repository provides a tool to download judicial verdicts from Taiwan's Judicial Yuan website.

## 命令提示字元執行:

```bash
conda activate env
python -m url_retrieval --year [YEAR] --month [MONTH] --day [DAY]
```

The above command downloads verdicts for the specified date. Replace `[YEAR]`, `[MONTH]`, and `[DAY]` with the desired values.
The result will be saved in the `data` directory as a CSV file named `cases_[YEAR]_[MONTH]_[DAY].csv`.

## Chrome Driver 下載 :

https://github.com/dreamshao/chromedriver

## 環境安裝

- conda create -n env python=3.10
- conda activate env
- pip install -r requirements.txt

## Jupyter Notebook Demo:

- demo.ipynb