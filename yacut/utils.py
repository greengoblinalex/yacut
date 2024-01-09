import random

from yacut.crud import get_url_map_by_id
from settings import ALLOW_SYMBOLS, ID_LENGTH


def get_unique_short_id():
    while True:
        custom_id = ''.join(random.sample(ALLOW_SYMBOLS, ID_LENGTH))
        if not get_url_map_by_id(custom_id):
            break
    return custom_id


def is_empty_string(input_string):
    return input_string is None or input_string.strip() == ''
