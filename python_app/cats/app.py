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
const = ['1', '2', '3', '4', '5']
extend = ".jpeg"

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'
def img_select(const):
    return random.choice(const) + extend


@app.route('/service')
def index():
    return render_template(
        'index.html',
        title = 'I love cats',
        image_file="images/" + img_select(const)
    )

# @app.route('/service')
# def google():
#     return redirect("http://service.mydomain.int/service")

# @api.route('/hello')
# class InfoReturn(Resource):
#     def get(self):
#         return {"hello": "HelloWorld!", "version": "Blue", "region": "localhost"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
