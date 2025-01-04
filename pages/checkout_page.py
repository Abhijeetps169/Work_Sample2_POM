import logging
from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.first_name_field = (By.ID, "first-name")
        self.last_name_field = (By.ID, "last-name")
        self.postal_code_field = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")

    # Locators for price details
    ITEM_TOTAL_LOCATOR = (By.CLASS_NAME, "summary_subtotal_label")  # Item total
    TAX_LOCATOR = (By.CLASS_NAME, "summary_tax_label")  # Tax
    TOTAL_LOCATOR = (By.CLASS_NAME, "summary_total_label")  # Total

    def enter_shipping_details(self, first_name, last_name, postal_code):
        self.logger.info("Entering shipping details.")
        self.driver.find_element(*self.first_name_field).send_keys(first_name)
        self.logger.info(f"Entered first name: {first_name}")
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.logger.info(f"Entered last name: {last_name}")
        self.driver.find_element(*self.postal_code_field).send_keys(postal_code)
        self.logger.info(f"Entered postal code: {postal_code}")
        self.driver.find_element(*self.continue_button).click()
        self.logger.info("Clicked the continue button.")

    def complete_checkout(self):
        self.logger.info("Clicking the finish button to complete checkout.")
        self.driver.find_element(*self.finish_button).click()
        self.logger.info("Checkout completed successfully.")

    def get_item_total(self):
        """
        Fetches the item total from the checkout summary.
        """
        item_total_text = self.driver.find_element(*self.ITEM_TOTAL_LOCATOR).text
        return self._extract_numeric_value(item_total_text)

    def get_tax(self):
        """
        Fetches the tax amount from the checkout summary.
        """
        tax_text = self.driver.find_element(*self.TAX_LOCATOR).text
        return self._extract_numeric_value(tax_text)

    def get_total(self):
        """
        Fetches the total amount from the checkout summary.
        """
        total_text = self.driver.find_element(*self.TOTAL_LOCATOR).text
        return self._extract_numeric_value(total_text)

    @staticmethod
    def _extract_numeric_value(text):
        """
        Extracts the numeric value from a text string like 'Item total: $29.99'.
        """
        return float(text.split("$")[-1])  # Extract and convert the numeric part to float
