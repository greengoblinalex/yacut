from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from settings import FIELDS_MODEL_TO_API_DICT, ALLOW_SYMBOLS, CUSTOM_ID_LENGTH


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json()

    if all(key not in data for key in FIELDS_MODEL_TO_API_DICT.keys()):
        raise InvalidAPIUsage('Отсутствует тело запроса')

    for key in FIELDS_MODEL_TO_API_DICT.keys():
        if key not in data:
            raise InvalidAPIUsage(f'`{key}` является обязательным полем!')

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


@app.route('/api/id/<int:id>/', methods=['GET'])
def get_url_map(id):
    url_map = URLMap.query.get(id)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.short_link}), 200
