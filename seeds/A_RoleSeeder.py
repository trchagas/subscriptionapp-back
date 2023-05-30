from flask_seeder import Seeder
from flask import make_response

from models.Role import Role

from config import db


class A_RoleSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        roles = [
            Role(slug='admin', description='admin role'),
            Role(slug='client', description='client role')
        ]

        try:
            for role in roles:
                db.session.add(role)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response({'message': e}), 500
