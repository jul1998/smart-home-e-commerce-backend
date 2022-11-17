import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import Producto, User, Compras
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/<int:user_id>/order_history")
@jwt_required()
def get_order_history(user_id):
    print(get_jwt_identity())
    body = request.get_json()
    user_body = body["user_body"]

    orders_from_user = Compras.query.filter_by(userId=user_id).first()
    print(orders_from_user)

    if not orders_from_user:
        return jsonify("No hay historial de ordenes")
    else:
        return jsonify(orders_from_user)




