# Taiwan-Judicial-Verdict-Download

This repository provides a tool to download judicial verdicts from Taiwan's Judicial Yuan website.

## CLI Usage:

```bash
python -m url_retrieval --year [YEAR] --month [MONTH] --day [DAY]
```

The above command downloads verdicts for the specified date. Replace `[YEAR]`, `[MONTH]`, and `[DAY]` with the desired values.
The result will be saved in the `data` directory as a CSV file named `cases_[YEAR]_[MONTH]_[DAY].csv`.

## Chrome Driver Loadload:

https://github.com/dreamshao/chromedriver

## 環境安裝 Environment Setup

- conda create -n env python=3.10
- conda activate env
- pip install -r requirements.txt

## Jupyter Notebook Demo:

- demo.ipynb