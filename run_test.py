import automat.test
import automat
import unittest
import sys
import subprocess
import time


class AutomatTestCase(unittest.TestCase):

    def setUp(self):
        try:
            self.runCmd(["/bin/bash", "./automat_stop.sh"])
        except:
            pass
        self.runCmd(["/bin/bash", "./automat_start.sh"])

    def tearDown(self):
        try:
            self.runCmd(["/bin/bash", "./automat_stop.sh"])
        except:
            pass

    def runCmd(self, command_and_args):
        return subprocess.check_output(command_and_args, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

class AUTOMAT_BFT_001(AutomatTestCase):
    def runTest(self):
        """Simple check of the server functionality"""
        s = automat.Automat("127.0.0.1", 8080)
        p = s.Project("build-automat")
        p.Build()

def suite():
    suite=unittest.TestSuite()
    suite.addTest(AUTOMAT_BFT_001())
    return suite
    

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print "Available tests are:"
        for test in suite():
            print test.id().split('.')[1],":",test.shortDescription()
        del sys.argv[1]
        sys.exit(0)
    runner = automat.test.FormattedTestRunner()
    if len(sys.argv) > 1:
        test_suite=unittest.TestSuite()
        test_suite.addTest(eval(sys.argv[1])())
    else:
        test_suite = suite()
    runner.run(test_suite)
