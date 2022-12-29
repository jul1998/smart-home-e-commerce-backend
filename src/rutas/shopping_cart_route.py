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

        
    if ShoppingCart.query.filter_by(productId=product_id).first():
        raise APIException("Product was already added to shopping cart", status_code=403)
    
    try:
        product_to_add_shopping_cart = ShoppingCart(user_id=user.id, productId=product.id,product_price=product.precio, product_quantity=quantity)
        db.session.add(product_to_add_shopping_cart)
        db.session.commit()
        return jsonify({"msg":"Product added to shopping cart!"}),200
    except:
        db.session.rollback()
        raise APIException("Something went wrong when adding product to shopping cart", status_code=400)

    

@app.route("/user/<int:user_id>/view_cart")
@jwt_required()
def display_shopping_cart_by_user_id(user_id):
    product_in_shopping_cart = ShoppingCart.query.filter_by(user_id=user_id).all()
    product_in_shopping_cart_serialized = list(map(lambda product: product.serialize(),product_in_shopping_cart))

    return jsonify(product_in_shopping_cart_serialized)

@app.route("/delete/product/<int:product_id>/user/<int:user_id>/shopping_cart", methods=["DELETE"])
def detelete_product_shopping_cart(product_id,user_id):

    if not ShoppingCart.query.filter_by(productId=product_id).first():
        raise APIException("Product does not exist in shopping cart from user")
    

        
    ShoppingCart.query.filter_by(productId=product_id).delete()
    db.session.commit()
    
    print(ShoppingCart.query.filter_by(productId=product_id).first())
    return jsonify({"msg":"Product deleted from shoppping cart"})
