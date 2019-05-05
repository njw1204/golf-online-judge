#!/bin/bash

# GolfJudge Python3 Solution Tester
# exit code 0 : Accepted

con="goj-python3-container" # docker container name

SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd )
ret=0 # exit code

# docker variables
time_limit=$4 # seconds

# problem variables
source_file=$1
input_testcase=$2
output_testcase=$3

echo "" > ${SCRIPTPATH}/output.out
sudo docker cp ${source_file} ${con}:/judge/main.py > /dev/null
sudo docker cp ${input_testcase} ${con}:/judge/input.in > /dev/null

sudo docker start ${con} > /dev/null
sudo docker stop -t ${time_limit} ${con} > /dev/null

if [ "$(diff --ignore-trailing-space --ignore-space-change --ignore-blank-lines --text -q ${SCRIPTPATH}/output.out ${output_testcase} 2>&1)" = "" ]; then
  echo "pass"
  ret=0
else
  echo "fail"
  ret=1
fi

sudo rm ${SCRIPTPATH}/output.out
exit $ret
