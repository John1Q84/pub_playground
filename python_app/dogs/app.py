#!/usr/bin/python3
# testing code
from flask import Flask, render_template, redirect, url_for
from flask_restx import Api, Resource

import json
import random

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
api = Api(app)
const = ['_1.jpeg','_2.jpeg','_3.jpeg','_4.jpeg','_5.jpeg']

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'
def img_select(const):
    return random.choice(const)


@app.route('/service')
def service():
    return render_template(
        'index.html',
        title = 'Dogs are cool',
        #backend_url = 'http://localhost:8080',
        backend_url = 'http://service.mydomain.int',
        image_file='images/' + img_select(const)
    )


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
