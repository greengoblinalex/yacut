from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from settings import URL_LENGTH, CUSTOM_ID_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, URL_LENGTH)]
    )
    custom_id = StringField(
        'Напишите id короткой ссылки',
        validators=[Length(1, CUSTOM_ID_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        from yacut.validators import validate_custom_id_data

        if validate_custom_id_data(field.data):
            raise ValidationError('Указано недопустимое имя для короткой ссылки')
