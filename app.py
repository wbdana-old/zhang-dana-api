from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Rsvp

@app.route('/')
def index():
    return jsonify(status=200)

# Get all RSVPs from every guest
@app.route('/rsvps')
def all_rsvps():
    query_result = Rsvp.query.all()
    return jsonify(result=[item.serialize for item in query_result])

@app.route('/rsvp', methods=['POST'])
def add_rsvp():
    rsvp_obj = request.get_json()
    if rsvp_obj['rehearsal'] == "True":
        rsvp_obj['rehearsal'] = True
    else:
        rsvp_obj['rehearsal'] = False
    if rsvp_obj['wedding'] == "True":
        rsvp_obj['wedding'] = True
    else:
        rsvp_obj['wedding'] = False
    if rsvp_obj['brunch'] == "True":
        rsvp_obj['brunch'] = True
    else:
        rsvp_obj['brunch'] = False
    new_rsvp = Rsvp(rsvp_obj['name'], rsvp_obj['email'], rsvp_obj['rehearsal'], rsvp_obj['wedding'], rsvp_obj['brunch'])
    db.session.add(new_rsvp)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run()
