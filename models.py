from app import db, migrate


class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Integer())
    pieces_left = db.Column(db.Integer())
    category = db.Column(db.String())
    specifications = db.Column(db.String())
    box_dimensions = db.Column(db.String())
    weight = db.Column(db.SmallInteger())
    img_paths = db.Column(db.String())

    def __init__(self, **kwargs):
        super(ProductModel).__init__(**kwargs)

    def __repr__(self):
        return f"<Product {self.name}>"


class TestModel(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.BigInteger, primary_key=True)
    login = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def __repr__(self):
        return f"<Client {self.login}>"

