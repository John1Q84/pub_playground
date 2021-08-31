#!/bin/bash
set -e

echo 'get temporary token for metedata'
TOKEN=`curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
echo ''

echo '>> Get Region ....'
export REGION=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep region | cut -d \" -f 4`
echo $REGION && echo ''

echo '>> Get instance id ....'
INSTANCE_ID=`curl -s -H "X-aws-ec2-metadata-token: $TOKEN"  http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep instanceId | cut -d \" -f 4`
echo $INSTANCE_ID && echo ''

REPO='https://github.com/John1Q84/pub_playground.git'


# curl http://169.254.169.254/latest/dynamic/instance-identity/document | grep availabilityZone | cut -d \" -f 4 | sed 's/.$//'

main() {
    if [ $(id -u) -ne 0 ]; then
        echo "Run script as rool!" >&2
        exit 1
    fi

    if [ ! -d "/opt/builders" ] ; then
        mkdir /opt/builders
    fi

    export HOME_DIR="/opt/builders"
   
    sleep=0
    while true; do
        get_tags &&
        git_init &&
        make_service &&
        break
    done
    echo 'initializing complete !!'
    exit 0

}

get_tags() {
    echo 'Get tags' 
    query="Reservations[*].Instances[*].[Tags[?Key=='service_name'].Value | [0]]"
    export service_name=`aws ec2 describe-instances --instance-id $INSTANCE_ID --region $REGION --query "$query" --out text`
    echo 'Tag name "service_name" is,' && echo "$service_name"
}

git_init(){
    yum install git -y
    cd $HOME_DIR
    git init builders_pkg
    cd builders_pkg
    git config core.sparseCheckout true
    git remote add -f origin $REPO
    echo "python_app/$service_name" > .git/info/sparse-checkout
    git pull origin main
}

make_service(){
    if [ ! -d $HOME_DIR/builders_pkg/python_app/$service_name ] ; then
        echo "git init failed"
        exit 1
    fi

    cd $HOME_DIR
    service_file=$HOME_DIR/buildersApp.service.tpl
    echo '[Unit]' > $service_file
    echo 'Description=Builders Micro Service' >> $service_file
    echo -e '\n' >> $service_file
    echo '[Service]' >> $service_file
    echo "ExecStart=$HOME_DIR/builders_pkg/python_app/$service_name/start.sh" >> $service_file
    echo "WorkingDirectory=$HOME_DIR/builders_pkg/python_app/$service_name" >> $service_file
    echo -e '\n' >> $service_file
    echo '[Install]' >> $service_file
    echo 'WantedBy=multi-user.target' >> $service_file
    
    echo 'Qualification...'
    cat $service_file

    cp $service_file /etc/systemd/system/buildersApp.service
    systemctl daemon-reload
    systemctl enable buildersApp
    systemctl start buildersApp

}

main