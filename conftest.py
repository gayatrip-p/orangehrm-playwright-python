"""
conftest.py: Shared pytest fixtures used across all test files.
Playwright browser and page setup lives here.
"""

import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser, BrowserContext
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Load environment variables from .env
load_dotenv()


# ── Config helpers ────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")

@pytest.fixture(scope="session")
def admin_credentials() -> dict:
    return {
        "username": os.getenv("ADMIN_USERNAME", "Admin"),
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
    }


# ── Browser fixtures ──────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context — set viewport and ignore HTTPS errors."""
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos/",
    }


# ── Page-level fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Return a fresh LoginPage and navigate to login URL."""
    lp = LoginPage(page)
    lp.open(base_url)
    return lp


@pytest.fixture
def logged_in_page(page: Page, base_url: str, admin_credentials: dict):
    """
    Pre-authenticated fixture.
    Use this when a test needs to START on the dashboard
    without repeating the login steps.
    """
    lp = LoginPage(page)
    lp.open(base_url)
    lp.login(admin_credentials["username"], admin_credentials["password"])

    dp = DashboardPage(page)
    dp.is_loaded()          # wait for dashboard to fully render
    return page             # return the page so the test can build any POM


# ── Hooks ─────────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to report on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot(full_page=True)
            import allure
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
