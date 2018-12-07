#!/usr/bin/env bash

cat << EOF
Environment Variables:
    ftp_proxy    = ${ftp_proxy}
    http_proxy   = ${http_proxy}
    https_proxy  = ${https_proxy}
    tester_name  = ${tester_name}
    env_rel_path = ${env_rel_path}
EOF

# install from custom-packages folder
#find /code/tests/env/custom-packages \
#    -name *.tar.gz \
#    -exec pip3 install {} \;

# install PyPI requirements
pip3 install -r /code/requirements.txt
