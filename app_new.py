from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
from flask_caching import Cache
from db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from db.models import Database
from datetime import datetime
from utils.webhook import process_message_event
import logging


app = Flask(__name__, static_folder='../client/build/static', template_folder="../client/build")
app.config['CACHE_TYPE'] = 'simple'  # Simple memory cache
cache = Cache(app)
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
    return send_from_directory(app.template_folder, "robots.txt")

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return send_from_directory(app.template_folder, "sitemap.xml")

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.template_folder, "favicon.ico")

@app.route('/api/v1/events')
@cache.cached(timeout=87400)  # Cache timeout set to 86400 seconds (24 hours)
def get_events_all():
    # get all events from the database
    events = db.get_all_active_events()  # Using the new function to get active events
    # events = db.get_all_events_created_today()
    return jsonify(events)

@app.route('/api/v1/events/<int:organization_id>')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_events(organization_id):
    # get all events from the database
    events = db.get_all_events_by_organization_active(organization_id)
    return jsonify(events)

@app.route('/api/v1/events/<string:organization_name>')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_events_by_name(organization_name):
    # get all events from the database
    events = db.get_all_events_by_organization_name(organization_name)
    return jsonify(events)

@app.route('/api/v1/prayer_times')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_prayer_times_all():
    # get all events from the database
    prayer_times = db.get_all_prayer_times()
    return jsonify(prayer_times)

@app.route('/api/v1/prayer_times/<int:organization_id>')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_prayer_times(organization_id):
    # get all events from the database
    prayer_times = db.get_all_prayer_times_by_organization(organization_id)
    return jsonify(prayer_times)

@app.route('/api/v1/prayer_times/<string:organization_name>')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_prayer_times_by_name(organization_name):
    # get all events from the database
    prayer_times = db.get_all_prayer_times_by_organization_name(organization_name)
    return jsonify(prayer_times)

@app.route('/api/v1/organizations')
@cache.cached(timeout=87400)
def get_organizations():
    # get all organizations from the database
    global organizations, organizationsCallTime
    if (datetime.now() - organizationsCallTime).total_seconds() > 604800:
        organizations = db.get_all_organizations()
        organizationsCallTime = datetime.now()
    return jsonify(organizations)

@app.route('/api/v1/organizations/<int:organization_id>/image')
@cache.cached(timeout=87400, query_string=True)  # Considers query string parameters for caching
def get_organization_image(organization_id):
    # get all organizations from the database
    image = db.get_organization_image(organization_id)
    return jsonify(image)

@app.route('/api/v1/webhook', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
def webhook_handler():
    # Only allow accepted methods (POST, PUT, PATCH, DELETE)
    if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
        logging.warning(f"Received unsupported HTTP method: {request.method}")
        return jsonify({'error': 'Method not allowed'}), 405

    # Try to get the JSON body from the request
    data = request.get_json(silent=True)
    if not data:
        logging.error("Invalid or missing JSON in the request")
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Log the incoming request data for debugging/traceability.
    logging.info(f"Received {request.method} request: {data}")

    # Process webhook events based on their type
    # (Messages, Statuses, Chats, etc.)
    if 'messages' in data:
        for message in data['messages']:
            # Filter out outgoing messages if needed
            if not message.get('from_me', True):
                process_message_event(db, message)
    # You can add additional conditions for other events such as chats, contacts, etc.
    else:
        logging.warning("Webhook event data does not contain known keys (messages/statuses/etc.)")

    # Always acknowledge the webhook with a success code
    return jsonify({'status': 'success'}), 200

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