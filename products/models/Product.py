from app import db
import random
from classes.abstract import Repository


class ProductModel(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    price = db.Column(db.Integer())
    pieces_left = db.Column(db.Integer())
    category = db.Column(db.String())
    specifications = db.Column(db.JSON())
    box_dimensions = db.Column(db.String())
    weight = db.Column(db.SmallInteger())
    img_paths = db.Column(db.Text())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Product {self.name}>"


class ProductModelRepository(Repository):

    model = ProductModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """
    @staticmethod
    def create_id() -> int:

        max_int = 9223372036854775807
        max_len = 19

        rand_int = str(random.randrange(1, max_int))

        free_units = '1' * (max_len - len(rand_int))

        # to always maintain the same length
        unique_id = int(free_units + rand_int)

        #  if a product with the same id is found, then rerun function

        if ProductModelRepository.model.query.get(unique_id):
            ProductModelRepository.create_id()
        else:
            return unique_id
        return 0
