from flask import Blueprint

from controllers.Client.NotificationController import NotificationController

client_notification_bp = Blueprint(
    'client_notification_bp', __name__)

client_notification_bp.route('', methods=['GET'])(
    NotificationController.index)
client_notification_bp.route('', methods=['POST'])(
    NotificationController.store)
client_notification_bp.route(
    '/<int:id>', methods=['GET'])(NotificationController.show)
client_notification_bp.route('/<int:id>/already-seen', methods=['PUT'])(
    NotificationController.setAsAlreadySeen)
