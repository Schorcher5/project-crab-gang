#!/bin/bash

# Move and activate script in parent folder in order for it to work properly


cd ./project-crab-gang
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio
echo "testing"
