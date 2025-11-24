from typing import Union

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src import TYPE_NAME_DICT, MAIN_URL, COURT_CODE, OutputField
from src.page_object_model.home import HomePage


def access_court_verdict_urls(driver, url: str) -> list[str]:
    """Collect all verdict URLs from a paginated court result page.

    This function opens a new browser tab, navigates to the given court URL,
    extracts all verdict links on the page, and follows pagination through the
    "Next" button until no further pages are available. The function guarantees
    that the newly opened tab is always closed, even if exceptions occur.

    Args:
        driver: A Selenium WebDriver instance controlling the browser.
        url (str): The initial URL of the court verdict listing page.

    Returns:
        list[str]: A list of URLs pointing to individual verdict detail pages.

    Raises:
        TimeoutException: If the required page elements fail to load within
            the specified wait time.
    """

    main_tab = driver.current_window_handle

    driver.switch_to.new_window('tab')
    all_urls: list[str] = []

    try:

        while True:
            driver.get(url)

            jud = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'jud'))
            )

            all_verdicts = jud.find_elements(By.TAG_NAME, 'a')

            all_urls.extend(verdict.get_attribute("href") for verdict in all_verdicts)

            try:
                next_page_icon = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'hlNext'))
                )

                url = next_page_icon.get_attribute("href")

            except TimeoutError:
                break

    finally:
        driver.close()
        driver.switch_to.window(main_tab)

    return all_urls


def fill_placeholder(driver: webdriver.Chrome, content: Union[str, int], id: str) -> None:
    """Fill an input field identified by its HTML ID.

    The function waits for an element with the specified ID to be present in the
    DOM and then sends the provided content into the input box.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        content (str | int): The text or number to input.
        id (str): The HTML ID of the placeholder input element.

    Raises:
        TimeoutException: If the element with the given ID does not appear
            before the wait timeout.
    """

    placeholder = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, id))
    )

    placeholder.send_keys(content)


def open_court_new_tab(driver: webdriver.Chrome, court_element, ):
    """Open a court result in a new browser tab and collect its verdict URLs.

    This function extracts the hyperlink from a court listing element, opens
    that link in a newly created tab, collects verdict URLs by calling
    `access_court_verdict_urls()`, and returns to the original tab.

    Args:
        driver (webdriver.Chrome): The active Selenium WebDriver instance.
        court_element: A Selenium WebElement representing a court entry
            (typically an <li> element containing an <a> link).

    Returns:
        tuple[str, list[str]]:
            - The court name (str)
            - A list of verdict URLs for that court (list[str])
    """

    main_tab = driver.current_window_handle

    link = court_element.find_element(By.TAG_NAME, "a")

    court_url = link.get_attribute("href")
    court_name = link.text.split("\n")[0]

    court_verdict_urls = access_court_verdict_urls(driver, url=court_url)

    driver.switch_to.window(main_tab)

    return court_name, court_verdict_urls


def fill_date_range(driver, start, end):
    """Fill the start and end date fields on the search page.

    This helper function populates six date input fields on the court query
    webpage. The fields correspond to the start and end date (year, month, day).

    Args:
        driver: The Selenium WebDriver instance.
        start (list | tuple): A sequence of three values [year, month, day]
            for the start date.
        end (list | tuple): A sequence of three values [year, month, day]
            for the end date.

    Raises:
        TimeoutException: If any of the date input fields fail to load within
            the wait timeout.
    """
    fields = ["dy1","dm1","dd1","dy2","dm2","dd2"]
    values = [*start, *end]
    for val, field in zip(values, fields):
        fill_placeholder(driver, val, field)


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
    driver.get(MAIN_URL)

    output = []

    for idx, type_name in enumerate(COURT_CODE):

        to_be_click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'input[type="checkbox"][name="jud_sys"][value={type_name}]')))

        to_be_click.click()

        # unclick checkbox: the webpage has some strong behavior, such that when clicking one checkbox, all previous checkboxes will be clicked too.
        for prev_type_name in COURT_CODE[:idx]:
            to_be_unclicked = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'input[type="checkbox"][name="jud_sys"][value={prev_type_name}]')))
            if to_be_unclicked.is_selected():
                to_be_unclicked.click()

        fill_date_range(driver, start=[year, month, day], end=[year, month, day])

        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnQry")))

        submit.click()

        tabcontent = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='tab-content']"))
        )
        if tabcontent.text == "查詢結果\n0":
            print(f"{TYPE_NAME_DICT[type_name]} on {year}-{month}-{day} has not result")
            driver.get(MAIN_URL)
            continue
        else:
            dvGrpCourt = WebDriverWait(tabcontent, 10).until(
                EC.presence_of_element_located((By.ID, "dvGrpCourt"))
            )

        all_court_elements = dvGrpCourt.find_elements(By.TAG_NAME, "li")

        for court_element in all_court_elements:

            court_name, court_verdict_urls = open_court_new_tab(driver, court_element)

            print(f"{TYPE_NAME_DICT[type_name]} @ {court_name} on {year}-{month}-{day} has {len(court_verdict_urls)} results")

            metadata = [{OutputField.URL: court_verdict_url,
                         OutputField.TYPE: TYPE_NAME_DICT[type_name],
                         OutputField.COURT: court_name,
                         OutputField.YEAR: year,
                         OutputField.MONTH: month,
                         OutputField.DAY: day} for court_verdict_url in court_verdict_urls]

            output.extend(metadata)

        driver.get(MAIN_URL)

    return output