from flask import request, make_response, g

from models.Admin import Admin
from config import db
from validator.UpdateAdmin import validate_UpdateAdmin


class AdminController:
    def index():
        auth_user = g.current_user
        data = request.get_json()
        if data:
            data = {k: v for k, v in data.items() if v != ""}

        admin = auth_user.admin.serialize

        if data and data.get('validation'):
            return {
                'admin': {
                    'name': admin['name']
                },
                
            }
        else:
            return {
                'admin': admin,
                
                'email': auth_user.email
            }

    def update(id):
        admin = Admin.query.filter_by(user_id=id)
        if not admin:
            return make_response({
                'message':
                'O usuário com este identificador não existe ou não é um administrador.'
            }), 400
        data = request.get_json()
        if data:
            data = {k: None if v == "" else v for k, v in data.items()}

        errors = validate_UpdateAdmin(data)
        if errors:
            return make_response(errors), 400

        try:
            admin.update(dict(data))
            db.session.commit()
            admin = admin.first()  # updated admin
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

        return admin.serialize
