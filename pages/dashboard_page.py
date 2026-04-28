"""
DashboardPage: Page Object for OrangeHRM Dashboard.
Reached after successful login.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page
import allure


class DashboardPage(BasePage):

    # ── Locators ─────────────────────────────────────────────────
    DASHBOARD_HEADER    = "//h6[text()='Dashboard']"
    USER_DROPDOWN       = ".oxd-userdropdown-tab"
    LOGOUT_OPTION       = "//a[text()='Logout']"
    SIDE_MENU           = ".oxd-sidepanel"
    QUICK_LAUNCH        = ".orangehrm-quick-launch"
    WELCOME_MESSAGE     = ".oxd-userdropdown-name"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Verifications ────────────────────────────────────────────
    @allure.step("Verify dashboard is loaded")
    def is_loaded(self) -> bool:
        """Returns True when the Dashboard header is visible."""
        try:
            self.wait_for_element(self.DASHBOARD_HEADER, timeout=15000)
            return True
        except Exception:
            return False

    def get_welcome_name(self) -> str:
        """Return the logged-in user's display name."""
        return self.get_text(self.WELCOME_MESSAGE)

    # ── Actions ──────────────────────────────────────────────────
    @allure.step("Logout from application")
    def logout(self):
        """Click user dropdown → Logout."""
        self.click(self.USER_DROPDOWN)
        self.wait_for_element(self.LOGOUT_OPTION)
        self.click(self.LOGOUT_OPTION)
        self.wait_for_url("/auth/login")
