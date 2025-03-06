# Python backend (Flask):

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

def initialize_database():
    with app.app_context():
        db.create_all()

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'lat': e.lat, 'lng': e.lng} for e in events])

@app.route('/api/events', methods=['POST'])
def add_event():
    data = request.json
    new_event = Event(name=data['name'], lat=data['lat'], lng=data['lng'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event added successfully'}), 201

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        lat = request.form['lat']
        lng = request.form['lng']
        new_event = Event(name=name, lat=float(lat), lng=float(lng))
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event added successfully'}), 201
    return render_template('create_event.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
    
#DON'T FORGET TO GIT INIT FOR VERSION CONTROL
