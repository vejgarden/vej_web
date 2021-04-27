#!/bin/bash
source /home/ubuntu/.bashrc
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $CWD
/home/ubuntu/py385/bin/uwsgi --http 0.0.0.0:5090 --mount /=flask_app:app --master -b 8192 --socket ./web.sock --chmod-socket=777 --vacuum --die-on-term
