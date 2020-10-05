import hashlib
import segno
from datetime import datetime

IMG_OUTPUT_PATH = 'static/qrcodes/'

def generate_qrcode_image(content, err_lvl):
    return segno.make(content, error = err_lvl)

def create_qrcode(content, error = 'H'):
    filename = IMG_OUTPUT_PATH + hashlib.sha256(f'{content}_{datetime.now()}'.encode('utf-8')).hexdigest() + '.svg'
    generate_qrcode_image(content, error).save(filename, scale=10, light='white', dark='black')
    return filename
