from flask import Blueprint

from controllers.Client.SubscriptionController import SubscriptionController

client_subscription_bp = Blueprint(
    'client_subscription_bp', __name__)

client_subscription_bp.route('', methods=['GET'])(
    SubscriptionController.index)
client_subscription_bp.route('', methods=['POST'])(
    SubscriptionController.store)
client_subscription_bp.route('/<int:id>',
                             methods=['PUT'])(SubscriptionController.update)
client_subscription_bp.route('/<int:id>',
                             methods=['DELETE'])(SubscriptionController.destroy)
client_subscription_bp.route(
    '/<int:id>', methods=['GET'])(SubscriptionController.show)
