"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .db import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

# Setup de Bcrypt
bcrypt = Bcrypt(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#####  Importar Modelos  ####
from src.modelos import User, Producto, FavoritoProductos, ShoppingCart, AdminUser, Compras, Reviews, Problemas, PreguntasProductos, BlockedList, ProductDescription, ShoppingCartItem, Comments

##### Importar las Rutas ####
from src.rutas import signup, login, hello_protected, logout, get_user_by_id, get_carritoCompras, change_password, signupAdmin, loginAdmin, send_email, display_settings, get_favorite_product, delete_account_by_id, get_product_info_by_id, add_product_description, delete_question_by_id, get_carritoCompras_2, add_item_to_shopping_cart, detelete_product_shopping_cart, display_shopping_cart_by_user_id, detelete_all_products_shopping_cart, display_specific_product_in_cart, modify_quantity_in_shopping_cart, post_comment



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=False)
