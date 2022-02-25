
from cart.classes.CartStrategyFactories import AddToCartFactory
from cart.classes.AddToCart import AddToCart

from cart import funcs

from helpers import customer_logged


class AddToCartManager:

    PRODUCT_ALREADY_IN_CART = 'in_cart'
    OK = 'ok'

    def __init__(self, product_id):
        self.logged_in_customer = None
        self.status = AddToCartManager.PRODUCT_ALREADY_IN_CART
        self.to_cart_adder = None
        self._strategy = None
        self._strategy_factory = AddToCartFactory()
        self.product_id = product_id

        if customer_logged():
            self.logged_in_customer = funcs.get_logged_in_customer()

    def add_product_return_status(self):

        if self.logged_in_customer and funcs.product_exists_in_customers_cart(self.logged_in_customer, self.product_id)\
                or funcs.product_exists_in_session_cart(self.product_id):
            self.status = AddToCartManager.PRODUCT_ALREADY_IN_CART
        else:
            self.choose_strategy()
            self.to_cart_adder = AddToCart(self._strategy)
            self.to_cart_adder.add_product(self.product_id)
            self.status = AddToCartManager.OK

        return self.status

    def choose_strategy(self):
        if self.logged_in_customer:
            strategy = self._strategy_factory.create_customer_strategy(self.logged_in_customer)
        else:
            session_cart_dict = funcs.get_session_cart_or_none()
            strategy = self._strategy_factory.create_session_strategy(session_cart_dict)

        self.set_strategy(strategy)

    def set_strategy(self, strategy):
        self._strategy = strategy

