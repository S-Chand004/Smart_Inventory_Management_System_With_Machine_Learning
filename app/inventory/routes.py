from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory')
def inventory():
    return 'This is the inventory page.'
