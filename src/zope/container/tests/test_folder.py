from unittest import TestCase, makeSuite

from zope.container.folder import Folder
from zope.container.tests.test_icontainer import TestSampleContainer


class Test(TestSampleContainer, TestCase):

    def makeTestObject(self):
        return Folder()

    def testDataAccess(self):
        folder = self.makeTestObject()
        self.assertNotEqual(folder.data, None)
        folder.data = 'foo'
        self.assertEqual(folder.data, 'foo')

def test_suite():
    return makeSuite(Test)

