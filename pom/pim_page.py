from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pom.base_page import BasePage

class PIMPage(BasePage):
    # Locators for elements on the PIM page
    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[contains(@class, 'oxd-button') and contains(., 'Add')]")
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    PIM_PAGE_HEADER = (By.XPATH, "//h6[text()='PIM']")
    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading-spinner")

    def add_employee(self, first_name, last_name):
        """ Adds an employee with the given first and last name. """
        print("Waiting for PIM page to load...")

        # Wait for the PIM page header to be visible
        try:
            WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.PIM_PAGE_HEADER))
            print("PIM page header is visible.")
        except TimeoutException:
            print("PIM page header did not load in time.")
            self.driver.save_screenshot("pim_page_timeout_error.png")
            raise

        # Wait for the loading spinner to disappear
        try:
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(self.LOADING_SPINNER))
            print("Loading spinner disappeared.")
        except TimeoutException:
            print("Loading spinner did not disappear in time.")
            self.driver.save_screenshot("loading_spinner_timeout.png")
            raise

        # Click the "Add Employee" button
        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON))
            add_employee_button = self.driver.find_element(*self.ADD_EMPLOYEE_BUTTON)
            add_employee_button.click()
            print("Clicked on 'Add Employee' button.")
        except TimeoutException:
            print("Failed to find or click the 'Add Employee' button.")
            self.driver.save_screenshot("add_employee_button_timeout_error.png")
            raise

        # Wait for the First Name input field to become visible and enter the first name
        try:
            WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.FIRST_NAME))
            self.send_keys(self.FIRST_NAME, first_name)
            print(f"Entered first name: {first_name}")
        except TimeoutException:
            print("First Name input field did not become visible in time.")
            self.driver.save_screenshot("first_name_timeout_error.png")
            raise

        # Wait for the Last Name input field to become visible and enter the last name
        try:
            WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.LAST_NAME))
            self.send_keys(self.LAST_NAME, last_name)
            print(f"Entered last name: {last_name}")
        except TimeoutException:
            print("Last Name input field did not become visible in time.")
            self.driver.save_screenshot("last_name_timeout_error.png")
            raise

        # Optionally fill the Employee ID field if it's visible
        try:
            emp_id_input = self.driver.find_element(By.XPATH, "//label[text()='Employee Id']/following::input[1]")
            emp_id_input.clear()
            emp_id_input.send_keys(f"{first_name[:2]}{last_name[:2]}{len(first_name)}")
            print("Filled custom Employee ID.")
        except Exception:
            print("Employee ID field not found. Continuing without it.")

        # Click the Save button to save the employee information
        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(self.SAVE_BUTTON))
            self.click(self.SAVE_BUTTON)
            print("Clicked the 'Save' button.")
            self.driver.save_screenshot(f"after_save_{first_name}_{last_name}.png")
        except TimeoutException:
            print("Save button did not become clickable.")
            self.driver.save_screenshot("save_button_timeout_error.png")
            raise

        # Wait for the Personal Details page to be visible, confirming successful employee creation
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[text()='Personal Details']"))
            )
            print("Employee saved successfully.")
        except TimeoutException:
            print("Did not reach Personal Details page. Possibly a validation error.")
            self.driver.save_screenshot(f"failed_personal_details_{first_name}_{last_name}.png")
