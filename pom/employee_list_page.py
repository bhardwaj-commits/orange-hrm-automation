from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class EmployeeListPage:
    # Locators for different elements on the Employee List page
    EMPLOYEE_NAME_SEARCH = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    EMPLOYEE_LIST = (By.CSS_SELECTOR, ".oxd-table.orangehrm-employee-list")
    EMPLOYEE_TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table.orangehrm-employee-list .oxd-table-row")
    NO_RECORDS_MESSAGE = (By.XPATH, "//span[text()='No Records Found']")

    def __init__(self, driver):
        self.driver = driver

    def send_keys(self, locator, text):
        """ Clears the field and sends keys to it. """
        print(f"Preparing to enter text into field: {text}")
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

        # Clear the input field using JavaScript and the clear method
        self.driver.execute_script("arguments[0].value = '';", element)
        element.clear()
        element.click()

        # Attempt to blur the field by clicking on the label, ensuring input is ready
        try:
            label = self.driver.find_element(By.XPATH, "//label[text()='Employee Name']")
            label.click()  # Click on the label to blur the input field
        except:
            pass

        # Ensure the field is empty before sending new text
        WebDriverWait(self.driver, 5).until(
            lambda d: d.find_element(*locator).get_attribute("value") == ""
        )

        # Send the provided text to the input field
        element.send_keys(text)
        time.sleep(0.5)

    def search_employee(self, full_name):
        """ Search for an employee using their full name. """
        print(f"Searching for employee: {full_name}")

        # Wait for the Employee Information page to be visible
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//h5[text()='Employee Information']"))
        )

        # Use the send_keys method to clear and enter the full name
        self.send_keys(self.EMPLOYEE_NAME_SEARCH, full_name)
        print(f"Entered full name: {full_name}")

        # Click the Search button
        try:
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            )
            search_button.click()
            print("Search button clicked.")
        except TimeoutException:
            print("Timeout: Search button not clickable.")
            self.driver.save_screenshot(f"search_button_timeout_{full_name.replace(' ', '_')}.png")
            raise

        # Wait for the employee table to load or for the "No Records Found" message to appear
        try:
            WebDriverWait(self.driver, 20).until(lambda d: (
                d.find_elements(*self.EMPLOYEE_TABLE_ROWS) or
                "No Records Found" in d.page_source
            ))
            print("Employee list updated.")
        except TimeoutException:
            print("Timeout: Employee table did not update.")
            self.driver.save_screenshot(f"search_timeout_{full_name.replace(' ', '_')}.png")
            raise

        # Check for the "No Records Found" message
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.NO_RECORDS_MESSAGE)
            )
            print(f"No records found for: {full_name}")
        except TimeoutException:
            print("Employee(s) found.")

        # Debugging: Print the table rows to check the data displayed
        try:
            rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
            print("Table Rows:")
            for row in rows:
                print(row.text)
        except Exception as e:
            print(f"Error retrieving table content: {e}")

    def is_employee_found(self, first_name, last_name):
        """ Verifies if the employee exists in the table rows. """
        print(f"Verifying presence of employee: {first_name} {last_name}")
        try:
            # Wait for the table rows to be visible
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(self.EMPLOYEE_TABLE_ROWS)
            )
            
            # Check if the employee is present in any of the rows
            rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
            for row in rows:
                text = row.text.lower()
                if first_name.lower() in text and last_name.lower() in text:
                    print(f"Found employee {first_name} {last_name} in row: {text}")
                    return True
            print(f"Employee {first_name} {last_name} not found in listed results.")
            return False
        except TimeoutException:
            print("Timeout: Table rows did not load in time.")
            self.driver.save_screenshot(f"employee_search_timeout_{first_name}_{last_name}.png")
            return False
        except Exception as e:
            print(f"Error checking employee presence: {e}")
            return False