from app import db, SMALLINT_LEN, SMALLINT_MAX
from classes.abstract import Repository
import random


class ShipmentMethodModel(db.Model):
    __tablename__ = 'shipment_method'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.SmallInteger, primary_key=True)
    cost = db.Column(db.Integer())
    estimated_time = db.Column(db.SmallInteger())
    name = db.Column(db.Text())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Product {self.name}>"


class ShipmentMethodModelRepository(Repository):

    model = ShipmentMethodModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """
    @staticmethod
    def create_id() -> int:

        max_int = SMALLINT_MAX
        max_len = SMALLINT_LEN

        rand_int = str(random.randrange(1, max_int))

        # to always maintain the same length
        free_units = '1' * (max_len - len(rand_int))

        unique_id = int(free_units + rand_int)

        #  if a category with the same id is found, then rerun function

        if ShipmentMethodModelRepository.model.query.get(unique_id):
            ShipmentMethodModelRepository.create_id()
        else:
            return unique_id
        return 0
