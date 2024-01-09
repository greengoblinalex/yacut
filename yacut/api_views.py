from flask import jsonify, request

from yacut import app
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from yacut.crud import create_url_map, get_url_map_by_id
from yacut.validators import validate_api_data


@app.route('/api/id/', methods=['POST'])
def create_new_url_map():
    data = request.get_json()
    url_map = URLMap()

    validated_data = validate_api_data(data)
    url_map.from_dict(validated_data)

    create_url_map(url_map)
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url_map(short_id):
    url_map = get_url_map_by_id(short_id)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
