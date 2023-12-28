from datetime import datetime
from urllib.parse import urlparse

from flask import request

from yacut import db
from settings import URL_LENGTH, FIELDS_MODEL_TO_API_DICT


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_LENGTH), nullable=False)
    short = db.Column(db.String(URL_LENGTH), unique=True, nullable=False)
    short_link = db.Column(db.String(URL_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(URLMap, self).__init__(*args, **kwargs)
        self.set_short_link()

    def set_short_link(self):
        parsed_url = urlparse(request.url)
        self.short_link = f'{parsed_url.scheme}://{parsed_url.netloc}/{self.short}/'

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.short_link
        }

    def from_dict(self, data):
        for field in FIELDS_MODEL_TO_API_DICT:
            if field in data:
                setattr(self, FIELDS_MODEL_TO_API_DICT[field], data[field])
        self.set_short_link()