# -*- coding: iso-8859-15 -*-

##########################################################################
# z3c.sqlalchemy - A SQLAlchemy wrapper for Python/Zope
#
# (C) Zope Corporation and Contributor
# Written by Andreas Jung for Haufe Mediengruppe, Freiburg, Germany
# and ZOPYX Ltd. & Co. KG, Tuebingen, Germany
##########################################################################


"""
Tests, tests, tests.........
"""

import unittest

from Products.SmartPrintNG.converter.manipulation import breakIntoPages, enumerateLinksInHtml, getLinksInHtml 
from Products.SmartPrintNG.converter.manipulation import removeLinks

html = """
<a href="http://www.heise.de" />HEISE</A>
<a href="@@control-panel" > Control Panel</a>
<a HREF="#anchor">
<a href="http://www.heise.de#anchor" />HEISE</A>
<A   HrEF="/foo/bar" />foo bar</A>
<a href="http://foo.com"><em>bar</em></a>
"""


class ManipulationTests(unittest.TestCase):

    def testGeLinks(self):
        links = getLinksInHtml(html)    
        self.assertEqual(links, ['http://www.heise.de',
                                 'http://www.heise.de#anchor',
                                 '/foo/bar',                  
                                 'http://foo.com',
                                ])

    def testEnumerateLinks(self):
        links = getLinksInHtml(html)
        html2 = enumerateLinksInHtml(html, links)
        self.assertEqual('HEISE [1]' in html2, True)
        self.assertEqual('HEISE [2]' in html2, True)
        self.assertEqual('foo bar [3]' in html2, True)
        self.assertEqual('bar [4]' in html2, True)


    def testBreakIntoPages(self):
        html = """<h1>hello world </h1><div>foo bar</div>\n
        <H1>Chapter 2</h1><div>chapter 2 goes here</div>"""

        result = breakIntoPages(html)
        self.assertEqual(result, '<div class="chapter sp-page"><h1>hello world </h1><div>foo bar</div></div>\n'\
                                 '<div class="chapter"><H1>Chapter 2</h1><div>chapter 2 goes here</div></div>')

    def testRemoveLink(self):
        result = removeLinks(html)
        self.assertEqual('<span>HEISE</span>' in result, True)
        self.assertEqual('<span>Control Panel</span>' in result, True)
        self.assertEqual('<span>foo bar</span>' in result, True)




def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ManipulationTests))
    return suite

