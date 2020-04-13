#!/usr/bin/env bash
args="$@"
vagrant ssh -c "tail -f -n0 ./logs/uwsgi/link-shortener.log & sudo uwsgi --ini ./config/uwsgi/link-shortener.ini $args"
