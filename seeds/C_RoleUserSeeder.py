from flask_seeder import Seeder
from flask import make_response

from models.RoleUser import RoleUser

from config import db


class C_RoleUserSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        roles = [
            RoleUser(role_id=1, user_id=1),
            RoleUser(role_id=2, user_id=2)
        ]

        try:
            for role in roles:
                db.session.add(role)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response({'message': e}), 500
