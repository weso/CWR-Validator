import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask.ext.bootstrap import Bootstrap
from validator import validator
from werkzeug.utils import secure_filename
from validator.validator import Validator

__author__ = 'Borja'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['V21'])

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
    file_validator = Validator()
    file_validator.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('results.html', filename=filename,
                           document=file_validator.document)


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
        port=int("80"),
        debug=True
    )