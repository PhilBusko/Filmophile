#!/bin/bash
# GLOBAL INSTALLS

sudo apt-get update

sudo apt-get install python3-pip python3-dev libpq-dev -y 

sudo apt-get install postgresql postgresql-contrib -y 

sudo apt-get install nginx -y 

sudo apt-get install gunicorn3 -y

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node

echo ''
pip3 --version
psql --version
nginx -v
gunicorn3 --version
node -e "console.log('node.js: ' + process.version)"

