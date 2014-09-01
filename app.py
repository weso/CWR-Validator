import datetime
import urllib2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask.ext.restful import abort
from werkzeug.utils import secure_filename
from document_formater import DocumentFormatter
from validator.validator import Validator

import os
import json

__author__ = 'Borja'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['V21'])

validations = {}

dt_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else obj.__dict__)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('validate_file',
                                filename=filename))


@app.route('/results/<filename>')
def validate_file(filename):

    # No more than 10 validations at a time
    if len(validations) == 10:
        validations.pop()

    file_validator = Validator()
    file_validator.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    validations[filename] = file_validator.document
    return render_template('results.html', filename=filename,
                           document=file_validator.document)

@app.route('/submit/<filename>')
def submit_file(filename):

    if filename in validations.keys():
        document = validations[filename]
        formatter = DocumentFormatter(document)

        agreements = formatter.get_agreements()

        req = urllib2.Request('http://127.0.0.1:5000/agreements')
        req.add_header('Content-Type', 'application/json')

        urllib2.urlopen(req, json.dumps(agreements, default=dt_handler))

        req = urllib2.Request('http://127.0.0.1:5000/works')
        req.add_header('Content-Type', 'application/json')

        works = formatter.get_works()

        for work in works:
            urllib2.urlopen(req, json.dumps(work.attr_dict, default=dt_handler))

        return render_template('results.html', filename=filename, document=document)
    else:
        abort(404)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("5001"),
        debug=True
    )
