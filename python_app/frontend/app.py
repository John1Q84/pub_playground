#!/usr/bin/python3
# testing code
from flask import Flask, render_template, redirect, url_for
from flask_restx import Api, Resource

import json, datetime

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
api = Api(app)


# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'

@app.route('/index')
def index():
    d = datetime.datetime.now()
    return render_template(
        'index.html',
        title = 'AWSome Demo Day!',
        time_now = d.strftime("%Y. %m. %d %A, %p %I:%m:%S"),
        region = configs['INFO']['REGION']
    )

@app.route('/service')
def google():
    return redirect("http://service.mydomain.int/service") # backend serviced의 endpoint, 실습에서는 hardcording으로 수행



# @api.route('/hello')
# class InfoReturn(Resource):
#     def get(self):
#         return {"hello": "HelloWorld!", "version": "Blue", "region": "localhost"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
