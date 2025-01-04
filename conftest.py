import pytest
import logging
import os

# Path for log files
LOG_FILE_PATH = "reports/test_logs.log"

def pytest_configure(config):
    """
    Configure pytest to generate an HTML report and set up logging.
    """
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Configure the HTML report path
    config.option.htmlpath = "reports/test_report.html"

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # Log to file
            logging.StreamHandler()  # Log to console
        ]
    )
    logging.info("Logging initialized.")


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """
    Fixture to ensure logging setup for the test session.
    """
    logging.info("Test session started.")
    yield
    logging.info("Test session completed.")


@pytest.fixture
def setup(request):
    """
    Fixture to initialize the WebDriver and handle teardown.
    """
    from selenium import webdriver

    # Set up WebDriver
    driver = webdriver.Chrome()  # Replace with appropriate WebDriver if needed
    driver.maximize_window()

    yield driver  # Pass the driver to the test

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to attach logs and screenshots to the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)  # Attach report to the item

    if report.when == "call" and report.failed:  # Only handle failed tests
        # Save a screenshot if the test uses the setup fixture
        driver = item.funcargs.get("setup")
        if driver:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved: {screenshot_path}")

            # Attach the screenshot to the HTML report
            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(report, "extra", [])
            extra.append(pytest_html.extras.image(screenshot_path))
            report.extra = extra

        # Attach logs to the HTML report
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as f:
                log_content = f.read()
            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(report, "extra", [])
            extra.append(pytest_html.extras.text(log_content, "Test Logs"))
            report.extra = extra
