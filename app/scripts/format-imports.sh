#!/bin/sh -e
export $(grep -v '^#' .env | xargs -0)

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --apply app
sh ./scripts/format.sh
