import jwt
from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from werkzeug.security import generate_password_hash
from flask import request, make_response, g

from models.RoleUser import RoleUser
from models.Role import Role

from config import SECRET_KEY, db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    roles = db.relationship('RoleUser',
                            backref=db.backref('user', lazy='joined'),
                            lazy='select')

    admin = db.relationship('Admin',
                            uselist=False,
                            lazy='select',
                            backref=db.backref('user', lazy='joined'))

    client = db.relationship('Client',
                             uselist=False,
                             lazy='select',
                             backref=db.backref('user', lazy='joined'))

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def encode_auth_token(self, user_id, secret_key):
        try:
            payload = {'iat': datetime.utcnow(), 'sub': user_id}

            return jwt.encode(payload, secret_key, algorithm='HS256')
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(self, auth_token, secret_key):
        try:
            payload = jwt.decode(auth_token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Assinatura de token expirada. Por favor, efetue o login novamente.'
        except jwt.InvalidTokenError:
            return 'Token inválido. Por favor, efetue o login novamente.'

    @staticmethod
    def verify_token():
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        elif request.method == 'OPTIONS':
            if 'Access-Control-Request-Headers' in request.headers:
                return make_response(), 200
            else:
                return make_response({'message': 'Requisição inválida'}), 400

        if not token:
            return make_response({'message':
                                  'Por favor, informe o token.'}), 400
        try:
            data = jwt.decode(token.split()[1],
                              SECRET_KEY,
                              algorithms=["HS256"])
            g.current_user = User.query.filter_by(id=data['sub']).first()

        except Exception as e:
            print(e)
            return make_response(
                {'message': 'O token informado é inválido ou incorreto.'}), 400

    @staticmethod
    def verify_role():
        slugFromRequest = request.path.split('/')[1]

        if not hasattr(g, 'current_user'):
            return make_response({
                'message':
                'Não é possível verificar roles. Usuário inválido.'
            }), 400
        user = g.current_user

        role = RoleUser.query.filter_by(user_id=user.id).join(
            Role, Role.id == RoleUser.role_id).filter_by(
                slug=slugFromRequest).first()

        if not role:
            return make_response({
                'message':
                'Você não tem permissão para acessar esta página.'
            }), 401

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
