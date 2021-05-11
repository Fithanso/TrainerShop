from app import app
import view
from products.blueprint import products
from account.blueprint import account

app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(account, url_prefix='/account')

if __name__ == '__main__':
    app.run(debug=True)


