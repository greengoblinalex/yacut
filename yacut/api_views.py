from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from yacut.utils import validate_data


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json()
    url_map = URLMap()
    url_map.from_dict(validate_data(data))
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url_map(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
