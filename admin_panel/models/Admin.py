from application import db
from classes.abstract import Repository


class AdminModel(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    login = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    last_visit = db.Column(db.DateTime())
    clearance_level = db.Column(db.SmallInteger)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Admin {self.__dict__}>"


class AdminModelRepository(Repository):

    model = AdminModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    First part of id is random. Second - number of seconds since 1970
    """
    @staticmethod
    def create_id() -> int:
        pass
