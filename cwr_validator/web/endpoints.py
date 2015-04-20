from flask import request, Response, session
from flask.ext.restful import Api, Resource
import flask as f

from cwr_validator.web import app
from cwr_validator.utils.file_manager import FileManager


__author__ = 'Borja'

# Api object to serve endpoints created
api = Api(app)

# Utils class to work with json
jsonConverter = None

# Main class of the webapp, in charge of the validation
validator = None

fileManager = FileManager()


@app.route('/upload/cwr', methods=['POST'])
def upload_cwr_handler():
    # Get the name of the uploaded file
    sent_file = request.files['file']

    if sent_file:
        fileManager.save_file_cwr(sent_file)
        session['cwr_file_name'] = sent_file.filename
        ctx = app.app_context()
        f.cwr = fileManager.read_cwr(sent_file.filename)


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


api.add_resource(ValidateDocumentAPI, '/cwr/validation', endpoint='validation')


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