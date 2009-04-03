import os
import unittest

from zope.interface import implements
import zope.component
from zope.app.testing import functional
from zope.publisher.browser import TestRequest

from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.container.traversal import ItemTraverser

ContainerLayer = functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftest_zcml_dependencies.zcml'),
    __name__, 'ContainerLayer', allow_teardown=True)


from zope.container.interfaces import IItemContainer
from zope.container.interfaces import ISimpleReadContainer

class ZCMLDependencies(functional.BrowserTestCase):

    def test_zcml_can_load_with_only_zope_component_meta(self):
        # this is just an example.  It is supposed to show that the
        # configure.zcml file has loaded successfully.

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
    ZCMLDependencies.layer = ContainerLayer
    suite.addTest(unittest.makeSuite(ZCMLDependencies))
    return suite


if __name__ == '__main__':
    unittest.main()
