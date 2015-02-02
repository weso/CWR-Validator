import codecs
import json
import urllib3

from flask import render_template, request, send_file, session

from webapp import app
from utils.file_manager import FileManager
from utils.json_converter import JsonConverter


__author__ = 'Borja'

API_ENDPOINT = 'http://127.0.0.1:5000'
DATABASE_ENDPOINT = 'http://127.0.0.1:5002'

fileManager = FileManager()
jsonConverter = JsonConverter()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def manage_uploaded_file():
    # Get the name of the uploaded file
    sent_file = request.files['file']

    if sent_file:
        file_path = fileManager.save_file(sent_file, 'uploads')

        # Open the uploaded file in utf-8 format and validate it
        with codecs.open(file_path, encoding='utf-8') as file_utf8:
            document_content = file_utf8.readlines()

            json_document = jsonConverter.parse_object(document_content)
        req = urllib3.Request(API_ENDPOINT + '/document/validation')
        req.add_header('Content-Type', 'application/json')

        response = urllib3.urlopen(req, json_document)

        response_json = json.loads(response.read())

        with open(FileManager.get_validations_path('CWROutput.V21'), "w") as output_file:
            for record in response_json["records"]:
                output_file.write((record + "\n").encode('utf-8'))
        session['document'] = response_json['document']

        return render_template('results.html', filename='CWROutput.V21', document=response_json["document"])


@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    return send_file(FileManager.get_validations_path(file_name),
                     as_attachment=True,
                     attachment_filename="validation-result.V21")


@app.route('/submit', methods=['POST'])
def submit_file():
    if session['document'] is not None:
        json_document = session['document']
        req = urllib3.Request(DATABASE_ENDPOINT + '/persist-document')
        req.add_header('Content-Type', 'application/json')

        urllib3.urlopen(req, json_document)

    session.pop('document', None)
