#!/bin/bash

set -e

PORT=5000
export SENDFILE="yes"

#/opt/cutycapt/app.py &

gunicorn app:__app__                \
    --bind=0.0.0.0:${PORT}          \
    --workers 4                     \
    --log-level=debug               \
    --log-file=/tmp/logfile         \
    --access-logfile=/tmp/accesslog \
    --error-logfile=/tmp/errorlog   \
    --daemon

while ! nc -z localhost ${PORT}; do   
  sleep 0.1 # wait for 1/10 of the second before check again
done

"$@"
