from flask import jsonify
from backend import app
from backend.utils import check_argument, query_argument, form_argument


@app.route('/api/groups')
@query_argument
@check_argument("_id")
def get_user_groups(_id):
    data = [{
        '_id': 1,
        'name': 'umji'
    }]
    return jsonify(data)
