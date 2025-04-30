
from selenium.webdriver.common.by import By
from pom.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    def open(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
