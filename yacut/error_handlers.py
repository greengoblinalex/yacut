from flask import render_template, jsonify, session, flash

from yacut import app
from yacut.forms import URLMapForm


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(409)
def url_map_already_exists(error):
    form = session.get('form', URLMapForm())
    flash('Предложенный вариант короткой ссылки уже существует.')
    return render_template('url_map.html', form=form), 409


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(error):
    return render_template('404.html'), 404
