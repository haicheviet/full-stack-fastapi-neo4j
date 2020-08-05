#! /usr/bin/env bash
set -e

python ./app/backend_pre_start.py

# Beat
celery worker --beat --workdir=. -A app.worker --loglevel=info