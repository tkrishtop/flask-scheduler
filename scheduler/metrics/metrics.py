from flask import request
from prometheus_client import Counter, Gauge, Histogram
from time import time


# Request count
REQUEST_COUNT = Counter(
    'scheduler_request_count', 'Scheduler request count',
    ['app_name', 'method', 'endpoint', 'http_status']
)


def save_request(response):
    if ('metrics' not in request.path) and ('favicon' not in request.path):
        REQUEST_COUNT\
            .labels('scheduler', request.method, request.path, response.status_code)\
            .inc()
    return response


# Ongoing request count
ONGOING_REQUEST_COUNT = Gauge(
    'scheduler_ongoing_request_count', 'Scheduler ongoing request count',
    ['app_name', 'method', 'endpoint']
)


def add_ongoing():
    if ('metrics' not in request.path) and ('favicon' not in request.path):
        ONGOING_REQUEST_COUNT\
            .labels('scheduler', request.method, request.path)\
            .inc()


def remove_ongoing(response):
    if ('metrics' not in request.path) and ('favicon' not in request.path):
        ONGOING_REQUEST_COUNT\
            .labels('scheduler', request.method, request.path)\
            .dec()
    return response


# Request response time
REQUEST_RESPONSE_TIME = Histogram(
    'scheduler_request_response_time_seconds', 'Scheduler request response time seconds',
    ['app_name', 'endpoint']
)


def start_timer():
    if ('metrics' not in request.path) and ('favicon' not in request.path):
        request.start_time = time()


def stop_timer(response):
    if ('metrics' not in request.path) and ('favicon' not in request.path):
        response_time = time() - request.start_time
        REQUEST_RESPONSE_TIME.labels('scheduler', request.path).observe(response_time)
    return response


# Register all metrics
def register_metrics(app):
    app.before_request(start_timer)
    app.before_request(add_ongoing)
    app.after_request(save_request)
    app.after_request(remove_ongoing)
    app.after_request(stop_timer)
