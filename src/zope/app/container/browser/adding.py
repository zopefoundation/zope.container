##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Adding View

The Adding View is used to add new objects to a container. It is sort of a
factory screen.

$Id$
"""

__docformat__ = 'restructuredtext'


from zope.app.container.constraints import checkFactory
from zope.app.container.constraints import checkObject
from zope.app.container.i18n import ZopeMessageFactory as _
from zope.app.container.interfaces import IAdding
from zope.app.container.interfaces import IContainerNamesContainer
from zope.app.container.interfaces import INameChooser
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.publisher.browser.menu import getMenu
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component.interfaces import IFactory
from zope.event import notify
from zope.exceptions.interfaces import UserError
from zope.i18n.interfaces.locales import ICollator
from zope.i18n.locales.fallbackcollator import FallbackCollator
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import LocationProxy
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser.absoluteurl import absoluteURL
import zope.security.checker

class Adding(BrowserView):
    implements(IAdding, IPublishTraverse)

    def add(self, content):
        """See zope.app.container.interfaces.IAdding
        """
        container = self.context
        name = self.contentName
        chooser = INameChooser(container)

        # check precondition
        checkObject(container, name, content)

        if IContainerNamesContainer.providedBy(container):
            # The container picks its own names.
            # We need to ask it to pick one.
            name = chooser.chooseName(self.contentName or '', content)
        else:
            request = self.request
            name = request.get('add_input_name', name)

            if name is None:
                name = chooser.chooseName(self.contentName or '', content)
            elif name == '':
                name = chooser.chooseName('', content)
            chooser.checkName(name, content)

        container[name] = content
        self.contentName = name # Set the added object Name
        return container[name]

    contentName = None # usually set by Adding traverser

    def nextURL(self):
        """See zope.app.container.interfaces.IAdding"""
        return absoluteURL(self.context, self.request) + '/@@contents.html'

    # set in BrowserView.__init__
    request = None
    context = None

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        if '=' in name:
            view_name, content_name = name.split("=", 1)
            self.contentName = content_name

            if view_name.startswith('@@'):
                view_name = view_name[2:]
            return getMultiAdapter((self, request), name=view_name)

        if name.startswith('@@'):
            view_name = name[2:]
        else:
            view_name = name

        view = queryMultiAdapter((self, request), name=view_name)
        if view is not None:
            return view

        factory = queryUtility(IFactory, name)
        if factory is None:
            return super(Adding, self).publishTraverse(request, name)

        return factory

    def action(self, type_name='', id=''):
        if not type_name:
            raise UserError(_(u"You must select the type of object to add."))

        if type_name.startswith('@@'):
            type_name = type_name[2:]

        if '/' in type_name:
            view_name = type_name.split('/', 1)[0]
        else:
            view_name = type_name

        if queryMultiAdapter((self, self.request),
                                  name=view_name) is not None:
            url = "%s/%s=%s" % (
                absoluteURL(self, self.request), type_name, id)
            self.request.response.redirect(url)
            return

        if not self.contentName:
            self.contentName = id

        # TODO: If the factory wrapped by LocationProxy is already a Proxy,
        #       then ProxyFactory does not do the right thing and the
        #       original's checker info gets lost. No factory that was
        #       registered via ZCML and was used via addMenuItem worked
        #       here. (SR)
        factory = getUtility(IFactory, type_name)
        if not type(factory) is zope.security.checker.Proxy:
            factory = LocationProxy(factory, self, type_name)
            factory = zope.security.checker.ProxyFactory(factory)
        content = factory()

        # Can't store security proxies.
        # Note that it is important to do this here, rather than
        # in add, otherwise, someone might be able to trick add
        # into unproxying an existing object,
        content = removeSecurityProxy(content)

        notify(ObjectCreatedEvent(content))

        self.add(content)
        self.request.response.redirect(self.nextURL())

    def nameAllowed(self):
        """Return whether names can be input by the user."""
        return not IContainerNamesContainer.providedBy(self.context)

    menu_id = None
    index = ViewPageTemplateFile("add.pt")

    def addingInfo(self):
        """Return menu data.

        This is sorted by title.
        """
        container = self.context
        result = []
        for menu_id in (self.menu_id, 'zope.app.container.add'):
            if not menu_id:
                continue
            for item in getMenu(menu_id, self, self.request):
                extra = item.get('extra')
                if extra:
                    factory = extra.get('factory')
                    if factory:
                        factory = getUtility(IFactory, factory)
                        if not checkFactory(container, None, factory):
                            continue
                        elif item['extra']['factory'] != item['action']:
                            item['has_custom_add_view']=True
                # translate here to have a localized sorting
                item['title'] = zope.i18n.translate(item['title'],
                                                    context=self.request)
                result.append(item)

        # sort the adding info with a collator instead of a basic unicode sort
        collator = queryAdapter(self.request.locale, ICollator)
        if collator is None:
            collator = FallbackCollator(self.request.locale)
        result.sort(key = lambda x: collator.key(x['title']))
        return result

    def isSingleMenuItem(self):
        "Return whether there is single menu item or not."
        return len(self.addingInfo()) == 1

    def hasCustomAddView(self):
       "This should be called only if there is `singleMenuItem` else return 0"
       if self.isSingleMenuItem():
           menu_item = self.addingInfo()[0]
           if 'has_custom_add_view' in menu_item:
               return True
       return False
