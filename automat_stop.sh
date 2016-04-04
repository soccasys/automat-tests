#!/bin/sh

set -x
cd ..
killall -q automat-server
rm -rf automat-db
