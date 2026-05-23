"""
Login tests for SauceDemo (https://www.saucedemo.com)
Covers: valid login, invalid credentials, locked user, empty fields
"""
import pytest
from playwright.sync_api import Page, expect


class TestLogin:

    def test_valid_login(self, page: Page):
        """Standard user can log in successfully."""
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(page.locator(".title")).to_have_text("Products")

    def test_invalid_password(self, page: Page):
        """Wrong password shows error message."""
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("wrong_password")
        page.locator("#login-button").click()

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Username and password do not match")

    def test_invalid_username(self, page: Page):
        """Unknown username shows error message."""
        page.locator("#user-name").fill("unknown_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Username and password do not match")

    def test_locked_out_user(self, page: Page):
        """Locked user sees specific locked-out error."""
        page.locator("#user-name").fill("locked_out_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Sorry, this user has been locked out")

    def test_empty_username(self, page: Page):
        """Submitting without username shows validation error."""
        page.locator("#login-button").click()

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Username is required")

    def test_empty_password(self, page: Page):
        """Submitting without password shows validation error."""
        page.locator("#user-name").fill("standard_user")
        page.locator("#login-button").click()

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Password is required")

    def test_logout(self, logged_in_page: Page):
        """Logged-in user can log out successfully."""
        logged_in_page.locator("#react-burger-menu-btn").click()
        logged_in_page.locator("#logout_sidebar_link").click()

        expect(logged_in_page).to_have_url("https://www.saucedemo.com/")
        expect(logged_in_page.locator("#login-button")).to_be_visible()
