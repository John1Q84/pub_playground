#!/bin/bash
set -e

## Set global variables
export RTN_VAL=0
export FILE="batch-put-items.json"


echo '>> Get Region ....'
export REGION=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep region | cut -d \" -f 4`
echo $REGION && echo ''


## remove aws-cli v1 and install v2
yum remove awscli -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
unzip -u awscliv2.zip
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update

## check existances of DynamoDB Table
export VAL=`aws dynamodb list-tables | grep 'lab1-table' | wc -l`

if [ ${VAL} -eq 1 ]
then
    echo "dynamo DB is ready"
    RTN_VAL=1
else
    echo "lab1-table is not ready" >&2
    exit 1
fi


## check batch-put-item.json file
if [ ! -f ${FILE} ] 
then
    echo "item json file is not provided"
    exit 1
fi

## Put data to the DynamoDB Table
if [ ${RTN_VAL} -eq 1 ] 
then
    aws dynamodb batch-write-item --request-items file://batch-put-items.json
fi
