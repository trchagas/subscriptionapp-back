from flask import Blueprint

from controllers.Admin.AdminController import AdminController

admin_admin_bp = Blueprint('admin_admin_bp', __name__)

admin_admin_bp.route('', methods=['GET'])(AdminController.index)
admin_admin_bp.route('/<int:id>', methods=['PUT'])(AdminController.update)
