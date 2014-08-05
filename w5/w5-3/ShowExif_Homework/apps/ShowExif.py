import logging
from apps import app
from flask import Flask, render_template, request, url_for
from PIL import Image
from PIL.ExifTags import TAGS
from StringIO import StringIO

from google.appengine.ext import db


class Photo(db.Model):
    photo = db.BlobProperty()

ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg', 'gif']


def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    fileinfo = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            print exifinfo
            if exifinfo != None:
                fileinfo = dict([(TAGS.get(key,key), str(value).decode('utf-8', 'ignore'))
                        for key, value in exifinfo.items()
                        if type(TAGS.get(key,key)) is str])
    except IOError:
        logging.error(fname)
    return fileinfo


def allowed_file(filename):
    return '.' in filename.lower() and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# index.html
@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filestream = file.read()
            upload_data = Photo()
            upload_data.photo = db.Blob(filestream)
            upload_data.put()

            url = url_for("shows", key=upload_data.key())
            exif_data = get_exif_data(StringIO(filestream))

            return render_template('ShowExif.html',
                original_path = url,
                exif_data = exif_data)
    return render_template("index.html")


@app.route('/show/<key>', methods=['GET'])
def shows(key):
    uploaded_data = db.get(key)
    return app.response_class(uploaded_data.photo)