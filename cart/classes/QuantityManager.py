from cart.classes.CartStrategyFactories import *
from cart.classes.ChangeQuantityInCart import *

from products.models.Product import ProductModel

from cart import funcs

from helpers import customer_logged


class QuantityManager:

    QUANTITY_EXCEEDS_PIECES_LEFT = 'exceeds'
    QUANTITY_IS_NULL = 'null'
    INVALID_OPERATION = 'invalid_operation'
    OK = 'ok'

    def __init__(self, change_mode, product_id):
        if change_mode not in [ChangeQuantityInCart.INCREASE, ChangeQuantityInCart.DECREASE]:
            raise ValueError("Invalid change mode!")

        self._change_mode = change_mode
        self.product_id = product_id
        self.quantity_changer = None
        self._strategy = None
        self._strategy_factory = None
        self.status = QuantityManager.OK

    def change_quantity_return_status(self):
        """Method changes quantity of a product in cart if there are enough pieces in stock. It returns status codes
        for blueprint's views for correct further operations"""

        self.choose_strategy_factory()

        self.choose_strategy()

        self.quantity_changer = ChangeQuantityInCart(self._strategy)

        products_quantities = funcs.get_products_quantities_dict()
        product_entity = ProductModel.query.get(self.product_id)

        if self._change_mode == ChangeQuantityInCart.INCREASE:
            self.increase_quantity_set_status(products_quantities, product_entity)

        elif self._change_mode == ChangeQuantityInCart.DECREASE:
            self.decrease_quantity_set_status()

        return self.status

    def choose_strategy_factory(self):
        strategy_factory = None

        if self._change_mode == ChangeQuantityInCart.INCREASE:
            strategy_factory = IncreaseStrategyFactory()
        elif self._change_mode == ChangeQuantityInCart.DECREASE:
            strategy_factory = DecreaseStrategyFactory()

        self._strategy_factory = strategy_factory

    def choose_strategy(self):
        """Method decides what strategy to use"""

        if customer_logged():
            customer_entity = funcs.get_logged_in_customer()
            strategy = self._strategy_factory.create_customer_strategy(customer_entity)

        else:
            session_cart_dict = funcs.get_session_cart_or_none()
            strategy = self._strategy_factory.create_session_strategy(session_cart_dict)

        self.set_strategy(strategy)

    def increase_quantity_set_status(self, products_quantities, product_entity):

        if self.pieces_left_are_enough(products_quantities, product_entity):
            self.quantity_changer.change_quantity(self.product_id)
        else:
            self.status = QuantityManager.QUANTITY_EXCEEDS_PIECES_LEFT

    def decrease_quantity_set_status(self):
        new_quantity = self.quantity_changer.change_quantity(self.product_id)

        if new_quantity == 0:
            self.status = QuantityManager.QUANTITY_IS_NULL

    def set_strategy(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy

    def pieces_left_are_enough(self, products_quantities, product_entity):
        if int(products_quantities[self.product_id]) < int(product_entity.pieces_left):
            return True

        return False



