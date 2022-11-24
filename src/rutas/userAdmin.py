import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import AdminUser, User, BlockedList
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route('/signupAdmin', methods=['POST'])
def signupAmin():
    body = request.get_json()
    # print(body['username'])
    
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
        

        password = bcrypt.generate_password_hash(
            body['password'], 12).decode("utf-8")

        new_user_admin = AdminUser(email=body['email'], password=password, is_active=True, estado="Active", name=body['name'], phone=body['phone'])
        
        user_admin = AdminUser.query.filter_by(email=body['email'])
        if not user_admin:
            raise APIException("El usuario ya existe", status_code=400)

  
        # print(new_user.serialize())
        db.session.add(new_user_admin)
        db.session.commit()
        return jsonify({"mensaje": "Usuario admin creado exitosamente"}), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500


@app.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = AdminUser.query.filter_by(email=email).first()

    if user is None:
        raise APIException("usuario no existe", status_code=401)

    # validamos el password si el usuario existe y si coincide con el de la BD
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException("usuario o password no coinciden", status_code=401)

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "email": user.email}), 200


@app.route('/helloprotected', methods=['get'])  # endpoint
@jwt_required()  # decorador que protege al endpoint
def hello_protectedAdmin():  # definición de la función
    #claims = get_jwt()
    # imprimiendo la identidad del usuario que es el id
    print("id del usuario:", get_jwt_identity())
    # búsqueda del id del usuario en la BD
    user = AdminUser.query.get(get_jwt_identity())

    # get_jwt() regresa un diccionario, y una propiedad importante es jti
    jti = get_jwt()["jti"]

    #tokenBlocked = TokenBlockedList.query.filter_by(token=jti).first()
    # cuando hay coincidencia tokenBloked es instancia de la clase TokenBlockedList
    # cuando No hay coincidencia tokenBlocked = None

    # if isinstance(tokenBlocked, TokenBlockedList):
    #    return jsonify(msg="Acceso Denegado")

    response_body = {
        "message": "token válido",
        "user_id": user.id,  # get_jwt_identity(),
        "user_email": user.email
    }

    return jsonify(response_body), 200

@app.route('/lista-usuarios', methods=['get'])
@jwt_required()
def allUsers():
    users = User.query.all()  # Objeto de SQLAlchemy
    users = list(map(lambda item: item.serialize(), users))

    response_body = {
        "lista": users
    }
    return jsonify(response_body), 200

@app.route('/lista-usuarios-admin', methods=['get'])
@jwt_required()
def allUsersAdmin():
    users = AdminUser.query.all()  # Objeto de SQLAlchemy
    users = list(map(lambda item: item.serialize(), users))

    response_body = {
        "lista": users
    }
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_idAdmin(user_id):
    user = User.query.get(user_id)
    if user == None:
        raise APIException("El usuario no existe", status_code=400)
    # print(user.serialize())
    return jsonify(user.serialize()), 200


@app.route("/user/<int:user_id>/change_password", methods=["GET","PUT"])
@jwt_required()
def change_passwordAdmin(user_id):
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




