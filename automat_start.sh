#!/bin/sh

#set -x
cd ..
killall -q automat-server
rm -rf automat-db automat-tests/automat-server.log

set -e
mkdir -p automat-db/projects
mkdir -p automat-db/builds
mkdir -p automat-db/records
# Careful with the next line, the order of the redirections are done must not be modified.
# Using the wrong order can cause the python script invoking this shell script to hang indefinitely.
nohup ./bin/automat-server --serve `pwd`/automat-db < /dev/null > automat-tests/automat-server.log 2>&1 &
sleep 1
