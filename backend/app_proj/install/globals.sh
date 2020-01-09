#!/bin/bash
# GLOBAL INSTALLS

sudo apt-get update

sudo apt-get install python3-pip python3-dev libpq-dev -y 

sudo apt-get install postgresql postgresql-contrib -y 

sudo apt-get install nginx -y 

sudo apt-get install gunicorn3 -y

