from flask import Blueprint

from controllers.SessionController import SessionController

session_bp = Blueprint('session_bp', __name__)

session_bp.route('', methods=['POST'])(SessionController.create)
session_bp.route('/validate', methods=['POST'])(SessionController.validate)
