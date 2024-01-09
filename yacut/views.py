from flask import render_template, redirect, abort

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.crud import create_url_map, get_url_map_by_id
from yacut.validators import validate_custom_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    url_map = None

    if form.validate_on_submit():
        custom_id = validate_custom_id(form.custom_id.data)

        if get_url_map_by_id(custom_id):
            abort(409)

        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        create_url_map(url_map)

    context = {
        'form': form,
        'url_map': url_map,
    }
    return render_template('url_map.html', **context)


@app.route('/<string:short_id>')
def redirect_to_original_url_view(short_id):
    url_map = get_url_map_by_id(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)