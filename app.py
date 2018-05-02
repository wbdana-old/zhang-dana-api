from flask import Flask
from flask import jsonify
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


if __name__ == '__main__':
    app.run()
