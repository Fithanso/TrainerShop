from app import db


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
