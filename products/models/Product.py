from application import db
from classes.abstract import Repository

from global_settings.models.GlobalSetting import GlobalSettingModelRepository

from constants import BIGINT_MAX, BIGINT_LEN
from helpers import to_int_if_fractional_zero

from sqlalchemy.orm import relationship

import json
import random
import os


class ProductModel(db.Model):
    __searchable__ = ['name', 'description']
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    price = db.Column(db.Numeric(10, 4))
    pieces_left = db.Column(db.Integer())
    category = db.Column(db.String(), db.ForeignKey('category.short_name'))
    characteristics = db.Column(db.Text())
    box_dimensions = db.Column(db.String())
    box_weight = db.Column(db.SmallInteger())
    img_names = db.Column(db.Text())
    creation_date = db.Column(db.DateTime())
    last_edited = db.Column(db.DateTime())
    category_object = relationship("CategoryModel", back_populates="products")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Product {self.__dict__}>"


class ProductModelRepository(Repository):

    model = ProductModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """
    @staticmethod
    def create_id() -> int:

        max_int = BIGINT_MAX
        max_len = BIGINT_LEN

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

    def prepare_list(self, entities, chunks, max_chars, upload_path):
        """Method takes Product entities and makes them ready to be displayed. List of entities is split
        into chunks, additional information about each is loaded"""

        # split all products into chunks of certain length - n. It is needed to display them in rows of n elements
        products_list = self.split_entities_into_chunks(entities, chunks)

        # prepare icons for all loaded products (1 per product), crop descriptions to max chars possible
        for product in entities:
            filenames = json.loads(product.img_names)
            description = self.create_product_description(product, max_chars)

            setattr(product, 'description', description)

            product.price = to_int_if_fractional_zero(product.price)

            if len(filenames) != 0:
                # i add a system separator to make a path absolute,
                # otherwise it'll search a 'static' folder inside products
                setattr(product, 'icon_path', self.get_upload_path_with_filename(upload_path, filenames[0]))

        return products_list

    def split_entities_into_chunks(self, entities, chunks):
        return [entities[i:i + chunks] for i in range(0, len(entities), chunks)]


    def create_product_description(self, product, max_chars):
        description = product.description[0:max_chars]

        if len(product.description) > max_chars:
            description += '...'

        return description

    def get_upload_path_with_filename(self, upload_path, filename):
        return os.path.sep + os.path.join(upload_path, filename)
