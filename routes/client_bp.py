from flask import Blueprint

from controllers.ClientController import ClientController

client_bp = Blueprint('client_bp', __name__)

client_bp.route('', methods=['POST'])(ClientController.store)
