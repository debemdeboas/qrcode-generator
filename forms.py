from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.core import BooleanField, DateField, RadioField, TimeField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired


class CustomFlaskForm(FlaskForm):
    name = ''
    QRFormat = '{}'

    @classmethod
    def to_qr_string(cls, dict) -> str:
        print(cls, cls.QRFormat, dict)
        return cls.QRFormat.format(*dict.values())


class BasicQRCodeForm(CustomFlaskForm):
    """
    User input for the str content of the desired QR code

    """
    name = 'Basic QR'

    content = StringField(
        label='QRCode content',
        description='Link, text, email, phone number... anything!',
        validators=[InputRequired()],
    )


class WifiQRCodeForm(CustomFlaskForm):
    """
    Wifi QR Code generator form

    Example:
    `WIFI:T:WPA;S:mynetwork;P:mypass;;`
    """
    name = 'Wi-Fi QR'
    QRFormat = 'WIFI:T:{crypt};S:{ssid};P:{passwd};H:{hidden};;'

    @classmethod
    def to_qr_string(cls, dict) -> str:
        if hidden := dict.get('hidden', 'n') == 'y':
            hidden = 'true'
        else:
            hidden = 'false'

        return cls.QRFormat.format(
            crypt=dict['crypt'],
            ssid=dict['ssid'],
            passwd=dict['passwd'],
            hidden=hidden
        )

    ssid = StringField(
        label='SSID',
        validators=[InputRequired()],
        render_kw={'placeholder': 'My Wi-Fi network'}
    )

    ssid_hidden = BooleanField(
        label='Hidden network',
        default=False
    )

    crypt = RadioField(
        label='Network cryptography',
        choices=[
            ('WEP', 'WEP'),
            ('WPA', 'WPA (default)'),
            # ('WPA2-EAP', 'WPA2-EAP'),
            ('nopass', 'None')],
        default='WPA',
    )

    passwd = PasswordField(
        label='Password',
        render_kw={'placeholder': 'MyPass123 (optional)'},
    )


class EventQRCodeForm(CustomFlaskForm):
    name = 'Event QR'
    QRFormat = \
        """
        BEGIN:VEVENT\r\n
        SUMMARY:{summary}\r\n
        DTSTART:{start}\r\n
        DTEND:{end}\r\n
        END:VEVENT\r\n
        """

    # DTSTART:19980118T073000Z

    DATE_FORMAT = '%Y%m%d'
    TIME_FORMAT = 'T%H%M00Z'

    @classmethod
    def to_qr_string(cls, dict) -> str:
        try:
            dtstart = datetime.strptime(
                f'{dict["dtpicker_start_date"]} {dict["start_hour"]}', '%d/%m/%Y %H:%M')
            dtstart = dtstart.strftime(cls.DATE_FORMAT + cls.TIME_FORMAT)
        except:
            dtstart = datetime.now().strftime(cls.DATE_FORMAT + cls.TIME_FORMAT)

        try:
            dtend = datetime.strptime(
                f'{dict["dtpicker_end_date"]} {dict["end_hour"]}', '%d/%m/%Y %H:%M')
            dtend = dtend.strftime(cls.DATE_FORMAT + cls.TIME_FORMAT)
        except:
            dtend = datetime.now().strftime(cls.DATE_FORMAT + cls.TIME_FORMAT)

        return cls.QRFormat.format(
            summary=dict['event_name'],
            start=dtstart,
            end=dtend
        )

    event_name = StringField(
        label='Event',
        validators=[InputRequired()],
        render_kw={'placeholder': 'My birthday! Please come, I\'m lonely'}
    )

    start_hour = TimeField(label='Starts at')
    end_hour = TimeField(label='Ends at')

    dtpicker_start_date = DateField(label='Begins')
    dtpicker_end_date = DateField(label='Ends')
