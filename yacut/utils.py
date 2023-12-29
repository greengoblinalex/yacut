import random

from yacut.models import URLMap
from settings import ALLOW_SYMBOLS, ID_LENGTH


def get_unique_short_id(custom_id=None):
    if not custom_id:
        while True:
            custom_id = ''.join(random.sample(ALLOW_SYMBOLS, ID_LENGTH))
            if not URLMap.query.filter_by(short=custom_id).first():
                break
    return custom_id


def url_map_to_dict(url_map):
    return dict(
        id=url_map.id,
        original=url_map.original,
        short=url_map.short,
        timestamp=url_map.timestamp
    )