#!/usr/bin/env bash
args="$@"
vagrant ssh -c "source ./venv/bin/activate && cd ./app/ && poetry $args"
