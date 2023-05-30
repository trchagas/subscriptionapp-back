from flask import request, make_response, g
from models.Client import Client

from validator.UpdateClient import validate_UpdateClient

from config import db


class ClientController:
    def index():
        data = request.args
        if data:
            data = {k: v for k, v in data.items() if v != ""}
        auth_user = g.current_user
        client = auth_user.client
        if data.get('validation'):
            return {
                'name':
                client.name,
            }
        elif data.get('filterData'):
            return {'created_at': str(client.created_at)}
        else:
            retData = client.serialize
            retData['email'] = auth_user.email
            return retData

    def update(id):
        auth_user = g.current_user
        client = Client.query.get(id)

        if not client or client.user_id != auth_user.id:
            return make_response({'message': 'Não autorizado.'}), 401

        data = request.get_json()
        if data:
            data = {
                k: None if v == "" else v
                for k, v in data.items() if k not in
                ['email']
            }

        errors = validate_UpdateClient(data)
        if errors:
            return make_response(errors), 400

        client = Client.query.filter_by(user_id=id)
        try:
            client.update(dict(data))
            db.session.commit()
            client = client.first()  # updated client
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
        return client.serialize
