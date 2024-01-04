from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from urllib import request
import json
from datetime import datetime
# from imageOcr import filterText

from rahmaScraper import RahmaSpider
from snmcScraper import SnmcSpider
from kmaScraper import KmaSpider

app = Flask(__name__, static_folder='../../client/build')
# app = Flask(__name__, static_folder="./build/static", template_folder="./build")

CORS(app)
application = app

rahma = RahmaSpider()
snmc = SnmcSpider()
kma = KmaSpider()

rahmaEvents = rahma.get_events()
rahmaEventCallTime = datetime.now()

rahmaPrayerTimes = rahma.get_prayerTimes()
rahmaPrayerCallTime = datetime.now()

snmcEvents = snmc.get_events()
snmcEventCallTime = datetime.now()

snmcPrayerTimes = snmc.get_prayerTimes()
snmcPrayerCallTime = datetime.now()

kmaEvents = kma.get_events()
kmaEventCallTime = datetime.now()

kmaPrayerTimes = kma.get_prayerTimes()
kmaPrayerCallTime = datetime.now()

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html')

@app.route('/robots.txt', methods=['GET'])
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return send_from_directory(app.static_folder, "sitemap.xml")

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and path != "favicon.ico":
        return send_from_directory('../../client/build', path)
    else:
        return send_from_directory('../../client/build', 'index.html')

@app.route('/api/v1/masjidrahma/events', methods=['GET'])
def get_rahma_events():
    global rahmaEvents, rahmaEventCallTime
    if (datetime.now() - rahmaEventCallTime).total_seconds() > 21600:
        events = rahma.get_events()
        rahmaEvents = events
        rahmaEventCallTime = datetime.now()
    else:
        events = rahmaEvents
    return jsonify(events)


@app.route('/api/v1/masjidrahma/prayer', methods=['GET'])
def get_rahma_prayer():
    global rahmaPrayerTimes, rahmaPrayerCallTime
    if (datetime.now() - rahmaPrayerCallTime).total_seconds() > 21600:
        prayerTimes = rahma.get_prayerTimes()
        rahmaPrayerTimes = prayerTimes
        rahmaPrayerCallTime = datetime.now()
    else:
        prayerTimes = rahmaPrayerTimes
    return jsonify(prayerTimes)


@app.route('/api/v1/snmc/events', methods=['GET'])
def get_snmc_events():
    global snmcEvents, snmcEventCallTime
    if (datetime.now() - snmcEventCallTime).total_seconds() > 21600:
        events = snmc.get_events()
        # events = filterText(snmc.get_events())
        snmcEvents = events
        snmcEventCallTime = datetime.now()
    else:
        events = snmcEvents
    return jsonify(events)


@app.route('/api/v1/snmc/prayer', methods=['GET'])
def get_snmc_prayer():
    global snmcPrayerTimes, snmcPrayerCallTime
    if (datetime.now() - snmcPrayerCallTime).total_seconds() > 21600:
        prayers = snmc.get_prayerTimes()
        snmcPrayerTimes = prayers
        snmcPrayerCallTime = datetime.now()
    else:
        prayers = snmcPrayerTimes
    return jsonify(prayers)

@app.route('/api/v1/kma/events', methods=['GET'])
def get_kma_events():
    global kmaEvents, kmaEventCallTime
    if (datetime.now() - kmaEventCallTime).total_seconds() > 21600:
        events = kma.get_events()
        kmaEvents = events
        kmaEventCallTime = datetime.now()
    else:
        events = kmaEvents
    return jsonify(events)

@app.route('/api/v1/kma/prayer', methods=['GET'])
def get_kma_prayer():
    global kmaPrayerTimes, kmaPrayerCallTime
    if (datetime.now() - kmaPrayerCallTime).total_seconds() > 21600:
        prayers = kma.get_prayerTimes()
        kmaPrayerTimes = prayers
        kmaPrayerCallTime = datetime.now()
    else:
        prayers = kmaPrayerTimes
    return jsonify(prayers)


# # Flask error handling

# Flask error handling
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
    
@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api/"):
        return jsonify(message="Resource not found"), 404
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(405)
def handle_405(e):
    if request.path.startswith("/api/"):
        return jsonify(message="Method not allowed"), 405
    return e

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
