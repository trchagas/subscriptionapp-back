import json
from flask import request, make_response, jsonify, g
from helpers.QueryHelper import QueryHelper
from helpers.SubscriptionTemplateHelper import SubscriptionTemplateHelper

from models.SubscriptionTemplate import SubscriptionTemplate
from models.SubscriptionTemplateIcon import SubscriptionTemplateIcon

from validator.StoreSubscriptionTemplate import validate_StoreSubscriptionTemplate
from validator.UpdateSubscriptionTemplate import validate_UpdateSubscriptionTemplate

from config import db


class SubscriptionTemplateController:
    def index():
        subscription_templates = SubscriptionTemplate.query.order_by(
            SubscriptionTemplate.name.asc())
        data = request.args
        if data:
            data = {k: v for k, v in data.items() if v != ""}
            subscription_templates = QueryHelper.checkQueryLimit(
                subscription_templates, data)
            subscription_templates = QueryHelper.checkQueryOffset(
                subscription_templates, data)
        subscription_templates = subscription_templates.all()
        return jsonify([c.serialize for c in subscription_templates])

    def show(id):
        subscription_template = SubscriptionTemplate.query.filter_by(
            id=id).first()
        if not subscription_template:
            return make_response({
                'message':
                'Nenhum template com este identificador está cadastrado.'
            }), 400
        return {
            **subscription_template.serialize,
            **{
                'icon': subscription_template.icon.serialize if subscription_template.icon else None
            }
        }

    def store():
        auth_user = g.current_user
        requestData = request.form.to_dict()
        subscription_template_data = json.loads(requestData['data'])
        if subscription_template_data:
            subscription_template_data = {k: v for k, v in subscription_template_data.items() if v != ""}

        errors = validate_StoreSubscriptionTemplate(subscription_template_data)
        if errors:
            return make_response(errors), 400

        try:
            subscription_template_data['admin_id'] = auth_user.admin.user_id
            subscription_template = SubscriptionTemplate(subscription_template_data)
            db.session.add(subscription_template)
            db.session.commit()
            db.session.refresh(subscription_template)
            icon = request.files.get('image')
            if icon:
                SubscriptionTemplateHelper.updateIcon(icon, subscription_template)
            print(subscription_template)
            return subscription_template.serialize
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

    def update(id):
        auth_user = g.current_user
        subscription_template = SubscriptionTemplate.query.filter_by(
            id=id).first()

        if not subscription_template or subscription_template.admin_id != auth_user.admin.user_id:
            return make_response({'message': 'Não autorizado.'}), 401

        requestData = request.form.to_dict()
        subscription_templateData = json.loads(requestData['data'])
        if subscription_templateData:
            subscription_templateData = {
                k: None if v == "" else v
                for k, v in subscription_templateData.items()
            }

        errors = validate_UpdateSubscriptionTemplate(subscription_templateData)
        if errors:
            return make_response(errors), 400

        subscription_template = SubscriptionTemplate.query.filter_by(id=id)
        icon = request.files.get('image')
        try:
            subscription_template.update(dict(subscription_templateData))
            db.session.commit()
            subscription_template = subscription_template.first()  #updated subscription_template
            if icon:
                SubscriptionTemplateHelper.updateIcon(icon, subscription_template)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
        return subscription_template.serialize

    def destroy(id):
        subscription_template = SubscriptionTemplate.query.filter_by(
            id=id).first()
        if not subscription_template:
            return make_response({
                'message':
                'Nenhum template com este identificador está cadastrado.'
            }), 400

        iconOnly = request.args.get('iconOnly')
        try:
            icon = subscription_template.icon
            if not iconOnly:
                SubscriptionTemplate.query.filter_by(id=id).delete()
            if icon:
                SubscriptionTemplateHelper.removeIcon(icon)
                SubscriptionTemplateIcon.query.filter_by(
                    subscription_template_id=subscription_template.id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

        return make_response(), 200
