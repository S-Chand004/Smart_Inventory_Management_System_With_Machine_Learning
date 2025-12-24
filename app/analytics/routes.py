from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics():
    return 'This is the analytics page.'
