from pathlib import Path
import base64

ROOT = Path.cwd() 
BASE_PATH = ROOT / 'data'

def img_to_string(file='img/logo-ioasys-alpa.png'):
    with open(file, "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        return str
    
def string_to_img(base64_string):
    img = base64.b64decode(base64_string)
    return img 
