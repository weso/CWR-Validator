# -*- encoding: utf-8 -*-
import logging

from flask import current_app
from flask.ext.restful import Resource, reqparse

"""
Flask RESTful resources for the file uploading endpoints.

These take handle of receiving and processing files.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

_logger = logging.getLogger(__name__)


class UploadFileResource(Resource):
    """
    Resource for building an endpoint where files are received.

    It receives a file and sends it to the correct service to be processed.
    """

    def __init__(self):
        super(UploadFileResource, self).__init__()

        self._reqparse = reqparse.RequestParser()
        self._reqparse.add_argument('file_id', type=str, required=True,
                                    help='No file ID provided',
                                    location='json')
        self._reqparse.add_argument('filename', type=unicode, required=True,
                                    help='No file name provided',
                                    location='json')
        self._reqparse.add_argument('contents', type=unicode, required=True,
                                    help='No file contents provided',
                                    location='json')

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
        _logger.info('Received CWR file')

        file_data = self._reqparse.parse_args()

        _logger.info('Accepted CWR file')

        file_service = current_app.config['FILE_SERVICE']

        file_id = file_data['file_id']

        _logger.info('Beginning to process file with id %s' % file_id)

        file_service.process_cwr(file_data)

        _logger.info('Finished processing file with id %s' % file_id)

        return '', 200
