from flask import Flask, Response, abort
from apscheduler.schedulers.background import BackgroundScheduler
from random import randint
from requests import get
from time import sleep

import prometheus_client as prom
from metrics.metrics import register_metrics

import logging
import os


app = Flask(__name__)
register_metrics(app)

HOST = "0.0.0.0"

LOCAL_PORT = 5555
PORT_FLASK = os.getenv('PORT', LOCAL_PORT)

prod = bool(os.getenv('PORT'))
LOCAL_APP_NAME = "http://" + HOST + ":" + str(LOCAL_PORT)
APP_NAME = "https://flask-scheduler.herokuapp.com/" if prod else LOCAL_APP_NAME

# ------------logging---------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flask-scheduler')
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------

# ------------------- APIs ---------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    """"
    Homepage
    """
    return Response("Hi there!", status=200)


@app.route('/ok/', methods=['GET'])
def response_ok():
    """"
    Test endpoint with good response
    """
    sleep(randint(1, 5))  # add sleep to track inprogress stuff
    return Response("OK", status=randint(200, 204))


@app.route('/ko/', methods=['GET'])
def response_ko():
    """"
    Test endpoint with bad response
    """
    sleep(randint(1, 5))  # add sleep to track inprogress stuff
    abort(randint(500, 505))


@app.errorhandler(Exception)
def handle(e):
    return "Test error : " + str(e), e.code


@app.route('/metrics')
def metrics():
    return Response(prom.generate_latest(), mimetype=prom.CONTENT_TYPE_LATEST)

# ---------------------------------------------------------------------------------

def job():
    """
    run requests in a loop using scheduler
    """
    try:
        request_str = APP_NAME
        if randint(0, 1):
            request_str += "ok/"
        else:
            request_str += "ko/"
        logger.info(f"Request : {request_str}")
        get(request_str)
        logger.info(f"Request processed : {request_str}")
    except Exception as e:
        logger.error(f"Got an error : {str(e)} with request : {request_str}")
        pass


# Init the scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job, 'interval', seconds=20)

# Explicitly kick off the background thread
scheduler.start()


if __name__ == '__main__':
    # Note that two scheduler instances will be launched if Flask is in debug mode
    app.run(host=HOST, port=PORT_FLASK, debug=False)