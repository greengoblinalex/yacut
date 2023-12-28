import random

from settings import ALLOW_SYMBOLS, ID_LENGTH


def get_unique_short_id(custom_id=None):
    if not custom_id:
        custom_id = ''.join(random.sample(ALLOW_SYMBOLS, ID_LENGTH))
    return custom_id


def url_map_to_dict(url_map):
    return dict(
        id=url_map.id,
        original=url_map.original,
        short=url_map.short,
        timestamp=url_map.timestamp
    )