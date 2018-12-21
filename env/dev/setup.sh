#!/usr/bin/env bash

cat << EOF
Environment Variables:
    ftp_proxy    = ${ftp_proxy}
    http_proxy   = ${http_proxy}
    https_proxy  = ${https_proxy}
    tester_name  = ${tester_name}
    env_rel_path = ${env_rel_path}
EOF

# ------ Install Packages
# apt
apt install sqlite3
# pip
python3 -m pip install --upgrade pip
python3 -m pip install -r /code/requirements.txt

# ------ Configure
sqlite3 /code/data.db ""
