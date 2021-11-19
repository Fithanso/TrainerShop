from app import db, BIGINT_LEN, BIGINT_MAX
import time
import random
from classes.abstract import Repository


class CustomerModel(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    login = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    patronymic = db.Column(db.String())
    birthday = db.Column(db.Date())
    delivery_address = db.Column(db.String())
    last_visit = db.Column(db.DateTime())
    register_date = db.Column(db.DateTime())
    phone_number = db.Column(db.String())
    active_cart = db.Column(db.String())
    orders = db.Column(db.Text())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Customer {self.email}>"


class CustomerModelRepository(Repository):

    model = CustomerModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """
    @staticmethod
    def create_id() -> int:

        max_int = BIGINT_MAX
        max_len = BIGINT_LEN

        rand_int = str(random.randrange(1, max_int))

        # to always maintain the same length
        free_units = '1' * (max_len - len(rand_int))

        unique_id = int(free_units + rand_int)

        #  if a user with the same id is found, then rerun function
        if CustomerModelRepository.model.query.get(unique_id):
            CustomerModelRepository.create_id()
        else:
            return unique_id
        return 0
