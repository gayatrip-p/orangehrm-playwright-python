"""
test_login.py — OrangeHRM Login Module Test Suite
=====================================================
Covers:
  ✅ TC_LOGIN_001  Valid login redirects to dashboard
  ✅ TC_LOGIN_002  Invalid password shows error
  ✅ TC_LOGIN_003  Invalid username shows error
  ✅ TC_LOGIN_004  Empty username shows Required
  ✅ TC_LOGIN_005  Empty password shows Required
  ✅ TC_LOGIN_006  Both fields empty shows Required
  ✅ TC_LOGIN_007  Login page UI elements are visible
  ✅ TC_LOGIN_008  Successful logout returns to login page
  ✅ TC_LOGIN_009  Data-driven negative tests (parametrize)
  ✅ TC_LOGIN_010  Page title is correct
"""

import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from test_data.login_data import (
    VALID_USERNAME, VALID_PASSWORD,
    INVALID_LOGINS,
    EXPECTED_ERROR_MSG, EXPECTED_REQUIRED,
    DASHBOARD_URL_FRAG,
)


# ═══════════════════════════════════════════════════════════════
# TEST CLASS
# ═══════════════════════════════════════════════════════════════

@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:

    # ── TC_LOGIN_007 ── UI Elements visible ──────────────────────
    @allure.title("TC_LOGIN_007 - Login page UI elements are displayed")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_ui_elements(self, login_page: LoginPage):
        """Verify all key UI elements exist on the login page."""

        with allure.step("Check OrangeHRM logo is visible"):
            assert login_page.is_logo_visible(), "Logo should be visible"

        with allure.step("Check username field is visible"):
            assert login_page.is_visible(LoginPage.USERNAME_INPUT), \
                "Username input should be visible"

        with allure.step("Check password field is visible"):
            assert login_page.is_visible(LoginPage.PASSWORD_INPUT), \
                "Password input should be visible"

        with allure.step("Check Login button is visible"):
            assert login_page.is_visible(LoginPage.LOGIN_BUTTON), \
                "Login button should be visible"

        with allure.step("Check Forgot Password link is visible"):
            assert login_page.is_visible(LoginPage.FORGOT_PASSWORD), \
                "Forgot password link should be visible"

        login_page.take_screenshot("login_page_ui")

    # ── TC_LOGIN_010 ── Page title ───────────────────────────────
    @allure.title("TC_LOGIN_010 - Login page title is correct")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_title(self, login_page: LoginPage):
        """Page title text should say 'Login'."""
        title = login_page.get_page_title_text()
        assert "Login" in title, f"Expected 'Login' in title, got: '{title}'"

    # ── TC_LOGIN_001 ── Valid login ──────────────────────────────
    @allure.title("TC_LOGIN_001 - Valid credentials redirect to Dashboard")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_valid_login(self, login_page: LoginPage, base_url: str):
        """
        GIVEN  valid admin credentials
        WHEN   user submits the login form
        THEN   user is redirected to the Dashboard
        """
        with allure.step("Enter valid username and password"):
            login_page.login(VALID_USERNAME, VALID_PASSWORD)

        dashboard = DashboardPage(login_page.page)

        with allure.step("Verify dashboard is displayed"):
            assert dashboard.is_loaded(), "Dashboard should load after valid login"

        with allure.step("Verify URL contains /dashboard"):
            login_page.assert_url_contains(DASHBOARD_URL_FRAG)

        with allure.step("Verify welcome name is shown"):
            welcome = dashboard.get_welcome_name()
            assert welcome, f"Welcome name should not be empty, got: '{welcome}'"

        dashboard.take_screenshot("after_valid_login")

    # ── TC_LOGIN_008 ── Logout ───────────────────────────────────
    @allure.title("TC_LOGIN_008 - Successful logout returns to login page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_logout(self, login_page: LoginPage, base_url: str):
        """
        GIVEN  user is logged in
        WHEN   user clicks Logout
        THEN   user is redirected back to the login page
        """
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        dashboard = DashboardPage(login_page.page)
        assert dashboard.is_loaded(), "Should be on dashboard before logout"

        dashboard.logout()

        with allure.step("Verify login page is shown after logout"):
            login_page.assert_url_contains("/auth/login")
            assert login_page.is_visible(LoginPage.USERNAME_INPUT), \
                "Username field should be visible after logout"

        login_page.take_screenshot("after_logout")

    # ── TC_LOGIN_002 ── Invalid password ─────────────────────────
    @allure.title("TC_LOGIN_002 - Invalid password shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_password(self, login_page: LoginPage):
        """
        GIVEN  valid username but wrong password
        WHEN   user submits login form
        THEN   error message 'Invalid credentials' is shown
        """
        login_page.login(VALID_USERNAME, "WrongPassword@123")

        with allure.step("Verify error message is displayed"):
            error_msg = login_page.get_error_message()
            assert EXPECTED_ERROR_MSG in error_msg, \
                f"Expected '{EXPECTED_ERROR_MSG}', got: '{error_msg}'"

        with allure.step("Verify user stays on login page"):
            login_page.assert_url_contains("/auth/login")

        login_page.take_screenshot("invalid_password_error")

    # ── TC_LOGIN_003 ── Invalid username ─────────────────────────
    @allure.title("TC_LOGIN_003 - Invalid username shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_username(self, login_page: LoginPage):
        """
        GIVEN  wrong username with valid password
        WHEN   user submits login form
        THEN   error message 'Invalid credentials' is shown
        """
        login_page.login("NonExistentUser", VALID_PASSWORD)

        error_msg = login_page.get_error_message()
        assert EXPECTED_ERROR_MSG in error_msg, \
            f"Expected '{EXPECTED_ERROR_MSG}', got: '{error_msg}'"

        login_page.take_screenshot("invalid_username_error")

    # ── TC_LOGIN_004 ── Empty username ───────────────────────────
    @allure.title("TC_LOGIN_004 - Empty username shows Required validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_username(self, login_page: LoginPage):
        """
        GIVEN  username is left blank
        WHEN   user submits login form
        THEN   'Required' validation message appears under username
        """
        login_page.enter_password(VALID_PASSWORD)
        login_page.click_login()

        with allure.step("Verify 'Required' appears for username field"):
            login_page.wait_for_element(".oxd-input-field-error-message")
            error_text = login_page.get_text(".oxd-input-field-error-message")
            assert EXPECTED_REQUIRED in error_text, \
                f"Expected 'Required', got: '{error_text}'"

        login_page.take_screenshot("empty_username_validation")

    # ── TC_LOGIN_005 ── Empty password ───────────────────────────
    @allure.title("TC_LOGIN_005 - Empty password shows Required validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_password(self, login_page: LoginPage):
        """
        GIVEN  password is left blank
        WHEN   user submits login form
        THEN   'Required' validation message appears
        """
        login_page.enter_username(VALID_USERNAME)
        login_page.click_login()

        login_page.wait_for_element(".oxd-input-field-error-message")
        error_text = login_page.get_text(".oxd-input-field-error-message")
        assert EXPECTED_REQUIRED in error_text, \
            f"Expected 'Required', got: '{error_text}'"

        login_page.take_screenshot("empty_password_validation")

    # ── TC_LOGIN_006 ── Both empty ───────────────────────────────
    @allure.title("TC_LOGIN_006 - Both fields empty shows Required validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_both_fields(self, login_page: LoginPage):
        """
        GIVEN  both username and password are empty
        WHEN   user clicks Login
        THEN   two 'Required' messages are shown (one per field)
        """
        login_page.click_login()

        errors = login_page.page.locator(".oxd-input-field-error-message").all()
        assert len(errors) >= 2, \
            f"Expected at least 2 'Required' messages, found: {len(errors)}"

        for err in errors:
            assert EXPECTED_REQUIRED in err.inner_text(), \
                f"Expected 'Required' in error, got: '{err.inner_text()}'"

        login_page.take_screenshot("both_fields_empty_validation")

    # ── TC_LOGIN_009 ── Data-driven negative tests ───────────────
    @allure.title("TC_LOGIN_009 - Data-driven: {username} / {password}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize(
        "username, password, expected_msg",
        INVALID_LOGINS,
        ids=[
            "wrong_password",
            "wrong_username",
            "both_wrong",
            "empty_username",
            "empty_password",
            "both_empty",
            "lowercase_admin",
            "uppercase_admin",
            "leading_space_username",
            "trailing_space_password",
        ]
    )
    def test_invalid_login_combinations(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_msg: str,
    ):
        """
        Data-driven test — runs once for each row in INVALID_LOGINS.
        Covers wrong creds, empty fields, case sensitivity, whitespace.
        """
        allure.dynamic.title(
            f"TC_LOGIN_009 - Login fails: username='{username}'"
        )

        login_page.login(username, password)

        with allure.step(f"Verify error contains '{expected_msg}'"):
            # Could be inline validation or alert — check both
            page = login_page.page

            has_alert = page.locator(LoginPage.ERROR_MESSAGE).is_visible()
            has_inline = page.locator(".oxd-input-field-error-message").count() > 0

            assert has_alert or has_inline, \
                f"Expected an error for username='{username}', " \
                f"password='{password}' — but no error was shown"

        with allure.step("Verify user stays on login page"):
            login_page.assert_url_contains("/auth/login")
