from selenium import webdriver

from src import MAIN_URL

class BasePage:

    main_url: str = MAIN_URL

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver