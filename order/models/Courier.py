from application import db


class CourierModel(db.Model):
    __tablename__ = 'courier'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    patronymic = db.Column(db.String())

    def __repr__(self):
        return f"<Courier {self.__dict__}>"
