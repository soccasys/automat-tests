#!/bin/sh

#set -x
cd ..
killall -q build-automat
rm -rf automat-db build-automat-tests/build-automat.log

set -e
mkdir -p automat-db/projects
mkdir -p automat-db/builds
mkdir -p automat-db/records
export GOPATH=`pwd`/automat-db/builds/build-automat
./bin/build-automat --example > automat-db/projects/build-automat
# Careful with the next line, the order of the redirections are done must not be modified.
# Using the wrong order can cause the python script invoking this shell script to hang indefinitely.
nohup ./bin/build-automat --serve `pwd`/automat-db < /dev/null > build-automat-tests/build-automat.log 2>&1 &
sleep 1
