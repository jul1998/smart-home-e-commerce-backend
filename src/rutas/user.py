import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    print(body)
    # print(body['username'])
    address = "ninguno"
    try:
        if body is None:
            raise APIException(
                "Body está vacío o email no viene en el body, es inválido", status_code=400)
        if body['email'] is None or body['email'] == "":
            raise APIException("email es inválido", status_code=400)
        if body['password'] is None or body['password'] == "":
            raise APIException("password es inválido", status_code=400)
        if body['phone'] is None or body['phone'] == "":
            raise APIException("password es inválido", status_code=400)
        if body['name'] is None or body['name'] == "":
            raise APIException("password es inválido", status_code=400)
        if body['address'] is None or body['address'] == "":
            raise APIException("password es inválido", status_code=400)
        

        password = bcrypt.generate_password_hash(
            body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True, estado="Active", name=body['name'], img_profile=None, phone=body['phone'], address=body['address'])



        print(new_user)
        # print(new_user.serialize())
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg":"Usuario creado exitosamente"}), 200

    except Exception as err:
        db.session.rollback()
        user = User.query.filter_by(email=body['email'])
        if user:
            raise APIException("El usuario ya existe", status_code=400)
        print(err)
        raise APIException({"Error al registrar usuario"}, status_code=400)


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user is None:
        raise APIException("usuario no existe", status_code=401)

    # validamos el password si el usuario existe y si coincide con el de la BD
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException("usuario o password no coinciden", status_code=401)

    access_token = create_access_token(identity=user.id) 
    return jsonify({"token": access_token, "email": user.email, "message": f"Welcome, {user.name.split(' ')[0]}"}), 200

@app.route('/payment', methods=['POST'])
@jwt_required
def payment():
    body = request.get_json()
    

@app.route('/helloprotected', methods=['get'])  # endpoint
@jwt_required()  # decorador que protege al endpoint
def hello_protected():  # definición de la función
    #claims = get_jwt()
    # imprimiendo la identidad del usuario que es el id
    print("id del usuario:", get_jwt_identity())
    # búsqueda del id del usuario en la BD
    user = User.query.get(get_jwt_identity())

    # get_jwt() regresa un diccionario, y una propiedad importante es jti
    jti = get_jwt()["jti"]

    tokenBlocked = BlockedList.query.filter_by(token=jti).first()
    # cuando hay coincidencia tokenBloked es instancia de la clase TokenBlockedList
    # cuando No hay coincidencia tokenBlocked = None

    if isinstance(tokenBlocked, BlockedList):
        return jsonify(msg="Acceso Denegado")

    response_body = {
        "isToken": "token válido",
        "user_id": user.id,  # get_jwt_identity(),
        "user_email": user.email,
    }

    return jsonify(response_body), 200


@app.route('/logout', methods=['get'])  # endpoint
@jwt_required()
def logout():
    print(get_jwt())
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)

    tokenBlocked = BlockedList(token=jti, created_at=now)
    db.session.add(tokenBlocked)
    db.session.commit()

    return jsonify({"message": "token eliminado"})


@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user == None:
        raise APIException("El usuario no existe", status_code=400)
    # print(user.serialize())
    return jsonify(user.serialize()), 200

@app.route('/user/carritoCompras', methods=['GET'])
#@jwt_required()
def get_carritoCompras():
    carrito_producto = CarritoCompras.query.all()
    carrito_producto = list(map( lambda carrito_producto: carrito_producto.serialize(), carrito_productos))
    carrito_completo = carrito_producto
    print(carrito_completo)
    return jsonify(carrito_completo), 200

@app.route("/user/<int:user_id>/change_password", methods=["GET","PUT"])
@jwt_required()
def change_password(user_id):
    """Ruta para cambiar password"""
    body = request.get_json()
    password_request = body["password"]
    if request.method == "PUT":
        hash_password = bcrypt.generate_password_hash(
                password_request, 10).decode("utf-8") #Crear nueva password encriptada

        password_to_change = User.query.filter_by(id=user_id).first() #Obtener usuario por user_id en url
        password_to_change.password = hash_password # Cambiar actual password
        db.session.commit() #Commit cambios
        return redirect (url_for("logout"))# Redireccionar a ruta de logout para agregar token a blocked list
    return jsonify("None")


@app.route("/user/<int:user_id>/settings", methods=["GET","PUT"])
@jwt_required()
def display_settings(user_id):
    body = request.get_json()
    print(body["img"])

    if body is None:
        raise APIException(
                "Body está vacío o email no viene en el body, es inválido", status_code=400)
    if body['email'] is None or body['email'] == "":
        raise APIException("email es inválido", status_code=400)
    if body['phone'] is None or body['phone'] == "":
        raise APIException("phone es inválido", status_code=400)
    if body['name'] is None or body['name'] == "":
        raise APIException("name es inválido", status_code=400)
    if body['address'] is None or body['address'] == "":
        raise APIException("address es inválido", status_code=400)

    user_to_update = User.query.get(user_id)
    user_to_update.email = body["email"]
    user_to_update.phone = body["phone"]
    user_to_update.name = body["name"]
    user_to_update.address = body["address"]
    user_to_update.img_profile = body["img"]
    db.session.commit()

    return jsonify("Settings were changed successfuly"), 200