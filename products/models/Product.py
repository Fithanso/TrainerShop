from app import app, db
from classes.abstract import Repository
import json
import random
import os


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
    characteristics = db.Column(db.JSON())
    box_dimensions = db.Column(db.String())
    weight = db.Column(db.SmallInteger())
    img_names = db.Column(db.Text())
    creation_date = db.Column(db.DateTime())
    last_edited = db.Column(db.DateTime())

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

    @staticmethod
    def prepare_list(entities, chunks, max_chars):
        """Method takes Product entities and make them ready to be displayed"""

        # split all products into chunks of certain length - n. It is needed to display them in rows of n elements
        products_list = [entities[i:i + chunks] for i in range(0, len(entities), chunks)]

        # prepare icons for all loaded products (1 per product), crop descriptions to max chars possible
        for product in entities:
            filenames = json.loads(product.img_names)
            description = product.description[0:max_chars]

            if len(product.description) > max_chars:
                description += '...'

            if len(filenames) != 0:
                # i add a system separator to make a path absolute,
                # otherwise it'll search a 'static' folder inside products
                setattr(product, 'icon_path', os.path.sep + os.path.join(app.config['UPLOAD_FOLDER'], filenames[0]))

            setattr(product, 'description', description)

        return products_list
