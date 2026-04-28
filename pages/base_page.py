"""
BasePage: Parent class for all Page Objects.
Contains reusable methods used across all pages.
"""

from playwright.sync_api import Page, expect
import allure


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ── Navigation ──────────────────────────────────────────────
    def navigate(self, url: str):
        """Navigate to a given URL."""
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    def get_title(self) -> str:
        """Return current page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return current page URL."""
        return self.page.url

    # ── Actions ──────────────────────────────────────────────────
    def click(self, locator: str):
        """Click an element."""
        with allure.step(f"Click: {locator}"):
            self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
        """Clear and type into an input field."""
        with allure.step(f"Fill '{value}' into {locator}"):
            self.page.locator(locator).clear()
            self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        """Get visible text of an element."""
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator: str) -> bool:
        """Check if an element is visible on page."""
        return self.page.locator(locator).is_visible()

    # ── Waits ─────────────────────────────────────────────────────
    def wait_for_element(self, locator: str, timeout: int = 10000):
        """Wait until an element is visible."""
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)

    def wait_for_url(self, url_fragment: str, timeout: int = 10000):
        """Wait until URL contains a specific fragment."""
        self.page.wait_for_url(f"**{url_fragment}**", timeout=timeout)

    # ── Assertions ───────────────────────────────────────────────
    def assert_url_contains(self, fragment: str):
        """Assert current URL contains a given string."""
        expect(self.page).to_have_url(f"**{fragment}**")

    def assert_element_visible(self, locator: str):
        """Assert element is visible."""
        expect(self.page.locator(locator)).to_be_visible()

    def assert_text_equals(self, locator: str, expected: str):
        """Assert element text matches expected value."""
        expect(self.page.locator(locator)).to_have_text(expected)

    # ── Screenshot ───────────────────────────────────────────────
    def take_screenshot(self, name: str = "screenshot"):
        """Take a screenshot and attach to Allure report."""
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
