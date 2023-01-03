import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList, ShoppingCart, Producto, ShoppingCartItem
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route("/user/<int:user_id>/add_shopping_cart", methods=["GET", "POST"])
@jwt_required()
def add_item_to_shopping_cart(user_id):
    body = request.get_json()
    product_id = body["product_id"]
    quantity = body["quantity"]

    user = User.query.filter_by(id=user_id).first() #Obtener el user id de url
    product = Producto.query.filter_by(id=product_id).first() #Obtener el product id de url

    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 

    if not cart_entry:
        try:
            product_to_add_shopping_cart = ShoppingCart(user_id=user.id)
            db.session.add(product_to_add_shopping_cart)
            db.session.commit()
            return jsonify({"message":"Product added to shopping cart!"}),200
        except:
            db.session.rollback()
            raise APIException("Something went wrong when adding product to shopping cart", status_code=400)
    cart_item = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id, productId=product_id).first()
    if cart_item:
        #Send a message saying that product was already added
        return jsonify({"message":"Product was already added to cart"}),403
    else:
        try:
            product_to_add_shopping_cart_item = ShoppingCartItem(shopping_cart_id=cart_entry.id,productId=product.id,product_price=product.precio, product_quantity=quantity)
            db.session.add(product_to_add_shopping_cart_item)
            db.session.commit()
            return jsonify({"message":"Product added to shopping cart"}),200
        except:
            db.session.rollback()
            raise APIException("Something went wrong when adding product to shopping cart", status_code=400)



    

@app.route("/user/<int:user_id>/view_cart")
@jwt_required()
def display_shopping_cart_by_user_id(user_id):
    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 

    product_in_shopping_cart_item = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id).all()
    product_in_shopping_cart_serialized = list(map(lambda product: product.serialize(),product_in_shopping_cart_item))

    return jsonify(product_in_shopping_cart_serialized)

@app.route("/user/<int:user_id>/find_product_in_cart")
@jwt_required()
def display_specific_product_in_cart(user_id):
    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 

    product_in_shopping_cart_item = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id).first()

    return jsonify(product_in_shopping_cart_item.serialize())

@app.route("/delete/user/<int:user_id>/shopping_cart", methods=["DELETE"])
@jwt_required()
def detelete_product_shopping_cart(user_id):
    body = request.get_json()
    product_id = body["product_id"]
    
    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 

    if not cart_entry:
        raise APIException("Product does not exist in shopping cart from user")

    product_to_delete = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id, productId=product_id).first()
    if not product_to_delete:
        raise APIException("Product does not exist in shopping cart from user")

    
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return jsonify({"message":"Product deleted from shoppping cart"})
    except:
        db.session.rollback()
        raise APIException("Something went wrong when adding product to shopping cart", status_code=400)

    

@app.route("/delete/user/<int:user_id>/all_shopping_cart", methods=["DELETE"])
@jwt_required()
def detelete_all_products_shopping_cart(user_id):
    body = request.get_json()
    product_id = body["product_id"]

    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 
    if not cart_entry:
        raise APIException("Product does not exist in shopping cart from user")

    product_to_delete = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id, productId=product_id).first()
    if not product_to_delete:
        raise APIException("Product does not exist in shopping cart from user")

    
    try:
        ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id).delete()
        db.session.commit()
        return jsonify({"message":"Products deleted from shoppping cart"})
    except:
        db.session.rollback()
        raise APIException("Something went wrong when adding product to shopping cart", status_code=400)

