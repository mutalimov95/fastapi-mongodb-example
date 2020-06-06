#! /usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)

celery worker -A app.worker -l info -Q main-queue -c 1
