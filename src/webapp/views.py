import codecs
import json

import requests
from flask import render_template, request, send_file, session, redirect, url_for

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
        filename = 'CWROutput.V21'
        file_path = fileManager.save_file(sent_file, 'uploads')

        # Open the uploaded file in utf-8 format and validate it
        with codecs.open(file_path, encoding='utf-8') as file_utf8:
            document_content = file_utf8.readlines()

            json_document = jsonConverter.parse_object(document_content)

        url = API_ENDPOINT + '/document/validation'
        headers = {'Content-type': 'application/json'}
        req = requests.post(url, data=json_document, headers=headers)

        response_json = req.json()

        with open(FileManager.get_validations_path(filename), "w") as output_file:
            for record in response_json["records"]:
                output_file.write((record + "\n").encode('utf-8'))
        session['document_name'] = filename
        with open(FileManager.get_validations_path(filename+ '.json'), "w") as output_file:
            json.dump(response_json["document"], output_file)

        return render_template('results.html', filename=filename, document=response_json["document"])


@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    return send_file(FileManager.get_validations_path(file_name),
                     as_attachment=True,
                     attachment_filename="validation-result.V21")


@app.route('/submit', methods=['POST'])
def submit_file():
    if session['document'] is not None:
        filename = session['document_name']
        with open(FileManager.get_validations_path(filename+'.json'), "w") as input_file:
            json_document = json.load(input_file)
        url = DATABASE_ENDPOINT + '/persist-document'
        headers = {'Content-type': 'application/json'}
        requests.post(url, data=json_document, headers=headers)

    session.pop('document_name', None)
    return redirect(url_for('index'))
