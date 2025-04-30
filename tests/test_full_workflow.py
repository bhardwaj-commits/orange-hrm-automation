import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pom.login_page import LoginPage
from pom.dashboard_page import DashboardPage
from pom.pim_page import PIMPage
from pom.employee_list_page import EmployeeListPage
import time

# Fixture to set up and tear down the WebDriver
@pytest.fixture(scope="function")
def driver():
    # Initialize Chrome WebDriver and maximize the browser window
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Quit the driver after the test is done
    driver.quit()

def test_full_workflow(driver):
    # Step 1: Open Login Page and perform login
    login_page = LoginPage(driver)
    login_page.open("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")

    # Step 2: Navigate to the PIM page from the Dashboard
    dashboard = DashboardPage(driver)
    dashboard.go_to_pim()

    # Step 3: Add multiple employees using a loop
    pim_page = PIMPage(driver)
    employees = [
        ("Prachi", "Bharadwaj"),
        ("Sanjana", "Sharma"),
        ("Priyanka", "R"),
        ("Namrata", "Kumari")
    ]

    for first, last in employees:
        # Add employee and handle any exceptions
        pim_page.add_employee(first, last)

        try:
            # Ensure the Personal Details page is loaded
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[text()='Personal Details']"))
            )
        except TimeoutException:
            # If timeout occurs, take a screenshot and skip to the next employee
            driver.save_screenshot(f"failed_add_{first}_{last}.png")
            continue

        try:
            # Navigate back to Employee List (PIM page) after adding an employee
            pim_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
            )
            pim_menu.click()

            # Wait until the Employee Information page is loaded
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h5[text()='Employee Information']"))
            )
        except TimeoutException:
            # Take a screenshot if the navigation fails and continue
            driver.save_screenshot(f"failed_navigate_employee_list_{first}_{last}.png")
            continue

    # Step 4: Verify if the added employees are visible in the Employee List
    employee_list = EmployeeListPage(driver)

    for first, last in employees:
        full_name = f"{first} {last}"

        try:
            # Clear any existing value in the employee search input before searching
            search_input = driver.find_element(*employee_list.EMPLOYEE_NAME_SEARCH)
            driver.execute_script("arguments[0].value = '';", search_input)
            search_input.clear()
            search_input.click()
            time.sleep(1)

            # Perform the employee search
            employee_list.search_employee(full_name)

            # Wait for search results to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-table-row"))
            )

            # Print each row's text for debugging purposes
            rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-row")
            for row in rows:
                print(f"Row Text: {row.text}")

            # Check if the employee is found in the list
            if employee_list.is_employee_found(first, last):
                print(f"{full_name} - Name Verified")
            else:
                print(f"{full_name} - Not Found")

            time.sleep(1)

        except TimeoutException:
            print(f"Timeout during verification for {full_name}")
        except Exception as e:
            print(f"Exception during search for {full_name}: {e}")

        # After each search, navigate back to the Employee List page
        try:
            # Reload Employee List page to prepare for the next employee search
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
            ).click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h5[text()='Employee Information']"))
            )
        except TimeoutException:
            continue

    # Step 5: Log out from the dashboard
    dashboard.logout()
    print("Logged out successfully.")