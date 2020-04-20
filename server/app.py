# To-Do: Configure CORS to only allow specific requests. Very important!

import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid
import pandas as pd
import json
import load_file

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'}

MATRIX = [
    {
        "id": uuid.uuid4().hex,
        "width": 5,
        "height": 5,
        "x": 2,
        "y": 2,
        "isActive": False
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.secret_key = "super secret key"  # INSECURE AND FOR DEBUGGING PURPOSES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r'/*': {'origins': '*'}}) # enable CORS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_matrix(matrix_id):
    for matrix in MATRIX:
        if matrix['id'] == matrix_id:
            MATRIX.remove(matrix)
            return True
    return False

@app.route('/matrix', methods=['GET', 'POST'])
def all_matrix():
    response_object = {'status': 'success'}
    response_object['matrix'] = MATRIX
    return jsonify(response_object)
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        dataList = json.loads(request.form['form'])
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            extension = os.path.splitext(file.filename)[1]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            make_preview(file, extension, dataList, False)
            return "success"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/matrix/<matrix_id>', methods=['PUT', 'DELETE'])
def single_matrix(matrix_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        response_object['message'] = 'Matrix updated!'
    if request.method == 'DELETE':
        make_preview(False, False, False, matrix_id)
        # remove_matrix(matrix_id)
        response_object['message'] = 'Matrix removed!'
    return jsonify(response_object)

def make_preview(input_file, extension, dataList, remove_id):
    MATRIX.clear()
    MATRICES = load_file.process_upload(input_file, extension, dataList, remove_id)
    for i in range(len(MATRICES)):
        print(MATRICES[i])
        MATRIX.append(MATRICES[i])
    print(MATRIX)
    return

if __name__ == '__main__':
    app.run()