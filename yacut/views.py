from flask import render_template, redirect, flash, abort

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    url_map = None

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Такой id уже существует, пожалуйста, выберите другой или оставьте поле пустым')
            return render_template('url_map.html', form=form)

        while True:
            unique_short_id = get_unique_short_id(custom_id)
            if not URLMap.query.filter_by(short=unique_short_id).first():
                break

        url_map = URLMap(
            original=form.original_link.data,
            short=unique_short_id
        )
        db.session.add(url_map)
        db.session.commit()

    context = {
        'form': form,
        'url_map': url_map,
    }
    return render_template('url_map.html', **context)


@app.route('/<string:short_id>/')
def redirect_to_original_url_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)