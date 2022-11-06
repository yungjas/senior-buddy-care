from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime

from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.sql import func

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3316/senior_buddies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Acceleration(db.Model):
    __tablename__ = 'acceleration'
    acc_id = db.Column(db.Integer, primary_key=True)
    acc = db.Column(FLOAT(unsigned=True), nullable=False)
    tilt = db.Column(db.String(64), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            "acc_id" : self.acc_id,
            "acc" : self.acc,
            "tilt" : self.tilt,
            "time_created" : self.time_created
        }

class Weight(db.Model):
    __tablename__ = 'weight'
    weight_id = db.Column(db.Integer, primary_key=True)
    weight_data = db.Column(FLOAT(unsigned=True), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            "weight_id" : self.weight_id,
            "weight_data" : self.weight_data,
            "time_created" : self.time_created
        }

@app.route("/acceleration/<string:date>")
def get_accleration(date):
    accs = Acceleration.query.filter(func.date(Acceleration.time_created) == datetime.strptime(date, '%Y-%m-%d')).all()
    if len(accs):
        return jsonify(
            {
                "code": 200,
                "data":  [acc.json() for acc in accs]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no data."
        }
    ), 404

@app.route("/weight/<string:date>")
def get_weight(date):
    weights = Weight.query.filter(func.date(Weight.time_created) == datetime.strptime(date, '%Y-%m-%d')).all()
    if len(weights):
        return jsonify(
            {
                "code": 200,
                "data":  [weight.json() for weight in weights]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no data."
        }
    ), 404

@app.route("/calendar")
def get_calendar():
    days = db.session.query(Weight.time_created, func.min(Weight.weight_data)).group_by(func.date(Weight.time_created)).all()
    if len(days):
        return jsonify(
            {
                "code": 200,
                "data":  [ {
                    "time_created" : day[0],
                    "weight_data" : day[1]
                } for day in days]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no data."
        }
    ), 404


@app.route("/dates")
def get_dates():
    days = db.session.query(Weight.time_created).group_by(func.date(Weight.time_created)).all()
    if len(days):
        return jsonify(
            {
                "code": 200,
                "data":  [ {
                    "time_created" : day[0],
                } for day in days]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no data."
        }
    ), 404
app.run(host='0.0.0.0', port=5001, debug=True)