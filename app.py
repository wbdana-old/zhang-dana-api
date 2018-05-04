from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/rsvp": {"origins": "https://zhang-dana.herokuapp.com"}})
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

# Needs to be a find or create by NAME
@app.route('/rsvp', methods=['POST'])
@cross_origin(origin='https://zhang-dana.herokuapp.com', headers=['Content-Type'])
def add_rsvp():
    try:
        rsvp_obj = request.get_json()
        user = Rsvp.query.filter_by(email=rsvp_obj['name']).first()
        if not not user:
            if rsvp_obj['name'] == "":
                return 'Name cannot be blank!', 400
            if rsvp_obj['email'] == "":
                return 'Email cannot be blank!', 400
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
            return 'We can\'t wait to see you!', 200
        else:
            user.name = rsvp_obj['name']
            user.rehearsal = rsvp_obj['rehearsal']
            user.wedding = rsvp_obj['wedding']
            user.brunch = rsvp_obj['brunch']
            db.session.commit()
            return 'We\'ve updated your RSVP!', 200
    except Error as e:
        print e
        return 'oh fuck', 500

# To update:
# e.g., first user with email="william.b.dana@gmail.com"
# user = Rsvp.query.filter_by(email="william.b.dana@gmail.com").first()
# user.name = "Updated Name"
# db.session.commit()

# Failed search for user by criterion:
# not not User //=> False

# def get_or_create_instrument(session, serial_number):
#     instrument = session.query(Instrument).filter_by(serial_number=serial_number).first()
#     if instrument:
#         return instrument
#     else:
#         instrument = Instrument(serial_number)
#         session.add(instrument)
#         return instrument


if __name__ == '__main__':
    app.run()
