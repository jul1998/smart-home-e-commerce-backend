import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, Producto, Ticket
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route("/create_ticket", methods=["GET", "POST"])
@jwt_required()
def create_ticket():
    body = request.get_json()
    user_id = body["user_id"]
    description = body["description"]
    now = datetime.now(timezone.utc)

    if description is None or description=="":
        raise APIException("Tickets cannot be empty" ,status_code=400)

    try:
        new_ticket = Ticket(user_id=user_id, description=description, posted_at=now)
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({"message": "Ticket was created"})
    except:
        db.session.rollback()
        raise APIException("Something went wrong...")

    
@app.route("/user/<int:user_id>/display_ticket_information")
@jwt_required()
def display_ticket_info_by_user(user_id):

    all_tickets = Ticket.query.filter_by(user_id=user_id).all()
    if not all_tickets:
        raise APIException("User does not have any ticket yet", status_code=400)

    all_tickets_serialized = list(map(lambda ticket: ticket.serialize(), all_tickets))

    print(all_tickets)
    return jsonify(all_tickets_serialized)