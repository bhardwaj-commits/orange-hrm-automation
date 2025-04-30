
from selenium.webdriver.common.by import By
from pom.base_page import BasePage

class DashboardPage(BasePage):
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    USER_DROPDOWN = (By.CLASS_NAME, 'oxd-userdropdown-icon')
    LOGOUT_BUTTON = (By.LINK_TEXT, 'Logout')

    def go_to_pim(self):
        self.click(self.PIM_MENU)

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_BUTTON)
