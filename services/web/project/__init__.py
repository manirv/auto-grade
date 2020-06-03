from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from . import auto_grade as ag
from flask import request
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

result = {
        'User': 'manirv',
        'Lab': 'Lab1',
        'labresult': 'PASS',
        'score': 5
    }
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route('/rf/api/v1.0/labs', methods=['GET'])
def get_labs():
    return jsonify({'result': result})

@app.route('/rf/api/v1.0/lab', methods=['POST'])
def post_lab():
    content = request.get_json()
    #print(content)
    result = ag.auto_grade(content['userid'],content['labname'], content['code'])
    return jsonify({'result': result})

@app.route('/rf/api/v1.0/key', methods=['POST'])
def post_key():
    content = request.get_json()
    #print(content)
    result = ag.save_lab_key(content['labname'], content['code'])
    return jsonify({'result': result})

@app.route('/upload_lab')
def load_lab_uploader():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_lab():
   if request.method == 'POST':
      userid = 'mani'
      f = request.files['file']
      file_content = f.read()
      #f.save(secure_filename(f.filename))
      labname = os.path.splitext(os.path.basename(f.filename))[0]
      return eval_lab(grade_lab(file_content), labname, userid)


@app.route('/upload_key')
def load_file_uploader():
   return render_template('upload_key.html')
	
@app.route('/save_key', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      file_content = f.read()
      #f.save(secure_filename(f.filename))
      labname = os.path.splitext(os.path.basename(f.filename))[0]
      return save_key(get_code_cell(file_content), labname)

def get_code_cell(json_data):
    parsed_json = ''
    parsed_json = json.loads(json_data)

    code_content = ''
    cells = parsed_json['cells']

    for cell in cells:
        cell_type = cell['cell_type']

        if 'metadata' not in cell:
            # raise ValueError("No metadata found")
            print("No metadata found")

        if cell_type == 'code':
            if cell['metadata'].get('tags') != None and cell['metadata'].get('tags')[0] == 'solution':
                code_cell = cell['source']
                for code_line in code_cell:
                    code_content = code_content + '\n' + code_line


    return code_content

def grade_lab(json_data):

    parsed_json = ''
    parsed_json = json.loads(json_data)

    code_content = ''
    cells = parsed_json['cells']
    for cell in cells:
        cell_type = cell['cell_type']

        if 'metadata' not in cell:
            # raise ValueError("No metadata found")
            code_cell = cell['source']
            for code_line in code_cell:
                code_content = code_content + '\n' + code_line

        if cell_type == 'code':
            if cell['metadata'].get('tags') == None or cell['metadata'].get('tags')[0] not in ['grade', 'gradehelper']:
                code_cell = cell['source']
                for code_line in code_cell:
                    code_content = code_content + '\n' + code_line
    return code_content

def save_key(code,labname):
    result = ag.save_lab_key(labname, code)
    return jsonify({'labname': labname, 'result': result})

def eval_lab(code,labname, userid):
    result = ag.auto_grade(userid,labname, code)
    return jsonify({'user' : userid, 'labname': labname, 'result': result})
