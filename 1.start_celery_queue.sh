#!/usr/bin/env bash

celery -A sohot.tasks worker --loglevel=info
pgrep -f celery >> pid
