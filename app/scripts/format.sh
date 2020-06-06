#!/bin/sh -e
export $(grep -v '^#' .env | xargs -0)

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
black app
isort --recursive --apply app