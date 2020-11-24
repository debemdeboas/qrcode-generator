import hashlib
import segno

from datetime import datetime

IMG_OUTPUT_PATH = 'static/qrcodes/'


def generate_qrcode_image(content, err_lvl):
    """
    Generates the scannable visual output.
    
    Parameters
    ----------
    content: str
        Content to be accessed through QR code

    err_lvl: str
        Desired error correction level

    Returns
    -------
        A QR code image
    
    """
    return segno.make(content, error=err_lvl)


def create_qrcode(content, error='H'):
    """
    Embeds content into a QR code.
    
    Parameters
    ----------
    content: str
        Content to be embedded into QR code
    
    error: str
       QR code error correction level (default: high)
    
    Returns
    -------
        Functional QR code
        
    """
    filename = IMG_OUTPUT_PATH \
        + hashlib.sha256(
            f'{content}_{datetime.now()}'.encode('utf-8')).hexdigest()

    qr = generate_qrcode_image(content, error)

    for ext in ['.svg', '.png']:
        qr.save(
            filename + ext,
            scale=200,
            border=1,
            light='white',
            dark='black')

    return filename
