import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList, ShoppingCart, Producto
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route("/user/<int:user_id>/product/<int:product_id>/quantity/<int:quantity>/add_shopping_cart", methods=["GET", "POST"])
@jwt_required()
def add_item_to_shopping_cart(user_id, product_id, quantity):
   
    user = User.query.filter_by(id=user_id).first() #Obtener el user id de url
    product = Producto.query.filter_by(id=product_id).first() #Obtener el product id de url
    

    product_to_add_shopping_cart = ShoppingCart(user_id=user.id, productId=product.id,product_price=product.precio, product_quantity=quantity)
    db.session.add(product_to_add_shopping_cart)
    db.session.commit()
    return jsonify("Hello")

@app.route("/user/<int:user_id>/view_cart")
@jwt_required()
def display_shopping_cart_by_user_id(user_id):
    product_in_shopping_cart = ShoppingCart.query.filter_by(user_id=user_id).all()
    product_in_shopping_cart_serialized = list(map(lambda product: product.serialize(),product_in_shopping_cart))


    return jsonify(product_in_shopping_cart_serialized)
