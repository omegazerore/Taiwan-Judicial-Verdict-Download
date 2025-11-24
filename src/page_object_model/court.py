from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.page_object_model import BasePage


class CourtPage(BasePage):

    def get_verdict_urls(self, court_element):
        court_name, court_verdict_urls = self.open_court_new_tab(court_element)

        return court_name, court_verdict_urls

    def open_court_new_tab(self, court_element) -> tuple[str, list[str]]:
        """Open a new tab for a specific court and collect all verdict URLs.

        This function opens a new browser tab, clicks on the provided court
        element to navigate to its verdict listing page, and extracts all
        verdict links by handling pagination through the "Next" button until
        no further pages are available. The function ensures that the newly
        opened tab is always closed, even if exceptions occur.

        Args:
            court_element: A Selenium WebElement representing the court link.
        """

        link = court_element.find_element(By.TAG_NAME, "a")

        court_url = link.get_attribute("href")
        court_name = link.text.split("\n")[0]

        court_verdict_urls = self.access_court_verdict_urls(url=court_url)

        return court_name, court_verdict_urls

    def access_court_verdict_urls(self, url: str) -> list[str]:
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

        main_tab = self.driver.current_window_handle

        self.driver.switch_to.new_window('tab')
        all_urls: list[str] = []

        try:

            while True:
                self.driver.get(url)

                jud = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, 'jud'))
                )

                all_verdicts = jud.find_elements(By.TAG_NAME, 'a')

                all_urls.extend([verdict.get_attribute("href") for verdict in all_verdicts])

                try:
                    next_page_icon = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'hlNext'))
                    )

                    url = next_page_icon.get_attribute("href")

                except TimeoutException:
                    break

        finally:
            self.driver.close()
            self.driver.switch_to.window(main_tab)

        return all_urls

