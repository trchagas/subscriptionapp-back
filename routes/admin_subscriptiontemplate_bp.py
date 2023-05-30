from flask import Blueprint

from controllers.Admin.SubscriptionTemplateController import SubscriptionTemplateController

admin_subscriptiontemplate_bp = Blueprint(
    'admin_subscriptiontemplate_bp', __name__)

admin_subscriptiontemplate_bp.route('', methods=['GET'])(
    SubscriptionTemplateController.index)
admin_subscriptiontemplate_bp.route('', methods=['POST'])(
    SubscriptionTemplateController.store)
admin_subscriptiontemplate_bp.route('/<int:id>',
                                    methods=['PUT'])(SubscriptionTemplateController.update)
admin_subscriptiontemplate_bp.route(
    '/<int:id>', methods=['GET'])(SubscriptionTemplateController.show)
admin_subscriptiontemplate_bp.route('/<int:id>',
                                    methods=['DELETE'])(SubscriptionTemplateController.destroy)
