from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from db.models import Database
from datetime import datetime
import logging


app = Flask(__name__, static_folder='../client/build/static', template_folder="../client/build")
# app = Flask(__name__, static_folder="./build/static", template_folder="./build")

CORS(app)
application = app

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info('Started')
db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
logging.info('Database connected')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

# get all organizations from the database and save them to a global variable to be cached and update once a week
organizations = db.get_all_organizations()
organizationsCallTime = datetime.now()


@app.route('/robots.txt', methods=['GET'])
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return send_from_directory(app.static_folder, "sitemap.xml")

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico")

@app.route('/api/v1/events')
def get_events_all():
    # get all events from the database
    events = db.get_all_events_created_today()
    return jsonify(events)

@app.route('/api/v1/events/<int:organization_id>')
def get_events(organization_id):
    # get all events from the database
    events = db.get_all_events_by_organization_today(organization_id)
    return jsonify(events)

@app.route('/api/v1/events/<string:organization_name>')
def get_events_by_name(organization_name):
    # get all events from the database
    events = db.get_all_events_by_organization_name(organization_name)
    return jsonify(events)

@app.route('/api/v1/prayer_times')
def get_prayer_times_all():
    # get all events from the database
    prayer_times = db.get_all_prayer_times()
    return jsonify(prayer_times)

@app.route('/api/v1/prayer_times/<int:organization_id>')
def get_prayer_times(organization_id):
    # get all events from the database
    prayer_times = db.get_all_prayer_times_by_organization(organization_id)
    return jsonify(prayer_times)

@app.route('/api/v1/prayer_times/<string:organization_name>')
def get_prayer_times_by_name(organization_name):
    # get all events from the database
    prayer_times = db.get_all_prayer_times_by_organization_name(organization_name)
    return jsonify(prayer_times)

@app.route('/api/v1/organizations')
def get_organizations():
    # get all organizations from the database
    global organizations, organizationsCallTime
    if (datetime.now() - organizationsCallTime).total_seconds() > 604800:
        organizations = db.get_all_organizations()
        organizationsCallTime = datetime.now()
    return jsonify(organizations)

@app.route('/api/v1/organizations/<int:organization_id>/image')
def get_organization_image(organization_id):
    # get all organizations from the database
    image = db.get_organization_image(organization_id)
    return jsonify(image)

# Flask error handling
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
    
@app.errorhandler(404)
def handle_404(e):
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(405)
def handle_405(e):
    return jsonify(message="Method not allowed"), 405

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == '__main__':
    app.run()