"""
Inventory / product listing tests for SauceDemo
Covers: product display, sorting, add to cart, cart badge
"""
import pytest
from playwright.sync_api import Page, expect


class TestInventory:

    def test_products_page_loads(self, logged_in_page: Page):
        """Inventory page displays products after login."""
        products = logged_in_page.locator(".inventory_item")
        expect(products).to_have_count(6)

    def test_product_names_visible(self, logged_in_page: Page):
        """All product names are visible on the page."""
        names = logged_in_page.locator(".inventory_item_name")
        expect(names).to_have_count(6)
        for name in names.all():
            expect(name).to_be_visible()

    def test_sort_by_price_low_to_high(self, logged_in_page: Page):
        """Products can be sorted by price low to high."""
        logged_in_page.locator("[data-test='product-sort-container']").select_option("lohi")

        prices = logged_in_page.locator(".inventory_item_price").all_text_contents()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric), f"Prices not sorted: {numeric}"

    def test_sort_by_price_high_to_low(self, logged_in_page: Page):
        """Products can be sorted by price high to low."""
        logged_in_page.locator("[data-test='product-sort-container']").select_option("hilo")

        prices = logged_in_page.locator(".inventory_item_price").all_text_contents()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric, reverse=True), f"Prices not sorted: {numeric}"

    def test_sort_by_name_a_to_z(self, logged_in_page: Page):
        """Products can be sorted alphabetically A-Z."""
        logged_in_page.locator("[data-test='product-sort-container']").select_option("az")

        names = logged_in_page.locator(".inventory_item_name").all_text_contents()
        assert names == sorted(names), f"Names not sorted A-Z: {names}"

    def test_add_single_item_to_cart(self, logged_in_page: Page):
        """Adding one item updates the cart badge to 1."""
        logged_in_page.locator(".btn_inventory").first.click()

        badge = logged_in_page.locator(".shopping_cart_badge")
        expect(badge).to_have_text("1")

    def test_add_multiple_items_to_cart(self, logged_in_page: Page):
        """Adding multiple items increments the cart badge correctly."""
        buttons = logged_in_page.locator(".btn_inventory").all()
        for i, btn in enumerate(buttons[:3]):
            btn.click()
            expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text(str(i + 1))

    def test_remove_item_from_inventory(self, logged_in_page: Page):
        """Item can be removed directly from inventory page."""
        logged_in_page.locator(".btn_inventory").first.click()
        expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")

        logged_in_page.locator("[data-test*='remove']").first.click()
        expect(logged_in_page.locator(".shopping_cart_badge")).not_to_be_visible()

    def test_product_detail_page(self, logged_in_page: Page):
        """Clicking a product name opens the product detail page."""
        first_name = logged_in_page.locator(".inventory_item_name").first.text_content()
        logged_in_page.locator(".inventory_item_name").first.click()

        expect(logged_in_page.locator(".inventory_details_name")).to_have_text(first_name)
        expect(logged_in_page.locator(".inventory_details_price")).to_be_visible()
