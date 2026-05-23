"""
Cart and checkout flow tests for SauceDemo
Covers: cart contents, checkout form validation, order completion
"""
import pytest
from playwright.sync_api import Page, expect


class TestCart:

    def test_cart_page_opens(self, logged_in_page: Page):
        """Cart icon navigates to the cart page."""
        logged_in_page.locator(".shopping_cart_link").click()
        expect(logged_in_page).to_have_url("https://www.saucedemo.com/cart.html")

    def test_cart_shows_added_item(self, logged_in_page: Page):
        """Item added from inventory appears in cart."""
        item_name = logged_in_page.locator(".inventory_item_name").first.text_content()
        logged_in_page.locator(".btn_inventory").first.click()
        logged_in_page.locator(".shopping_cart_link").click()

        cart_item = logged_in_page.locator(".cart_item_label").first
        expect(cart_item).to_contain_text(item_name)

    def test_remove_item_from_cart(self, logged_in_page: Page):
        """Item can be removed from the cart page."""
        logged_in_page.locator(".btn_inventory").first.click()
        logged_in_page.locator(".shopping_cart_link").click()

        logged_in_page.locator("[data-test*='remove']").first.click()
        expect(logged_in_page.locator(".cart_item")).not_to_be_visible()

    def test_continue_shopping_returns_to_inventory(self, logged_in_page: Page):
        """Continue Shopping button returns user to the inventory page."""
        logged_in_page.locator(".shopping_cart_link").click()
        logged_in_page.locator("[data-test='continue-shopping']").click()

        expect(logged_in_page).to_have_url("https://www.saucedemo.com/inventory.html")


class TestCheckout:

    def _add_item_and_go_to_checkout(self, page: Page):
        """Helper: add one item and navigate to checkout step one."""
        page.locator(".btn_inventory").first.click()
        page.locator(".shopping_cart_link").click()
        page.locator("[data-test='checkout']").click()

    def test_checkout_step_one_loads(self, logged_in_page: Page):
        """Checkout page one loads after clicking Checkout."""
        self._add_item_and_go_to_checkout(logged_in_page)
        expect(logged_in_page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
        expect(logged_in_page.locator(".title")).to_have_text("Checkout: Your Information")

    def test_checkout_requires_first_name(self, logged_in_page: Page):
        """Checkout shows error when first name is missing."""
        self._add_item_and_go_to_checkout(logged_in_page)
        logged_in_page.locator("[data-test='continue']").click()

        error = logged_in_page.locator("[data-test='error']")
        expect(error).to_contain_text("First Name is required")

    def test_checkout_requires_last_name(self, logged_in_page: Page):
        """Checkout shows error when last name is missing."""
        self._add_item_and_go_to_checkout(logged_in_page)
        logged_in_page.locator("[data-test='firstName']").fill("Mehul")
        logged_in_page.locator("[data-test='continue']").click()

        error = logged_in_page.locator("[data-test='error']")
        expect(error).to_contain_text("Last Name is required")

    def test_checkout_requires_postal_code(self, logged_in_page: Page):
        """Checkout shows error when postal code is missing."""
        self._add_item_and_go_to_checkout(logged_in_page)
        logged_in_page.locator("[data-test='firstName']").fill("Mehul")
        logged_in_page.locator("[data-test='lastName']").fill("Jethva")
        logged_in_page.locator("[data-test='continue']").click()

        error = logged_in_page.locator("[data-test='error']")
        expect(error).to_contain_text("Postal Code is required")

    def test_complete_checkout_flow(self, logged_in_page: Page):
        """Full happy path: add item → checkout → confirm order."""
        self._add_item_and_go_to_checkout(logged_in_page)

        # Step 1: Fill in customer details
        logged_in_page.locator("[data-test='firstName']").fill("Mehul")
        logged_in_page.locator("[data-test='lastName']").fill("Jethva")
        logged_in_page.locator("[data-test='postalCode']").fill("M5V 3A8")
        logged_in_page.locator("[data-test='continue']").click()

        # Step 2: Review order summary
        expect(logged_in_page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
        expect(logged_in_page.locator(".cart_item")).to_be_visible()

        # Step 3: Finish order
        logged_in_page.locator("[data-test='finish']").click()
        expect(logged_in_page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
        expect(logged_in_page.locator(".complete-header")).to_have_text("Thank you for your order!")
