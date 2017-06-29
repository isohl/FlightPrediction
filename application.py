from flask import Flask, current_app, jsonify, request
import traceback
import logging

import predict

application = Flask(__name__)
logger = logging.getLogger("FlightPrediction")

@application.route("/")
def root():
    return current_app.send_static_file('index.html')

@application.route("/track")
def track():
    resp = {"success":False}
    try:
        trackup, trackdown = predict.webPredict(request.args)
        resp["trackup"] = trackup
        resp["trackdown"] = trackdown
        resp["success"] = True
    except:
        print traceback.format_exc()
    return jsonify(resp)

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    application.debug = True
    application.run(host='0.0.0.0', port=80)