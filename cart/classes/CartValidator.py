from cart import funcs
from helpers import *


class CartValidator:

    def __init__(self):
        self.cart_valid = False
        self.logged_in_customer = None

        if customer_logged():
            self.logged_in_customer = funcs.get_logged_in_customer()

    def validate_cart_with_product(self, product_id):

        if self.logged_in_customer:
            if all((self.validate_logged_customers_cart(), self.check_if_product_in_customers_cart(product_id))):
                return True
        else:
            if self.check_if_product_in_session_cart(product_id):
                return True

        return False

    def validate_logged_customers_cart(self):
        """Method checks if customer's cart is not None and if it's a dictionary"""
        return funcs.customers_cart_is_valid(self.logged_in_customer)

    def check_if_product_in_customers_cart(self, product_id):
        return funcs.product_exists_in_customers_cart(self.logged_in_customer, product_id)

    @staticmethod
    def check_if_product_in_session_cart(product_id):
        return funcs.product_exists_in_session_cart(product_id)

