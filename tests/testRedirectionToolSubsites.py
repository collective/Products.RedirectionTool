import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import RedirectionToolTestCase
import utils
from Products.CMFPlone.browser.interfaces import INavigationRoot
from zope.interface import alsoProvides

class StructMaker:
    # creates a plone folder/document structre from a pattern
    
    def __init__(self, struct, root):
        self.items = struct.splitlines()
        parent=root
        lastrow = self.addFolder(parent, 0)
                
    def addFolder(self, parent, row):
        startnesting=self.getNesting(row)
        name, navRoot = self.getDetails(row)
        closing = False;
        #this folder will become new parent for included content
        parent = utils.makeContent(parent, 'Folder', name)
        if navRoot:
            alsoProvides(parent,INavigationRoot)
        while not closing:
            row+=1
            if self.isFolder(row):
                row = self.addFolder(parent, row)
            else:
                name, navRoot = self.getDetails(row)
                item = utils.makeContent(parent, 'Document', name)
                if navRoot:
                    alsoProvides(item, INavigationRoot) 
            closing = self.isClosing(row, startnesting)       
        return row
        
    def getDetails(self, row):
        symbols = self.items[row].strip().split()
        name = symbols[0]; navRoot= '+' in symbols
        return name, navRoot
                 
    def getNesting(self, rowIndex):
        curRow = self.items[rowIndex]
        curNest = 0;         
        while curRow.strip() and curRow[curNest] == ' ': 
            curNest += 1
        return curNest
                        
    def isFolder(self, rowIndex):
        return self.getNesting(rowIndex+1) > self.getNesting(rowIndex)

    def isClosing(self, rowIndex, startnesting):
        return self.getNesting(rowIndex+1) <= startnesting
        
     
class TestRedirectionToolSubsites(RedirectionToolTestCase.RedirectionToolTestCase):
    
    struct = """sites   
      realtor +
        houses
          firstSt
          gardenRow
        bungalows
          lakesideView
      carDealer +
        sportsCars
          porsche
        familyCars
          fordGranada

    """ # that empty line is needed
        
    # Test helper methods
    def testExtractReferenceFromNonExistingString(self):
        self.failUnlessRaises(NameError, self.rt.extractReference, 'nonexisting')
        
    def testStructMaker(self):
        self.loginAsPortalOwner()
        struct=StructMaker(self.struct, self.portal)
        self.logout()
        
    def testAliasByPath(self):
        self.loginAsPortalOwner()
        struct=StructMaker(self.struct, self.portal)
        homesurl="/homes"
        housesobj=self.portal.sites.realtor.houses
        self.failUnless(self.rt.addRedirect(homesurl, self.portal.portal_url.getRelativeContentURL(housesobj)))
        self.failUnless(self.rt.getRedirect(homesurl))
        
        self.failUnlessEqual(self.rt.getRedirectObject(homesurl), housesobj)
        self.failUnless(self.rt.getRedirect(homesurl+'/'))
        self.failUnlessEqual(self.rt.getRedirectObject(homesurl+'/'), housesobj)
        self.logout()
        


if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    from unittest import TestSuite, makeSuite
    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestRedirectionToolSubsites))
        return suite
