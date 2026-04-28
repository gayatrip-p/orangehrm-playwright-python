"""
LoginPage: Page Object for OrangeHRM Login page.
URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
"""

from pages.base_page import BasePage
from playwright.sync_api import Page
import allure


class LoginPage(BasePage):

    # ── Locators ─────────────────────────────────────────────────
    USERNAME_INPUT   = "input[name='username']"
    PASSWORD_INPUT   = "input[name='password']"
    LOGIN_BUTTON     = "button[type='submit']"
    ERROR_MESSAGE    = ".oxd-alert-content-text"
    FORGOT_PASSWORD  = "//p[text()='Forgot your password? ']"
    LOGO             = ".orangehrm-login-logo"
    PAGE_TITLE       = ".orangehrm-login-title"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Actions ──────────────────────────────────────────────────
    @allure.step("Open login page")
    def open(self, base_url: str):
        """Navigate to the login page."""
        self.navigate(f"{base_url}/web/index.php/auth/login")
        self.wait_for_element(self.USERNAME_INPUT)

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        self.fill(self.USERNAME_INPUT, username)

    @allure.step("Enter password")
    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)

    @allure.step("Click Login button")
    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("Login with username='{username}'")
    def login(self, username: str, password: str):
        """Full login flow in one call."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Getters ──────────────────────────────────────────────────
    def get_error_message(self) -> str:
        """Return the error alert text shown on failed login."""
        self.wait_for_element(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def is_logo_visible(self) -> bool:
        return self.is_visible(self.LOGO)

    def get_page_title_text(self) -> str:
        return self.get_text(self.PAGE_TITLE)
