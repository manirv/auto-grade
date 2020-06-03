from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import auto_grade as ag
from flask import request


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



