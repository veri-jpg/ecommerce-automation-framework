import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.payment_page import PaymentPage
from pages.product_page import ProductsPage


@pytest.mark.smoke
def test_checkout_flow_places_order_successfully(page, api_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(api_user["email"], api_user["password"])

    products_page = ProductsPage(page)
    products_page.navigate()
    products_page.add_product_to_cart(index=0)
    products_page.go_to_cart_from_modal()

    cart_page = CartPage(page)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.add_order_comment("Please deliver in the morning.")
    checkout_page.place_order()

    payment_page = PaymentPage(page)
    payment_page.pay(
        name_on_card="Test User",
        card_number="4111111111111111",
        cvc="123",
        expiry_month="12",
        expiry_year="2030",
    )
    payment_page.expect_order_confirmed()
