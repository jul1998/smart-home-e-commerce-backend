import os
from flask_admin import Admin
from .db import db


### Importar los modelos #####
from src.modelos import User, Producto, FavoritoProductos, ShoppingCart, AdminUser, Compras, Reviews, Problemas, PreguntasProductos, BlockedList, ProductDescription, ShoppingCartItem, Comments



from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Producto, db.session))
    admin.add_view(ModelView(Compras, db.session))
    admin.add_view(ModelView(FavoritoProductos, db.session))
    admin.add_view(ModelView(PreguntasProductos, db.session))
    admin.add_view(ModelView(AdminUser, db.session))
    admin.add_view(ModelView(BlockedList, db.session))
    admin.add_view(ModelView(ProductDescription, db.session))
    admin.add_view(ModelView(ShoppingCart, db.session))
    admin.add_view(ModelView(ShoppingCartItem, db.session))
    admin.add_view(ModelView(Comments, db.session))

