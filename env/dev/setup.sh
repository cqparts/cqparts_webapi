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
apt-get update
# apt
apt-get install sqlite3 -y
# pip
python3 -m pip install --upgrade pip
python3 -m pip install -r /code/requirements.txt
# watchman
#   variation of: https://facebook.github.io/watchman/docs/install.html#installing-from-source
apt-get install libssl-dev autoconf automake libtool pkg-config -y
watchman_ver=4.9.0
pushd /tmp
wget -nv https://github.com/facebook/watchman/archive/v${watchman_ver}.tar.gz \
    -O watchman-${watchman_ver}.tar.gz
tar -xzf watchman-${watchman_ver}.tar.gz
cd watchman-${watchman_ver}
./autogen.sh
./configure
make
make install
popd

# ------ Configure
sqlite3 /code/data.db ""
