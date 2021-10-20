from app import db, INT_LEN, INT_MAX
import random
from classes.abstract import Repository


class CategoryModel(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    short_name = db.Column(db.String())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Category {self.short_name}>"


class CategoryModelRepository(Repository):

    model = CategoryModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """
    @staticmethod
    def create_id() -> int:

        max_int = INT_MAX
        max_len = INT_LEN

        rand_int = str(random.randrange(1, max_int))

        free_units = '1' * (max_len - len(rand_int))

        # to always maintain the same length
        unique_id = int(free_units + rand_int)

        #  if a category with the same id is found, then rerun function

        if CategoryModelRepository.model.query.get(unique_id):
            CategoryModelRepository.create_id()
        else:
            return unique_id
        return 0

