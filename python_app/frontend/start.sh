#!/bin/sh
echo 'get temporary token for metedata'
export TOKEN=`curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
echo ''

echo '>> Get Region ....'
export REGION=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep region | cut -d \" -f 4`
echo $REGION && echo ''


export HERE=$(dirname $(realpath -s $0))
echo $HERE

#export region="us-east-1"

#cat configs.json.tpl | sed -i "s/REGION_CODE/'$region'/g" > configs.json
cat configs.json.tpl | sed "s/REGION_CODE/$REGION/g" > configs.json

source "$HERE/put-data.sh" > put-data.log
source "$HERE/v_demo_app/bin/activate"
pip3 install -r requirements.txt

python3 app.py
