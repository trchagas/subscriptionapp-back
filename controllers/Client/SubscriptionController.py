import json
from flask import request, make_response, jsonify, g
from helpers.QueryHelper import QueryHelper

from models.Subscription import Subscription


from config import db


class SubscriptionController:
    def index():
        subscriptions = Subscription.query.order_by(
            Subscription.name.asc())
        data = request.args
        if data:
            data = {k: v for k, v in data.items() if v != ""}
            subscriptions = QueryHelper.checkQueryLimit(
                subscriptions, data)
            subscriptions = QueryHelper.checkQueryOffset(
                subscriptions, data)
        subscriptions = subscriptions.all()
        return jsonify([c.serialize for c in subscriptions])

    def show(id):
        subscription = Subscription.query.filter_by(
            id=id).first()
        if not subscription:
            return make_response({
                'message':
                'Nenhuma inscrição com este identificador está cadastrada.'
            }), 400
        return {
            **subscription.serialize,

        }

    def store():
        auth_user = g.current_user

        subscription_data = json.loads(request.data.decode("utf-8"))["data"]

        if subscription_data:
            subscription_data = {k: v for k,
                                 v in subscription_data.items() if v != ""}

        # errors = validate_StoreSubscription(subscription_data)
        # if errors:
        #     return make_response(errors), 400

        try:

            subscription_data['client_id'] = auth_user.client.user_id
            subscription = Subscription(subscription_data)
            db.session.add(subscription)
            db.session.commit()
            db.session.refresh(subscription)
            # icon = request.files.get('image')
            # if icon:
            #    SubscriptionHelper.updateIcon(icon, subscription)
            return subscription.serialize
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

    def update(id):

        auth_user = g.current_user
        subscription = Subscription.query.filter_by(
            id=id).first()

        if not subscription or subscription.client_id != auth_user.client.user_id:
            return make_response({'message': 'Não autorizado.'}), 401

        subscriptionData = json.loads(request.data.decode("utf-8"))["data"]

        if subscriptionData:
            subscriptionData = {k: v for k,
                                v in subscriptionData.items() if v != ""}

        subscription = Subscription.query.filter_by(id=id)

        try:
            subscription.update(dict(subscriptionData))
            db.session.commit()
            subscription = subscription.first()  # updated subscription

        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
        return subscription.serialize

    def destroy(id):

        subscription = Subscription.query.filter_by(
            id=id).first()
        if not subscription:
            return make_response({
                'message':
                'Nenhuma inscrição com este identificador está cadastrada.'
            }), 400

        try:

            Subscription.query.filter_by(id=id).delete()

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

        return make_response(), 200
