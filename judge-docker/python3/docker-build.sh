#!/bin/bash
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd )
sudo docker build -t goj-python3 ${SCRIPTPATH}
