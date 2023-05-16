from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "testkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)
Migrate(app=app, db=db)

class Statistics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    stat_id = db.Column(db.String(), unique=True)
    concentration = db.Column(db.String())
    position = db.Column(db.String())
    datetimerecord = db.Column(db.DateTime(), default=datetime.now().replace(microsecond=0)) 

@app.route('/', methods=['GET'])
def main_page():
    stats = Statistics.query.order_by(Statistics.id.desc()).all()
    return render_template('index.html', number=Statistics.query.count(), stats=stats)

@app.route('/fake-data', methods=['GET'])
def fake_data():
    stats = Statistics()
    stats.stat_id = str(uuid.uuid1())
    concentration = 0
    while concentration < 0.5:
        concentration = random.random()
    stats.concentration = str(concentration)
    stats.position = "testing-position"
    db.session.add(stats)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Created fake data"
    })
