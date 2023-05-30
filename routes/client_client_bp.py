from flask import Blueprint

from controllers.Client.ClientController import ClientController

client_client_bp = Blueprint('client_client_bp', __name__)

client_client_bp.route('', methods=['GET'])(ClientController.index)
client_client_bp.route('/<int:id>',
                       methods=['PUT'])(ClientController.update)
