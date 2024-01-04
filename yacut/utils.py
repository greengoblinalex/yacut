import random

from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from settings import ALLOW_SYMBOLS, ID_LENGTH, CUSTOM_ID_LENGTH


def get_unique_short_id():
    while True:
        custom_id = ''.join(random.sample(ALLOW_SYMBOLS, ID_LENGTH))
        if not URLMap.query.filter_by(short=custom_id).first():
            break
    return custom_id


def is_empty_string(input_string):
    return input_string is None or input_string.strip() == ''


def validate_data(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if is_empty_string(custom_id):
        data['custom_id'] = get_unique_short_id()
    else:
        if (
            any(item not in ALLOW_SYMBOLS for item in custom_id) or
            len(custom_id) > CUSTOM_ID_LENGTH
        ):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    return data