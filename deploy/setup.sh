#!/bin/bash

# XXX Probably not finished yet

# Initial Upgrading
apt-get update
apt-get upgrade

# apt-get dependencies
apt-get install -y python-dev python-pip python-virtualenv postgresql-9.4 \
                   libpq-dev zip unzip htop ipython curl git vim-nox sudo \
                   supervisor

# Add swap
fallocate -l 2G /swapfile
mkswap /swapfile
cat >> /etc/fstab << EOF
/swapfile       none            swap        sw              0       0
EOF

# Cloning the project
mkdir -p ~/devel/
cd ~/devel
git clone https://github.com/nihey/fii-watcher.git

# RDBMS setup
# Allow us to create a user for ourselves
cat > /etc/postgresql/9.4/main/pg_hba.conf < ~/devel/fii-watcher/deploy/pg_hba.conf
/etc/init.d/postgresql restart
# Create a user and a database
createuser root -U postgresql -s
createdb fii_watch

# Database setup
cd fii-watcher/api
psql fii_watch < data/sql/schema.sql

# Python dependencies
virtualenv env --system-site-packages
env/bin/pip2.7 -r requirements.txt

# node version manager, along with node dependencies
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 4.4
nvm alias default 4.4
npm install casperjs phantomjs@1

# Setup cronjob
crontab ~/devel/fii-watcher/deploy/crontab
