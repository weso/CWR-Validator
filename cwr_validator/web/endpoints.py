from flask import request, Response
from flask.ext.restful import Api

from cwr_validator.web import app
from cwr_validator.service.file import LocalCWRFileService


__author__ = 'Borja'

# Api object to serve endpoints created
api = Api(app)

# Utils class to work with json
jsonConverter = None

file_service = LocalCWRFileService()


@app.route('/upload/cwr', methods=['POST'])
def upload_cwr_handler():
    # Get the name of the uploaded file
    sent_file = request.files['file']

    if sent_file:
        id = file_service.save_file(sent_file)
        file_service.process_file(id)


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