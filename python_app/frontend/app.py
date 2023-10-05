#!/usr/bin/python3
# testing code
import json, datetime, requests, os, time
from flask import Flask, render_template, current_app, Response, request, abort, g as app_ctx
from flask_restx import Api, Resource

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
api = Api(app)
SITE_NAME = 'http://service.mydomain.int/'
#SITE_NAME = 'http://localhost:8080/'   # for local test

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'

@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    elapsed_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(elapsed_time * 1000)
    current_app.logger.info('%s %s %s %s ms', request.method, request.path, requests.status_codes, time_in_ms )
    return response


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template(
        '404.html',
        title = 'Sorry, page not found..',
    ), 404

@app.route('/', defaults={'path': '/index'})

@app.route('/index')
def index():
    d = datetime.datetime.now()
    return render_template(
        'index.html',
        title = 'AWSome Demo Day!',
        time_now = d.strftime("%Y. %m. %d %A, %p %I:%m:%S"),
        region = configs['INFO']['REGION']
    )


@app.route('/<path:path>',methods=['GET'])
def proxy(path):
    global SITE_NAME
    if path == 'cat':
        SITE_NAME='cat-'+SITE_NAME
        app.logger.
    elif path == 'dog':
        SITE_NAME='dog='+SITE_NAME
    else:
        app.logger()
        abort(404)
    if request.method == 'GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        response = Response(resp.text, resp.status_code)
    else:
        abort(403)
    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
