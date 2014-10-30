from flask import request, Response

from flask.ext.restful import Api, Resource
from api import api_app
from utils.json_converter import JsonConverter
from validator import Validator


__author__ = 'Borja'

# Api object to serve endpoints created
api = Api(api_app)

# Utils class to work with json
jsonConverter = JsonConverter()

# Main class of the webapp, in charge of the validation
validator = Validator()


class ValidateDocumentRegexAPI(Resource):
    @staticmethod
    def get():

        return 'Please, use this endpoint by post method.'

    @staticmethod
    def post():

        if request.json is None:
            result = {
                'success': False,
                'error': 'Expected json content'
            }

            return response_json_item(result)
        else:
            # Get json document from the request
            json_document = request.json

            # Validate the regex
            valid_records, invalid_records = validator.validate_document_format(json_document)

            result = {
                'success': True,
                'valid_records': valid_records,
                'invalid_records': invalid_records
            }

            return response_json_item(result)


class ValidateDocumentAPI(Resource):
    @staticmethod
    def get():

        return 'Please, use this endpoint by post method.'

    @staticmethod
    def post():

        if request.json is None:
            result = {
                'success': False,
                'error': 'Expected json content'
            }

            return response_json_item(result)
        else:
            # Get json document from the request
            json_document = request.json

            # Validate the regex
            document = validator.validate_document(json_document)

            records = []
            for record in sorted(document.extract_records(), key=lambda item: item.number):
                records.append(record.record.encode('utf-8'))
                for message in record.messages:
                    records.append(str(message).encode('utf-8'))

            jsonConverter.print_object(document)

            result = {
                'success': True,
                'document': document,
                'records': records
            }

            return response_json_item(result)


api.add_resource(ValidateDocumentRegexAPI, '/document/validation/regex', endpoint='regex_validation')
api.add_resource(ValidateDocumentAPI, '/document/validation', endpoint='validation')


def response_json_list(app_request, collection):
    """
    Return response with the content in the format requested
    :type app_request: object
    Available formats:
    * JSON

    :param app_request: the request object
    :param collection: the collection to be converted
    :return: response in the requested format
    """

    def return_json():
        return Response(jsonConverter.parse_object(collection), mimetype='application/json')

    functions = {
        'json': return_json,
    }

    functions_accept = {
        'application/json': return_json,
    }

    if request.args.get('format') in functions.keys():
        return functions[app_request.args.get('format')]()
    else:
        return (functions_accept[app_request.headers.get('Accept')]
                if request.headers.get('Accept') in functions_accept.keys() else functions['json'])()


def response_json_item(item):
    return Response(jsonConverter.parse_object(item), mimetype='application/json')