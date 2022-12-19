import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import Producto, User, PreguntasProductos
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/product/<product_id>/user/<user_id>/questions", methods=["POST"])
@jwt_required()
def post_product_question(product_id, user_id):
    """Ruta para postear preguntas con base en el method"""
    body = request.get_json()
    now = datetime.now(timezone.utc)
    
    user = User.query.filter_by(id=user_id).first() #Obtener el user id de url
    product = Producto.query.filter_by(id=product_id).first() #Obtener el product id de url
    print(user)
    ask_by_userid_body = user_id
    productId_body = product_id
    descripcion_body = body["description"]
    posted_at_body = now
    estado_body = "Pending"

    if descripcion_body == "" or len(descripcion_body) == 0:
        return APIException("Description is empty", status_code=400)


    new_question = PreguntasProductos(ask_by_userid=user.id, 
    productId=product.id,
    descripcion=descripcion_body, 
    posted_at=now,estado=estado_body)

    db.session.add(new_question)
    db.session.commit()
    return jsonify({"msg":"Question posted successfuly"}),200
    

@app.route("/product/<product_id>/questions")
def get_questions(product_id):
    """Ruta para obtener preguntas filtrado por productId"""

    question_query = PreguntasProductos.query.filter_by(productId=product_id).all() #Obtener todas las preguntas de un producto por id
    #questions = PreguntasProductos.query.all()
    questions_json = list(map(lambda question: question.serialize(),question_query))#Map over questions in product
    print(questions_json)
    return jsonify(questions_json)

@app.route("/preguntasAdmin") #route para ver todas las preguntas hechas y poder responderlas.
@jwt_required() #Solo admins pueden ver todas las preguntas
def get_allquestions(): 
    questions = PreguntasProductos.queryAll()
    questions_json = list(map(lambda question: question.serialize(),questions))
    return jsonify(questions_json)