from wtforms.form import Form
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import StringField

class SmsForm(Form):
    phone = StringField('Phone', validators=[validators.DataRequired(),
        validators.length(11, 11, '手机号不正确')])