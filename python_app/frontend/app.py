#!/usr/bin/python3
# testing code
from flask import Flask, render_template, current_app, redirect, url_for, Response, request, abort, g as app_ctx
from time import strftime

import json, datetime, requests, time, logging, os

# logging path setting
if not os.path.isdir('logs'):
  os.mkdir('logs')

# default werkzeug logger diable
logging.getLogger('werkzeug').disabled = True

# log location, log level setting
logging.basicConfig(filename = "logs/frontend.log", level = logging.INFO)

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
#api = Api(app)
CAT_SITE_NAME = 'http://cat-service.mydomain.int/'
DOG_SITE_NAME = 'http://dog-service.mydomain.int/'
ELAPSED_TIME = 0
#SITE_NAME = 'http://localhost:8080/'   # for local test

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'

@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    global ELAPSED_TIME
    timestamp = strftime(' %Y-%b-%dT%H:%M:%S')
    elapsed_time = time.perf_counter() - app_ctx.start_time
    ELAPSED_TIME = int(elapsed_time * 1000)
    current_app.logger.info('%s %s %s %s %s %s', timestamp, ELAPSED_TIME, request.method, request.remote_addr, request.path, response.status )
    return response



@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template(
        '404.html',
        title = 'Sorry, page not found..',
    ), 404

@app.route('/')
def default():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    d = datetime.datetime.now()
    region = configs['INFO']['REGION']
    return render_template(
        'index.html',        
        time_now = d.strftime("%Y. %m. %d %A, %p %I:%m:%S"),
        region = region,
        title = "Hands on time"
    )


@app.route('/<path:path>',methods=['GET'])
def proxy(path):
    global CAT_SITE_NAME
    global DOG_SITE_NAME
    if path == 'cat':
        if request.method == 'GET':
            resp = requests.get(f'{CAT_SITE_NAME}{path}')
            response = Response(resp.text, resp.status_code)
        else:
            abort(403)
    elif path == 'dog':
        if request.method == 'GET':
            resp = requests.get(f'{DOG_SITE_NAME}{path}')
            response = Response(resp.text, resp.status_code)
        else:
            abort(403)
    else:
        app.logger.error('Invalide page request')
        abort(404)
    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)