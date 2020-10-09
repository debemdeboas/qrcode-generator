from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class QRCodeForm(FlaskForm):
    """
    User input for the str content of the desired QR code
    
    """
    content = StringField(
        label='QRCode content',
        description='Link, text, email, phone number... anything!',
        validators=[InputRequired()],
    )
