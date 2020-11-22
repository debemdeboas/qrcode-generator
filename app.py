import os

from dotenv           import load_dotenv
from flask            import Flask, request
from flask_bootstrap  import Bootstrap
from flask.templating import render_template
from forms            import QRCodeForm
from qrcode_generator import create_qrcode, IMG_OUTPUT_PATH
from waitress         import serve

#
# Setup
#

load_dotenv()  # Load environment variables

app = Flask(__name__)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.urandom(32)
bootstrap = Bootstrap(app)

if not os.path.exists(IMG_OUTPUT_PATH):
    os.mkdir(IMG_OUTPUT_PATH)  # Creates file path to output image, if not already existent


#
# App routes
#

@app.route('/', methods=['POST', 'GET'])
def homepage():
    """
    Renders application homepage from HTML file.
    
    """
    return render_template(
        'index.html',
        title='QRCode Generator',
        form=QRCodeForm())


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    """
    Renders the generated QR code and prompts the user to download it or generate another.
    
    """
    img_path = create_qrcode(request.form['content'])
    return render_template(
        'generate_qrcode.html',
        title='generated QRCode',
        img=img_path,
        content=request.form['content'])


#
# Run!
#

if __name__ == "__main__":
    #app.run(threaded=True, port=9691)
    serve(app, port=9691, host='0.0.0.0', url_scheme='https')
