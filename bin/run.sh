#!/bin/bash

gunicorn --worker-class eventlet -w 1 backend:app

