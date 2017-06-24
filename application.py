from flask import Flask, current_app, jsonify, request
import traceback

import LocalPredict

application = Flask(__name__)

@application.route("/")
def root():
    return current_app.send_static_file('index.html')

@application.route("/track")
def track():
    resp = {"success":False}
    try:
        trackup, trackdown = LocalPredict.webPredict(request.args)
        resp["trackup"] = trackup
        resp["trackdown"] = trackdown
        resp["success"] = True
    except:
        print traceback.format_exc()
    return jsonify(resp)

if __name__ == "__main__":
    application.debug = True
    application.run()