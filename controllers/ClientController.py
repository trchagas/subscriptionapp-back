from flask import request, make_response, jsonify, g
from werkzeug.security import check_password_hash
from models.User import User
from models.Client import Client
from models.Role import Role
from models.RoleUser import RoleUser

from config import SECRET_KEY, db
from helpers.UserHelper import UserHelper

from validator.ClientUser import validate_ClientUser

import json


class ClientController:
    def store():
        clientData = json.loads(request.data.decode("utf-8"))

        clientData = request.get_json()
        if clientData:
            clientData = {k: v for k, v in clientData.items() if v != ""}

        userData = {
            'email': clientData.pop('email'),
            'password': clientData.pop('password'),
        }

        role = Role.query.filter_by(slug='client').first()
        if not role:
            return make_response(
                {'message':
                 "A role 'client' não está cadastada no sistema."}), 500
        try:

            # insert user first
            user = User(userData.get('email'), userData.get('password'))
            db.session.add(user)
            db.session.commit()
            # add client
            clientData['user_id'] = user.id
            client = Client(clientData)
            db.session.add(client)
            # add role_user
            db.session.add(RoleUser(role.id, user.id))
            db.session.commit()
            return client.serialize
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
