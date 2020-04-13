#!/usr/bin/env bash
vagrant ssh -c "source ./venv/bin/activate && python -m pip install -r ./app/requirements.txt"
