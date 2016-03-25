#!/bin/bash

export PATH=$PATH:/usr/local/bin/
cd ~/devel/fii-watcher/api/
source env/bin/activate
source ~/.nvm/nvm.sh
nvm use 4.2
~/devel/fii-watcher/api/env/bin/python ~/devel/fii-watcher/api/feed
