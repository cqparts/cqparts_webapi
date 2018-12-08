#!/usr/bin/env bash

# Create database
db_file=data.db
if [ ! -f "${db_file}" ] ; then
    echo creating empty database: ${db_file}
    sqlite3 ${db_file} ""
fi

# Run serve
python3 serve.py
