from flask import request, make_response, jsonify, g
from werkzeug.security import check_password_hash
from models.User import User

from config import SECRET_KEY
from helpers.UserHelper import UserHelper

from validator.SessionUser import validate_SessionUser


class SessionController:
    def create():
        post_data = request.get_json()
        if post_data:
            post_data = {k: v for k, v in post_data.items() if v != ""}

        errors = validate_SessionUser(post_data)
        if errors:
            return make_response(errors), 400

        try:
            user = User.query.filter_by(email=post_data.get('email')).first()
            if user and check_password_hash(user.password,
                                            post_data.get('password')):
                auth_token = user.encode_auth_token(user.id, SECRET_KEY)
                if auth_token:
                    responseObject = {
                        'user': {
                            'user_id': user.id,
                            'created_at': user.created_at,
                            'updated_at': user.updated_at,
                            'token': auth_token.decode(),
                        },
                        'roles': UserHelper.getRoles(user)
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                return make_response({
                    'message':
                    'Credenciais inválidas. Por favor, verifique e-mail e senha e tente novamente.'
                }), 400

        except Exception as e:
            print(e)
            return make_response({
                'message':
                'Ocorreu um erro ao efetuar o login. Por favor, tente novamente.'
            }), 500

    def validate():
        user = g.current_user
        if not user:
            return make_response({
                'message':
                'Não é possível verificar roles. Usuário inválido.'
            }), 400

        slugFromRequest = request.path.split('/')[1]
        roles = UserHelper.getRoles(user)
        if slugFromRequest not in roles:
            return make_response({'message':
                                  'Token ou endpoint inválido.'}), 400
        return make_response(), 200
