import unittest

from zope.configuration.xmlconfig import XMLConfig
from zope.interface import implements
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserPublisher

from zope.container.interfaces import IItemContainer
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ItemTraverser
from zope.container.testing import ContainerPlacelessSetup


class ZCMLDependencies(ContainerPlacelessSetup, unittest.TestCase):

    def test_zcml_can_load(self):
        # this is just an example.  It is supposed to show that the
        # configure.zcml file has loaded successfully.

        import zope.container
        XMLConfig('configure.zcml', zope.container)()

        request = TestRequest()

        class SampleItemContainer(object):
            implements(IItemContainer)

        sampleitemcontainer = SampleItemContainer()
        res = zope.component.getMultiAdapter(
            (sampleitemcontainer, request), IBrowserPublisher)
        self.failUnless(isinstance(res, ItemTraverser))
        self.failUnless(res.context is sampleitemcontainer)

        class SampleSimpleReadContainer(object):
            implements(ISimpleReadContainer)

        samplesimplereadcontainer = SampleSimpleReadContainer()
        res = zope.component.getMultiAdapter(
            (samplesimplereadcontainer, request), IBrowserPublisher)
        self.failUnless(isinstance(res, ItemTraverser))
        self.failUnless(res.context is samplesimplereadcontainer)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZCMLDependencies))
    return suite


if __name__ == '__main__':
    unittest.main()
