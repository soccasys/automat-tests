all: clean
	cd ..;GOPATH=`pwd` go install github.com/soccasys/build-automat
	PYTHONPATH=python-lib python run_test.py

clean:
	rm -rf python-lib/automat/*.pyc python-lib/automat/test/*.pyc
	-killall -q build-automat-db
	rm -rf ../bin ../pkg ../automat-db build-automat.log
