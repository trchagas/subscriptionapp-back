from flask_seeder import Seeder
from flask import make_response
from models.Client import Client

from models.User import User
from models.Admin import Admin

from config import db


class B_UserSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        users = [
            User(email='admin@mail.com', password='123456'),
            User(email='client@mail.com', password='123456')
        ]

        try:
            for user in users:
                db.session.add(user)

            admin = Admin(1, 'Admin teste')
            client = Client({
                "user_id": 2,
                "name": "Nome teste",
            })

            db.session.add(admin)
            db.session.add(client)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
