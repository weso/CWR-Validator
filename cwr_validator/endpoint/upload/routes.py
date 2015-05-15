# -*- encoding: utf-8 -*-
from flask import request, Blueprint, render_template, current_app, jsonify, Response


__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

upload_blueprint = Blueprint('upload', __name__,
                             template_folder='templates',
                             static_folder='static')


@upload_blueprint.route('/', methods=['POST'])
def upload_cwr_handler():
    # Get the name of the uploaded file
    if 'file' in request.files:
        sent_file = request.files['file']

        if sent_file:
            file_service = current_app.config['FILE_SERVICE']

            file_id = file_service.save_file(sent_file, current_app.config['UPLOAD_FOLDER'])

            jsonify({'file_id': file_id})
    else:
        return Response(status=405)


@upload_blueprint.route('/', methods=['GET'])
def upload():
    return render_template('upload.html')