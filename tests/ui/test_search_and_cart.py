import pytest

from pages.cart_page import CartPage
from pages.product_page import ProductsPage


@pytest.mark.regression
def test_search_product_and_add_to_cart_updates_cart_count(page):
    products_page = ProductsPage(page)
    products_page.navigate()
    products_page.search("Dress")
    products_page.expect_search_results_visible()

    products_page.add_product_to_cart(index=0)
    products_page.go_to_cart_from_modal()

    cart_page = CartPage(page)
    assert cart_page.get_item_count() == 1
    assert len(cart_page.get_item_names()) == 1
