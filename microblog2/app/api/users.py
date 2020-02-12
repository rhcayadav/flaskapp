from app.api import bp
from flask import jsonify
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    #print(User.query.get_or_404(id))
    return jsonify(User.query.get_or_404(id).to_dict())
    #return str(User.query.get_or_404(id))