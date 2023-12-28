from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from settings import URL_LENGTH, CUSTOM_ID_LENGTH, ALLOW_SYMBOLS


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
        if any(char not in ALLOW_SYMBOLS for char in field.data):
            raise ValidationError('Указано недопустимое имя для короткой ссылки')