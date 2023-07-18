#!/bin/sh

echo 'get temporary token for metedata'
TOKEN=`curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
echo ''

echo '>> Get Region ....'
REGION=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep region | cut -d \" -f 4`
echo $REGION && echo ''

HERE=$(dirname $(realpath -s $0))
echo $HERE

#cat configs.json.tpl | sed -i "s/REGION_CODE/'$region'/g" > configs.json
cat configs.json.tpl | sed "s/REGION_CODE/$REGION/g" > configs.json

source "$HERE/v_demo_app/bin/activate"
pip3 install --upgrade pip
pip3 install -r requirements.txt

# install python opentelemetry sdk and other libraries for tradcing
# pip3 install opentelemetry-api
# pip3 install opentelemetry-sdk
# pip3 install opentelemetry-distro
# pip3 install opentelemetry-exporter-otlp-proto-grpc
# pip3 install opentelemetry-sdk-extension-aws
# pip3 install opentelemetry-propagator-aws-xray
# pip3 install opentelemetry-distro opentelemetry-exporter-otlp
# pip3 install opentelemetry-instrumentation-botocore
# pip3 install opentelemetry-instrumentation-flask

# pip3 install opentelemetry-distro[otlp]>=0.24b0 \
#             opentelemetry-sdk-extension-aws~=2.0 \
#             opentelemetry-propagator-aws-xray~=1.0

opentelemetry-bootstrap -a install

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
export OTEL_PROPAGATORS=xray \
export OTEL_PYTHON_ID_GENERATOR=xray \

opentelemetry-instrument \
    --service_name myServiceCats \
    python3 app.py


#python3 app.py
