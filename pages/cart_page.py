import logging
from selenium.webdriver.common.by import By

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.checkout_button = (By.ID, "checkout")

    def proceed_to_checkout(self):
        self.logger.info("Clicking the checkout button.")
        self.driver.find_element(*self.checkout_button).click()
        self.logger.info("Proceeded to the checkout page.")