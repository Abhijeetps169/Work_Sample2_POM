import logging
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("setup")
class TestSauceDemoCheckout:
    def test_end_to_end_checkout(self, setup):
        """
        Test case for end-to-end checkout functionality.
        """
        driver = setup
        try:
            logger.info("Opening SauceDemo website.")
            driver.get("https://www.saucedemo.com/")

            # Login
            login_page = LoginPage(driver)
            logger.info("Logging into SauceDemo.")
            login_page.login("standard_user", "secret_sauce")

            # Add items to cart
            inventory_page = InventoryPage(driver)
            logger.info("Adding items to the cart.")
            inventory_page.add_items_to_cart()
            logger.info("Navigating to the cart.")
            inventory_page.go_to_cart()

            # Proceed to checkout
            cart_page = CartPage(driver)
            logger.info("Proceeding to checkout.")
            cart_page.proceed_to_checkout()

            # Enter shipping details and complete checkout
            checkout_page = CheckoutPage(driver)
            logger.info("Entering shipping details.")
            checkout_page.enter_shipping_details("Abhijeet", "Shinde", "12345")
            logger.info("Completing the checkout process.")
            checkout_page.complete_checkout()

            # Verify checkout success
            assert "Thank you for your order!" in driver.page_source
            logger.info("End-to-end checkout test completed successfully.")

        except Exception as e:
            logger.error(f"Test failed due to an error: {e}")
            pytest.fail(f"Test failed: {e}")

    @pytest.mark.price
    def test_verify_total_price(self, setup):
        """
        Test case to verify that total price is equal to item total plus tax.
        """
        driver = setup
        try:
            logger.info("Opening SauceDemo website.")
            driver.get("https://www.saucedemo.com/")

            # Login
            login_page = LoginPage(driver)
            logger.info("Logging into SauceDemo.")
            login_page.login("standard_user", "secret_sauce")

            # Add items to cart
            inventory_page = InventoryPage(driver)
            logger.info("Adding items to the cart.")
            inventory_page.add_items_to_cart()
            logger.info("Navigating to the cart.")
            inventory_page.go_to_cart()

            # Proceed to checkout
            cart_page = CartPage(driver)
            logger.info("Proceeding to checkout.")
            cart_page.proceed_to_checkout()

            # Enter shipping details and complete checkout
            checkout_page = CheckoutPage(driver)
            logger.info("Entering shipping details.")
            checkout_page.enter_shipping_details("Abhijeet", "Shinde", "12345")


            # Verify total price calculation
            checkout_page = CheckoutPage(driver)
            logger.info("Verifying total price.")
            item_total = checkout_page.get_item_total()  # Assume it fetches the item total
            tax = checkout_page.get_tax()  # Assume it fetches the tax amount
            total = checkout_page.get_total()  # Assume it fetches the total amount

            assert total == item_total + tax, "Total price does not match the sum of item total and tax."
            logger.info("Total price verification successful.")

        except Exception as e:
            logger.error(f"Test failed due to an error: {e}")
            pytest.fail(f"Test failed: {e}")