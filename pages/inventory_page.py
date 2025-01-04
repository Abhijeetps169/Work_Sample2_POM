import logging
from selenium.webdriver.common.by import By

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.add_to_cart_button = (By.CSS_SELECTOR, ".inventory_item button")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def add_items_to_cart(self):
        self.logger.info("Adding items to the cart.")
        buttons = self.driver.find_elements(*self.add_to_cart_button)
        for idx, button in enumerate(buttons[:2]):  # Add the first 2 items to the cart
            button.click()
            self.logger.info(f"Added item {idx + 1} to the cart.")
        self.logger.info("Finished adding items to the cart.")

    def go_to_cart(self):
        self.logger.info("Navigating to the cart page.")
        self.driver.find_element(*self.cart_icon).click()
        self.logger.info("Navigated to the cart page.")
