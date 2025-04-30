
import pytest
from pom.login_page import LoginPage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.login("Admin", "admin123")
