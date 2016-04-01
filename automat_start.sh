#!/bin/sh

#set -x
cd ..
killall -q build-automat
rm -rf automat-db

set -e
mkdir -p automat-db/projects
mkdir -p automat-db/builds
mkdir -p automat-db/records
export GOPATH=`pwd`/automat-db/builds/build-automat
./bin/build-automat --example > automat-db/projects/build-automat
/usr/bin/nohup ./bin/build-automat --serve `pwd`/automat-db < /dev/null > automat.log 2>&1 &
sleep 1
