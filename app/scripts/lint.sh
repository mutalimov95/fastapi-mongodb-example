#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)

mypy app
black app --check
isort --recursive --check-only app
flake8
