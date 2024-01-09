from yacut import db
from yacut.models import URLMap


def create_url_map(url_map):
    db.session.add(url_map)
    db.session.commit()


def get_url_map_by_id(id):
    return URLMap.query.filter_by(short=id).first()