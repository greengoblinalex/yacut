from yacut.utils import is_empty_string, get_unique_short_id
from yacut.crud import get_url_map_by_id
from yacut.error_handlers import InvalidAPIUsage
from settings import CUSTOM_ID_LENGTH, ALLOW_SYMBOLS


def validate_api_data(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = validate_custom_id(data.get('custom_id'))

    if validate_custom_id_data(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if get_url_map_by_id(custom_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    data['custom_id'] = custom_id
    return data


def validate_custom_id(custom_id):
    return get_unique_short_id() if is_empty_string(custom_id) else custom_id


def validate_custom_id_data(custom_id):
    return (
        any(item not in ALLOW_SYMBOLS for item in custom_id) or
        len(custom_id) > CUSTOM_ID_LENGTH or len(custom_id) < 1
    )