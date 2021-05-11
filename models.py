from app import db, migrate


class ClientModel(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    login = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    patronymic = db.Column(db.String())
    birthday = db.Column(db.Date())
    delivery_address = db.Column(db.String())
    last_visit = db.Column(db.DateTime())
    register_date = db.Column(db.DateTime())
    active_cart = db.Column(db.String())
    orders = db.Column(db.String())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Client {self.email}>"


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

