import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Fix import issues by adding root directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def driver():
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
