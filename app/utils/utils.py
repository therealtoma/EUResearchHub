from re import match
from shutil import copy

from werkzeug.utils import secure_filename


def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return match(pattern, s)


def upload_file(file, name):
    # no file has been uploaded, using default profile picture
    if file is None:
        copy('../static/images/profile.jpg', f'../uploads/profile_images/{name}.jpg')
    else:
        filename = secure_filename(file.filename)
        file.save(f'../uploads/profile_images/{filename}.jpg')
