from dotenv import load_dotenv
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask.templating import render_template
from qrcode_generator import create_qrcode, IMG_OUTPUT_PATH
from waitress import serve

import forms
import inspect
import os
import sys

#
# Setup
#

load_dotenv()  # Load environment variables

app = Flask(__name__)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.urandom(32)
Bootstrap(app)
datepicker(app)

if not os.path.exists(IMG_OUTPUT_PATH):
    # Creates file path to output images, if not already existent
    os.mkdir(IMG_OUTPUT_PATH)

#
# App routes
#


@app.route('/', methods=['POST', 'GET'])
def homepage():
    """
    Renders application homepage from HTML file.

    """

    forms_list = map(lambda x: (eval('forms.' + x[0])(), x[0], eval('forms.' + x[0]).name),
                     inspect.getmembers(sys.modules['forms'],
                                        lambda x:
                                            inspect.isclass(x) and issubclass(x, forms.CustomFlaskForm) and x is not forms.CustomFlaskForm))

    return render_template(
        'index.html',
        title='QRCode Generator',
        forms=list(forms_list),
    )


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    """
    Renders the generated QR code and prompts the user to download it or generate another.

    """
    qr_content = eval(
        'forms.' + request.form['form_type']).to_qr_string(request.form.to_dict())

    img_path = create_qrcode(qr_content)
    return render_template(
        'generate_qrcode.html',
        title='generated QRCode',
        img=img_path,
        content=qr_content)


#
# Run!
#

if __name__ == "__main__":
    if os.getenv('APP_DEBUG') == 'y':
        app.run(threaded=True, port=9691, debug=True)
    else:
        serve(app, port=9691, host='0.0.0.0', url_scheme='https')
