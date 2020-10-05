from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class QRCodeForm(FlaskForm):
    content = StringField(
        label='QRCode content',
        description='Link, text, email, phone number... anything!',
        validators=[InputRequired()],
    )
