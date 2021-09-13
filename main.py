from app import app
import view
from products.blueprint import products
from account.blueprint import account
from admin_panel.blueprint import admin_panel
from categories.blueprint import categories
from characteristics.blueprint import characteristics

app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin_panel, url_prefix='/admin')
app.register_blueprint(characteristics, url_prefix='/characteristics')

if __name__ == '__main__':
    app.run(debug=True)


# TODO:
#  сделать отображение и добавление товаров, валидация validate on submit логина и сигнапа
#  по поводу формы добавления: надо сделать так, чтобы в выбор подгружались категории. это можно динамически добавлять:
#  https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectField . - СДЕЛАНО!!!
#  но надо потом подгружать спексы из этой категории. https://www.youtube.com/watch?v=I2dJuNwlIH0
#  https://stackoverflow.com/questions/39640024/create-dynamic-fields-in-wtform-in-flask


