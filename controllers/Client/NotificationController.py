from flask import request, make_response, jsonify, g
from helpers.QueryHelper import QueryHelper
from helpers.UserHelper import UserHelper

from validator.StoreNotification import validate_StoreNotification
from models.User import User
from models.Notification import Notification

from config import db


class NotificationController:

    def store():
        auth_user = g.current_user
        notificationData = request.get_json()
        if notificationData:
            notificationData = {k: v for k, v in notificationData.items() if v != ""}

        errors = validate_StoreNotification(notificationData)
        if errors:
            return make_response(errors), 400

        try:
            notificationData['client_id'] = auth_user.client.user_id
            notification = Notification(notificationData)
            db.session.add(notification)
            db.session.commit()
            return notification.serialize
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

    def index():
        notifications = Notification.query.all()
        return jsonify([p.serialize for p in notifications])

    def show(id):
        notification = Notification.query.get(id)
        if not notification:
            return make_response({
                'message':
                'Nenhuma notificação com este identificador está cadastrada.'
            }), 400
        return notification.serialize

    def setAsAlreadySeen(id):
        auth_user = g.current_user
        notification = Notification.query.filter(
            Notification.id == id,
            Notification.client_id == auth_user.client.user_id)
        if not notification:
            return make_response({'message': 'Não autorizado'}), 401
        try:
            Notification.query.filter_by(id=id).update(
                {'already_seen': True})
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
        return make_response(), 200
