import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import Producto
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/producto", methods=["POST"])
def create_product():
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

    #Si todo lo de arriba se cumple, se pasa a la siguiente parte de verificacion usando un try-excep-else block

    try: 
        new_product = Producto(name=product_name,
                    stock=product_stock,
                    precio=product_precio,
                    estado=product_estado
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