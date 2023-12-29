from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from yacut.utils import get_unique_short_id
from settings import ALLOW_SYMBOLS, CUSTOM_ID_LENGTH


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    data['custom_id'] = get_unique_short_id(data.get('custom_id'))

    if (
        any(item not in ALLOW_SYMBOLS for item in data['custom_id']) or
        len(data['custom_id']) > CUSTOM_ID_LENGTH
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url_map(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.short_link}), 200
