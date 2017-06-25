!#/bin/bash

apt-get update
apt-get install -y libgrib-api-dev python-dev python-pip

pip install numpy==1.7.* pyproj==1.9.5.1
pip install -r requirements.txt