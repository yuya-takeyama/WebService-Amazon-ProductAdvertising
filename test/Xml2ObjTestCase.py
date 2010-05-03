# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('../lib')
from xml2obj import Element, Xml2Obj

class Xml2ObjTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = Xml2Obj()
    self.root = self.parser.parse("""<?xml version="1.0"?><parent id="top"><child1 name="paul">Text goes here</child1><child2 name="fred">More text</child2></parent>""")
    self.rootJp = self.parser.parse("""<?xml version="1.0"?><parent id="最上位"><child1 name="イチロー">日本語の文字列</child1><child2 name="ジロー">もうひとつ</child2></parent>""")

  def testRootIsElement(self):
    self.assert_(isinstance(self.root, Element))

  def testRootIsElementJp(self):
    self.assert_(isinstance(self.rootJp, Element))

  def testChildIsList(self):
    self.assert_(isinstance(self.root.getElements('child1'), list))
    self.assert_(isinstance(self.root.child1, list))

  def testChildIsListJp(self):
    self.assert_(isinstance(self.rootJp.getElements('child1'), list))
    self.assert_(isinstance(self.rootJp.child1, list))

  def testGetDataIsExact(self):
    self.assertEqual(self.root.getElements('child1')[0].getData(), "Text goes here")
    self.assertEqual(self.root.getElements('child2')[0].getData(), "More text")

  def testGetDataIsExactJp(self):
    self.assertEqual(self.rootJp.getElements('child1')[0].getData(), "日本語の文字列")
    self.assertEqual(self.rootJp.getElements('child2')[0].getData(), "もうひとつ")

  def testGetDataByGetattrIsExact(self):
    self.assertEqual(self.root.child1[0].getData(), "Text goes here")
    self.assertEqual(self.root.child2[0].getData(), "More text")

  def testGetDataByGetattrIsExactJp(self):
    self.assertEqual(self.rootJp.child1[0].getData(), "日本語の文字列")
    self.assertEqual(self.rootJp.child2[0].getData(), "もうひとつ")


  def testGetAttributeIsExact(self):
    self.assertEqual(self.root.getAttribute('id'), "top")
    self.assertEqual(self.root.child1[0].getAttribute('name'), "paul")
    self.assertEqual(self.root.child2[0].getAttribute('name'), "fred")

  def testGetAttributeIsExactJp(self):
    self.assertEqual(self.rootJp.getAttribute('id'), "最上位")
    self.assertEqual(self.rootJp.child1[0].getAttribute('name'), "イチロー")
    self.assertEqual(self.rootJp.child2[0].getAttribute('name'), "ジロー")

  def testAddChildIsExact(self):
    newChild = self.parser.parse("""<?xml version="1.0"?><child3 name="john">I am a new one</child3>""")
    self.root.addChild(newChild)
    self.assertEqual(self.root.getElements('child3')[0].getData(), "I am a new one")
    self.assertEqual(self.root.child3[0].getData(), "I am a new one")
    self.assertEqual(self.root.child3[0].getAttribute('name'), "john")

  def testAddChildIsExactJp(self):
    newChild = self.parser.parse("""<?xml version="1.0"?><child3 name="サブロー">新要素</child3>""")
    self.root.addChild(newChild)
    self.assertEqual(self.root.getElements('child3')[0].getData(), "新要素")
    self.assertEqual(self.root.child3[0].getData(), "新要素")
    self.assertEqual(self.root.child3[0].getAttribute('name'), "サブロー")

unittest.main()
