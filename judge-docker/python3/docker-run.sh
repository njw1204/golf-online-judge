#!/bin/bash
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd )
echo "[goj-python3-container]"
sudo docker stop goj-python3-container
sudo docker rm goj-python3-container
echo "" > ${SCRIPTPATH}/output.out
sudo docker create --log-driver=none --cpus=".5" --memory="128m" -v ${SCRIPTPATH}/output.out:/judge/output.out --name goj-python3-container goj-python3
