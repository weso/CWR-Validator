# -*- encoding: utf-8 -*-
from flask import request, current_app, jsonify, Response
from flask.ext import restful


__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class UploadFileResource(restful.Resource):
    def get(self):
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        # Get the name of the uploaded file
        if 'file' in request.files:
            sent_file = request.files['file']

            if sent_file:
                file_service = current_app.config['FILE_SERVICE']

                file_id = file_service.save_file(sent_file, current_app.config['UPLOAD_FOLDER'])

                if file_id:
                    jsonify({'file_id': file_id})
                else:
                    return Response(status=405)
        else:
            return Response(status=405)