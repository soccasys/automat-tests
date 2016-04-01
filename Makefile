all: clean
	PYTHONPATH=python_lib python run_test.py

clean:
	rm -rf python_lib/automat/*.pyc
