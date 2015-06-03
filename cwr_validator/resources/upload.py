# -*- encoding: utf-8 -*-
from flask import request, current_app, jsonify
from flask.ext.restful import abort, Resource

"""
Flask RESTful resources for the file uploading endpoints.

These take handle of receiving and processing files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'


class UploadFileResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def get(self):
        """
        Getting from the uploads endpoint is disallowed.

        A message is returned to indicate this.

        :return: a message warning that the get command is disallowed
        """
        return 'Please, send files to the web service through a POST method.'

    def post(self):
        """
        Posts a file to the endpoint.

        It should receive a file, which can have any name, as it will just take the first file on the request.

        :return:
        """
        files = request.files.values()
        if not isinstance(files, list):
            files = list(request.files.values())
        if len(files) > 0:
            sent_file = files[0]

            if sent_file:
                file_service = current_app.config['FILE_SERVICE']

                file_id = file_service.process_cwr(sent_file)

                jsonify({'file_id': file_id})
        else:
            abort(405, message='No files received')
