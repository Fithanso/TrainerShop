from application import db

from classes.abstract import Repository

from constants import BIGINT_LEN, BIGINT_MAX

from sqlalchemy.orm import relationship
import random


class CharacteristicModel(db.Model):
    __tablename__ = 'characteristic'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.BigInteger(), db.ForeignKey('category.id'))
    type = db.Column(db.String())
    category = relationship("CategoryModel", back_populates="characteristics")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Characteristic {self.__dict__}>"


class CharacteristicModelRepository(Repository):

    model = CharacteristicModel

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

        #  if a category with the same id is found, then rerun function

        if CharacteristicModelRepository.model.query.get(unique_id):
            CharacteristicModelRepository.create_id()
        else:
            return unique_id
        return 0

