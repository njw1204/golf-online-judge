#!/bin/bash

# GolfJudge Python3 Solution Tester
# exit code 0 : Accepted

image_id="799" # docker image id (CHANGE THIS VALUE FOR YOUR PROJECT)

UUID=$(uuidgen) # container & output file unique name
ret=0 # exit code

# docker variables
time_limit=$4 # seconds
memory_limit="128M"

# problem variables
source_file=$1
input_testcase=$2
output_testcase=$3

echo "" > ${UUID}
sudo docker create --log-driver=none -m ${memory_limit} --stop-timeout ${time_limit} -v ${PWD}/${UUID}:/judge/output.out --name ${UUID} ${image_id} > /dev/null 2>&1
sudo docker cp ${source_file} ${UUID}:/judge/main.py > /dev/null 2>&1
sudo docker cp ${input_testcase} ${UUID}:/judge/input.in > /dev/null 2>&1

sudo docker start ${UUID} > /dev/null 2>&1
sudo docker stop ${UUID} > /dev/null 2>&1

if [ "$(diff --ignore-trailing-space --ignore-space-change --ignore-blank-lines --text -q ${UUID} ${output_testcase} 2>&1)" = "" ]; then
  echo "pass"
  ret=0
else
  echo "fail"
  ret=1
fi

sudo docker rm ${UUID} > /dev/null 2>&1
exit $ret
