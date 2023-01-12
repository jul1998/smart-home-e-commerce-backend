import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import Producto, User,Comments
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/product/<int:product_id>/user/<int:user_id>/post_comment", methods=["POST"])
@jwt_required()
def post_comment(product_id,user_id):
    body = request.get_json()
    comment_body = body["comment"]
    now = datetime.now(timezone.utc)
    print(body)

    product = Producto.query.filter_by(id=product_id).first()
    if not product:
        raise APIException("Product does not exist", status_code=400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise APIException("User does not exits", status_code=400)
    try:
        new_comment = Comments(posted_by_userid=user.id, productId=product.id, posted_at=now, comment=comment_body)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"message":"Comment was posted successfully"})
    except:
        db.session.rollback()
        raise APIException("Something went wrong...", status_code=400)

@app.route("/product/<int:product_id>/get_comments")
def get_comments(product_id):

    comments_query = Comments.query.filter_by(productId=product_id).all()
    if comments_query == []:
        raise APIException("There are no questions for this product", status_code=404)

        
    comments_serialized = list(map(lambda comment: comment.serialize(), comments_query))

    return jsonify(comments_serialized)
    