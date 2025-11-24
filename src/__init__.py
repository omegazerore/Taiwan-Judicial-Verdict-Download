from enum import Enum

TYPE_NAME_DICT = {"C": "憲法",
                  "V": "民事",
                  "M": "刑事",
                  "A": "行政",
                  "P": "懲戒"}

MAIN_URL = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"

COURT_CODE = ["C", "V", "M", "A", "P"]

class OutputField(str, Enum):

    URL = "url"
    TYPE = "type"
    COURT = "court"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"