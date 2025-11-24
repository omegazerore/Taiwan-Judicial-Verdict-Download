from typing import Union

from selenium import webdriver

from src import TYPE_NAME_DICT, COURT_CODE, OutputField
from src.page_object_model.home import HomePage


def retrieve_case_by_day(driver: webdriver.Chrome, year: Union[int, str], month: Union[int, str], day: Union[int, str]) -> list[dict]:
    """Retrieve all court verdicts for a specific calendar date.

    The function iterates through all court system types defined in
    ``COURT_CODE``, performs a date-based query for each system, parses the
    results, and compiles structured metadata for each verdict. If a court
    system returns no results, it logs a message and moves on.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance handling the
            browsing session.
        year (int | str): The target year.
        month (int | str): The target month.
        day (int | str): The target day.

    Returns:
        list[dict]: A list of metadata dictionaries, where each dictionary
        contains:
            - URL: The verdict URL.
            - TYPE: The court system type name.
            - COURT: The court name.
            - YEAR, MONTH, DAY: The query date breakdown.
    """

    home = HomePage(driver)
    home.go_to_homepage()

    url_output = []

    for idx, type_name in enumerate(COURT_CODE):

        home.select_court_system(idx=idx, type_name=type_name)
        home.fill_date_range(start=[year, month, day], end=[year, month, day])

        result = home.submit()

        output = result.get_courts()

        if not output:
            print(f"{TYPE_NAME_DICT[type_name]} on {year}-{month}-{day} has not result")
            continue

        court = output[0]

        for court_element in output[1]:

            court_name, court_verdict_urls = court.open_court_new_tab(court_element)

            print(f"{TYPE_NAME_DICT[type_name]} @ {court_name} on {year}-{month}-{day} has {len(court_verdict_urls)} results")

            metadata = [{OutputField.URL: court_verdict_url,
                         OutputField.TYPE: TYPE_NAME_DICT[type_name],
                         OutputField.COURT: court_name,
                         OutputField.YEAR: year,
                         OutputField.MONTH: month,
                         OutputField.DAY: day} for court_verdict_url in court_verdict_urls]

            url_output.extend(metadata)

        home.go_to_homepage()

    return url_output