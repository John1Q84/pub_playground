#!/usr/bin/python3
# testing code
from flask import Flask, render_template, redirect, url_for
from flask_restx import Api, Resource

import json
import random

# OTLP tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource, get_aggregated_resources

# Exporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Propagation
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.aws import AwsXRayPropagator

# AWS X-Ray ID Generator
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator

# Resource detector
from opentelemetry.sdk.extension.aws.resource.ec2 import (
    AwsEc2ResourceDetector,
)

# Setup AWS X-ray propagator
set_global_textmap(AwsXRayPropagator())

# Setup AWS EC2 resource detector
resource = get_aggregated_resources (
    [
        AwsEc2ResourceDetector(),
    ]
)

# Setup tracer provider with the X-Ray ID generator
tracer_provider = TracerProvider(resource=resource, id_generator=AwsXRayIdGenerator())
processor = BatchSpanProcessor(OTLPSpanExporter())
tracer_provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(tracer_provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)


# Instrumentation
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor


# Instrumentation
BotocoreInstrumentor().instrument()


with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
FlaskInstrumentor().instrument_app(app)
api = Api(app)
const = ['1.jpeg', '2.jpeg', '3.jpeg', '4.jpeg', '5.jpeg']

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'
def img_select(const):
    return random.choice(const) 


@app.route('/service')
def servoce():
    return render_template(
        'index.html',
        title = 'I love cats',
        # backend_url = 'http://localhost:8080',
        image_url = 'https://raw.githubusercontent.com/John1Q84/pub_playground/main',
        image_file='images/cats/' + img_select(const)
    )


@app.route('/kr/service')
def kr_servoce():
    return render_template(
        'index.html',
        title = '<KR> I love cats',
        # backend_url = 'http://localhost:8080',
        image_url = 'https://raw.githubusercontent.com/John1Q84/pub_playground/main',
        image_file='images/cats/' + img_select(const)
    )

@app.route('/us/service')
def us_servoce():
    return render_template(
        'index.html',
        title = '<US> I love cats',
        # backend_url = 'http://localhost:8080',
        image_url = 'https://raw.githubusercontent.com/John1Q84/pub_playground/main',
        image_file='images/cats/' + img_select(const)
    )



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
