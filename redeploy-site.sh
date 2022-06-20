#!/bin/bash

# Move and activate script in parent folder in order for it to work properly

tmux kill-server
cd ./project-crab-gang
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
tmux new-session -d -s "server"
tmux  send-keys -t "server" "flask run --host=0.0.0.0" Enter
echo "testing"

