#!/usr/bin/env bash
args="$@"
vagrant ssh -c "source ./venv/bin/activate && python ./app/manage.py $args"
