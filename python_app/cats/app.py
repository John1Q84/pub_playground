#!/usr/bin/python3
# testing code
from flask import Flask, render_template, request, current_app, g as app_ctx
from flask_restx import Resource

import json, random, logging, os, time
import boto3
from botocore.exceptions import ClientError

# logging path setting
if not os.path.isdir('logs'):
  os.mkdir('logs')

# default werkzeug logger diable
logging.getLogger('werkzeug').disabled = True

logger = logging.getLogger('myLogger')
# log location, log level setting
logging.basicConfig(filename = "logs/backend-cat.log", level = logging.DEBUG)

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

# Get the dynamodb resource
dynamodb = boto3.resource('dynamodb')

app = Flask (__name__)

@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    global ELAPSED_TIME
    elapsed_time = time.perf_counter() - app_ctx.start_time
    ELAPSED_TIME = int(elapsed_time * 1000)
    current_app.logger.info('%s ms %s %s %s', ELAPSED_TIME, request.method, request.path, response.status )
    return response


def isTableExist(table_name):
    try:
        table = dynamodb.Table('table_name')
        table.load()
        return True
    except ClientError as err:
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            logger.error(
                "Could not check for dynamoDB table existence of %s. Here's why: %s: %s",
                table_name, err.response['Error']['Code'], err.response['Error']['Message']
            )
            raise




#const = ['1.jpeg', '2.jpeg', '3.jpeg', '4.jpeg', '5.jpeg']

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'
def get_id():
    return '10'+ random(1, 2, 3, 4, 5)

def get_url(table_name):
    if isTableExist(table_name):
        id = get_id
        logger.info("get %s item from table", id)
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={'id': id},
            ProjectionExpression='url'
        )
        return response
    else:
        logger.error(
            "Cloud not get item from Table. Because, %s: %s",
            ClientError.response['Error']['Code'], ClientError.response['Error']['Message']
        )
        raise
    

@app.route('/cat')
def service():
    return render_template(
        'index.html',
        title = 'I love cats',
        # backend_url = 'http://localhost:8080',
        #image_url = 'https://raw.githubusercontent.com/John1Q84/pub_playground/main',
        #image_file='images/cats/' + img_select(const)
        image_url = get_url('lab1-table')
    )




if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
