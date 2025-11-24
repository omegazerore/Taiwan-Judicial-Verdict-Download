from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.page_object_model import BasePage
from src.page_object_model.court import CourtPage


class ResultPage(BasePage):

    def get_courts(self):

        tabcontent = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='tab-content']"))
        )
        if tabcontent.text == "查詢結果\n0":
            self.driver.get(self.main_url)
            return None

        else:
            dvGrpCourt = WebDriverWait(tabcontent, 10).until(
                EC.presence_of_element_located((By.ID, "dvGrpCourt"))
            )

            all_court_elements = dvGrpCourt.find_elements(By.TAG_NAME, "li")

            return CourtPage(self.driver), all_court_elements