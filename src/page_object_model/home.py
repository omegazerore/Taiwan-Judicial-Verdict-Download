from typing import Union

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src import COURT_CODE
from src.page_object_model import BasePage
from src.page_object_model.result import ResultPage

class HomePage(BasePage):

    def __init__(self, driver: webdriver.Chrome):

        self.driver = driver

    def go_to_homepage(self) -> None:
        self.driver.get(self.main_url)

    def select_court_system(self, idx: int, type_name: str):

        to_be_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'input[type="checkbox"][name="jud_sys"][value={type_name}]')))

        to_be_click.click()

        # unclick checkbox: the webpage has some strong behavior, such that when clicking one checkbox, all previous checkboxes will be clicked too.
        for prev_type_name in COURT_CODE[:idx]:
            to_be_unclicked = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'input[type="checkbox"][name="jud_sys"][value={prev_type_name}]')))
            if to_be_unclicked.is_selected():
                to_be_unclicked.click()

    def fill_date_range(self, start, end) -> None:

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
        fields = ["dy1", "dm1", "dd1", "dy2", "dm2", "dd2"]
        values = [*start, *end]
        for val, field in zip(values, fields):
            self.fill_placeholder(self.driver, val, field)

    def fill_placeholder(self, driver: webdriver.Chrome, content: Union[str, int], id: str) -> None:
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

    def submit(self):

        submit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnQry")))

        submit.click()

        return ResultPage(self.driver)