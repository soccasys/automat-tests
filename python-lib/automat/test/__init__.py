import unittest
import sys
import subprocess
import time

class FormattedTestRunner:

    def __init__(self, stream=sys.stderr):
        self.stream = stream

    def writeUpdate(self, message):
        self.stream.write(message)

    def run(self, test):
        "Run the given test case or test suite."
        result = _FormattedTestResult(self)
        startTime = time.time()
        self.writeUpdate("\n")
        self.writeUpdate("Test ID              Description                                             Result Duration\n")
        self.writeUpdate("==================== ======================================================= ====== ==========\n")
        test(result)
        stopTime = time.time()
        timeTaken = float(stopTime - startTime)
        self.writeUpdate("\n")
        result.printErrors()
        run = result.testsRun
        self.writeUpdate("\n")
        return result
    

def format_string(text, length):
    if len(text) > length:
        return text[:length]
    else:
        return text + (length-len(text))*" "

class _FormattedTestResult(unittest.TestResult):
    """A test result class that can print

    FormattedTestRunner.
    """

    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.start = time.time()
        # we should escape quotes here
        self.runner.writeUpdate('%s %s ' %
                                (format_string(test.__class__.__name__, 20), format_string(test.shortDescription(),55)))

    def addSuccess(self, test):
        self.stop = time.time()
        unittest.TestResult.addSuccess(self, test)
        self.runner.writeUpdate('PASS   %d secs\n' % int(self.stop-self.start))

    def addError(self, test, err):
        self.stop = time.time()
        unittest.TestResult.addError(self, test, err)
        self.runner.writeUpdate('ERROR  %d secs\n' % int(self.stop-self.start))

    def addFailure(self, test, err):
        self.stop = time.time()
        unittest.TestResult.addFailure(self, test, err)
        self.runner.writeUpdate('FAIL   %d secs\n' % int(self.stop-self.start))

    def printErrors(self):
        self.printErrorList('Error', self.errors)
        self.printErrorList('Failure', self.failures)

    def printErrorList(self, flavor, errors):
        
        for test, err in errors:
            self.runner.writeUpdate('%s %s\n' %
                                    (test.__class__.__name__, flavor))
            lines = err.split('\n')
            for line in lines:
                self.runner.writeUpdate("   > %s\n" % line)
            self.runner.writeUpdate("\n")

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def runCmd(self, command_and_args):
        return subprocess.check_output(command_and_args, stderr=subprocess.STDOUT)

