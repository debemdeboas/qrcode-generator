import os

from dotenv           import load_dotenv
from flask            import Flask, request
from flask_bootstrap  import Bootstrap
from flask.templating import render_template
from forms            import QRCodeForm
from qrcode_generator import create_qrcode, IMG_OUTPUT_PATH

#
# Setup
#

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap(app)

if not os.path.exists(IMG_OUTPUT_PATH):
    os.mkdir(IMG_OUTPUT_PATH)


#
# App routes
#

@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('index.html', title='QRCode Generator', form=QRCodeForm())

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    img_path = create_qrcode(request.form['content'])
    return render_template('generate_qrcode.html', title='generated QRCode', img=img_path, content=request.form['content'])

#
# Run!
#

if __name__ == "__main__":
    app.run(threaded=True, port=9691, host='0.0.0.0')
