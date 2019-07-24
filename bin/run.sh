#!/bin/bash

export BACKEND_SETTINGS=`pwd`/settings.cfg
gunicorn --worker-class eventlet -w 1 backend:app --bind 0.0.0.0:8000

