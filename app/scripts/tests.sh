#! /usr/bin/env bash

export $(grep -v '^#' .env | xargs -0)

pytest app/tests
