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
        """Add, Modify, Build, Remove projects"""
        s = automat.Server("127.0.0.1", 8080)
        with self.assertRaises(automat.ProjectNotFound) as cm:
            p = s.GetProject("brand-new-project")
        self.assertEqual(cm.exception.code, 404)
        # Create a new Project
        p = automat.Project("brand-new-project")
        p.AddComponent("src/github.com/soccasys/automat", "https://github.com/soccasys/automat.git", "master")
        p.AddComponent("src/github.com/soccasys/automat-server", "https://github.com/soccasys/automat-server.git", "master")
        p.AddStep("Build All", ".", [ "go", "install", "github.com/soccasys/automat-server"], {})
        self.assertEqual(p.name, "brand-new-project")
        self.assertTrue("src/github.com/soccasys/automat-server" in p.components)
        self.assertTrue("src/github.com/soccasys/automat" in p.components)
        self.assertTrue(len(p.steps) == 1)
        self.assertEqual(p.steps[0].directory, ".")
        self.assertTrue(len(p.steps[0].command) == 3)
        self.assertEqual(p.steps[0].command[0], "go")
        self.assertEqual(p.steps[0].command[1], "install")
        self.assertEqual(p.steps[0].command[2], "github.com/soccasys/automat-server")
        s.PutProject(p)
        # Retrieve and verify the new project from the server
        p2 = s.GetProject("brand-new-project")
        self.assertEqual(p2.name, "brand-new-project")
        self.assertTrue("src/github.com/soccasys/automat-server" in p2.components)
        self.assertTrue("src/github.com/soccasys/automat" in p2.components)
        self.assertTrue(len(p2.steps) == 1)
        self.assertEqual(p2.steps[0].directory, ".")
        self.assertTrue(len(p2.steps[0].command) == 3)
        self.assertEqual(p2.steps[0].command[0], "go")
        self.assertEqual(p2.steps[0].command[1], "install")
        self.assertEqual(p2.steps[0].command[2], "github.com/soccasys/automat-server")
        # Update the project
        p2.steps[0].description = "Modified text"
        p2.Put()
        p3 = s.GetProject("brand-new-project")
        self.assertEqual(p3.steps[0].description, "Modified text")
        self.assertEqual(p3.name, "brand-new-project")
        self.assertTrue("src/github.com/soccasys/automat-server" in p3.components)
        self.assertTrue("src/github.com/soccasys/automat" in p3.components)
        self.assertTrue(len(p3.steps) == 1)
        self.assertEqual(p3.steps[0].directory, ".")
        self.assertTrue(len(p3.steps[0].command) == 3)
        self.assertEqual(p3.steps[0].command[0], "go")
        self.assertEqual(p3.steps[0].command[1], "install")
        self.assertEqual(p3.steps[0].command[2], "github.com/soccasys/automat-server")
        # Build the project, without setting the environment variable => FAILURE
        r = p2.Build()
        self.assertEqual(r.name, "brand-new-project")
        self.assertTrue(r.duration > 0)
        self.assertTrue("src/github.com/soccasys/automat-server" in r.components)
        self.assertTrue(r.components["src/github.com/soccasys/automat-server"].duration > 0)
        self.assertTrue(r.components["src/github.com/soccasys/automat-server"].status == "BUILD_OK")
        self.assertTrue("src/github.com/soccasys/automat" in r.components)
        self.assertTrue(r.components["src/github.com/soccasys/automat"].duration > 0)
        self.assertTrue(r.components["src/github.com/soccasys/automat"].status == "BUILD_OK")
        self.assertTrue(len(r.steps) == 1)
        self.assertEqual(r.steps[0].directory, ".")
        self.assertEqual(r.steps[0].status, "BUILD_FAILED")
        self.assertTrue(len(r.steps[0].command) == 3)
        self.assertEqual(r.steps[0].command[0], "go")
        self.assertEqual(r.steps[0].command[1], "install")
        self.assertEqual(r.steps[0].command[2], "github.com/soccasys/automat-server")
	# TODO Build the project, with the environment variable => SUCCESS
        p2 = automat.Project("brand-new-project")
        p2.AddComponent("src/github.com/soccasys/automat", "https://github.com/soccasys/automat.git", "master")
        p2.AddComponent("src/github.com/soccasys/automat-server", "https://github.com/soccasys/automat-server.git", "master")
        p2.AddStep("Build All", ".", [ "go", "install", "github.com/soccasys/automat-server"], {'GOPATH': '$BUILD_ROOT'})
	s.PutProject(p2)
	r = p2.Build()
        self.assertEqual(r.steps[0].status, "BUILD_OK")
        # Delete the project
        s.DeleteProject("brand-new-project")
        with self.assertRaises(automat.ProjectNotFound) as cm:
            p4 = s.GetProject("brand-new-project")
        self.assertEqual(cm.exception.code, 404)

class AUTOMAT_BFT_002(AutomatTestCase):
    def runTest(self):
        """Error handling in the server"""
        s = automat.Server("127.0.0.1", 8080)
        with self.assertRaises(automat.ProjectNotFound) as cm:
            p = s.GetProject("does-not-exist")
        self.assertEqual(cm.exception.code, 404)
        p = automat.Project("does-not-exist", s.automat)
        with self.assertRaises(automat.ProjectNotFound) as cm:
            p.Build()
        self.assertEqual(cm.exception.code, 404)
        with self.assertRaises(automat.ProjectNotFound) as cm:
            p = s.GetProject("another/invalid/name")
        self.assertEqual(cm.exception.code, 404)

def suite():
    suite=unittest.TestSuite()
    suite.addTest(AUTOMAT_BFT_001())
    suite.addTest(AUTOMAT_BFT_002())
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
