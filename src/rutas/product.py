import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import Producto, User, FavoritoProductos, Reviews, ProductDescription
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/producto", methods=["POST"])
#@jwt_required()
def create_product():
    product_img = None
    body = request.get_json() 
    product_name = body["name"]
    product_stock = body["stock"]
    product_precio = body["precio"]
    product_estado = body["estado"]
 


    if body is None:
        raise APIException("Body cannot be empty")
    if product_name == "":
         raise APIException("Product name cannot be empty")
    if product_stock == "" or not product_stock.isdigit(): #isdigit() es un metodo para verificar si input es interger(True) o string(False)
         raise APIException("Product stock cannot be empty nor text")
    if product_precio == "":
         raise APIException("Product price cannot be empty nor text")
    if product_estado == "":
         raise APIException("Product estado cannot be empty")
    if body["img"] != "" or body["img"] is None:
        product_img = body["img"]

    #Si todo lo de arriba se cumple, se pasa a la siguiente parte de verificacion usando un try-excep-else block

    try: 
        new_product = Producto(name=product_name,
                    stock=product_stock,
                    precio=product_precio,
                    estado=product_estado,
                    img_product = product_img

        )
        db.session.add(new_product)
    except Exception:
        db.session.rollback()
        raise APIException("Error during process", status_code=401)
    else:
        db.session.commit()
        return jsonify({"msg":"Product added successfuly"}),200


@app.route("/products_list")
def get_product_list():
    all_products = Producto.query.all()
    all_products_list = list(map(lambda product: product.serialize(), all_products))
    return jsonify(all_products_list)

@app.route("/user/<int:user_id>/add_to_favorite/product/<int:product_id>", methods=["POST"])
#@jwt_required()
def add_to_favorite_list(user_id,product_id):
    """Ruta para obtener lista de productos favoritos """
    user = User.query.filter_by(id=user_id).first() #Obtener el user id de url
    product = Producto.query.filter_by(id=product_id).first() #Obtener el product id de url
    print(user.name, product.id)

    #favorite = FavoritoProductos.query.filter_by(userId=user_id).first()
    #print(favorite.product.precio)

    try:
        add_favorite = FavoritoProductos(userId=user.id, productId=product.id) #Agregar a db
        db.session.add(add_favorite)
        
    except Exception:
        db.session.rollback()
        msg = { #El msg que el usuario puede ver 
            "user": user.name,
            "product": product.id,
            "success": False
        }
        return jsonify(msg),400

    else:
        db.session.commit() #Commit
        msg = { #El msg que el usuario puede ver 
            "user": user.name,
            "product": product.id,
            "success": True
        }
        return jsonify(msg),200


@app.route("/user/<int:user_id>/favorite_product/<int:product_id>")
def get_favorite_product(user_id, product_id):
    pass

@app.route("/product/<int:product_id>/product_info")
def get_product_info_by_id(product_id):
    product = Producto.query.get(product_id)
    #product_reviews = Reviews.query.get(product_id).serialize()
    
    return jsonify(product.serialize())

@app.route("/product/<int:product_id>/add_description", methods=["GET", "POST"])
def add_product_description(product_id):
    if request.method == "POST":
        body = request.get_json()
        product_description_request = body["description"]
        product = Producto.query.filter_by(id=product_id).first()
        if body == None or product_description_request == "":
            raise APIException("Body cannot be empty")
        
        
        new_description = ProductDescription(description=product_description_request, product_id=product.id)
        db.session.add(new_description)
        db.session.commit()
        return jsonify({"msg":"Description added"}),200
    else:
        #description = ProductDescription.query.get(product_id).serialize()["description"]
        all_descriptions = ProductDescription.query.filter_by(product_id=product_id).all()

        all_descriptions_serilized = list(map(lambda description: description.serialize(), all_descriptions))
        print(all_descriptions_serilized)
        return jsonify(all_descriptions_serilized),200