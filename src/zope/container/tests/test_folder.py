from unittest import TestCase, makeSuite

from zope.container.folder import Folder

from zope.container.tests.test_icontainer import BaseTestIContainer
from zope.container.tests.test_icontainer import DefaultTestData


class Test(BaseTestIContainer, TestCase):

    def makeTestObject(self):
        return Folder()

    def makeTestData(self):
        return DefaultTestData()

    def getUnknownKey(self):
        return '10'

    def getBadKeyTypes(self):
        return [None, ['foo'], 1, '\xf3abc']

def test_suite():
    return makeSuite(Test)

