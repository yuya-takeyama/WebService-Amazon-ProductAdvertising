# -*- coding: utf-8 -*-
"""
Much of this program is quoted from "Python Cookbook, 2nd Edition" p.479 (O'Reilly Japan).
Only the method Element.__getattr__ is written by me.
And changed to encode strings to UTF-8.
"""

from xml.parsers import expat

class Element(object):

  def __init__(self, name, attributes):
    self.name = name
    self.attributes = attributes
    self.cdata = ''
    self.children = []

  def __getattr__(self, key):
    return self.getElements(key)

  def addChild(self, element):
    self.children.append(element)

  def getAttribute(self, key):
    return self.attributes.get(key)

  def getData(self):
    return self.cdata

  def getElements(self, name=''):
    if name:
      return [child for child in self.children if child.name == name]

class Xml2Obj(object):

  def __init__(self):
    self.root = None
    self.nodeStack = []

  def StartElement(self, name, attributes):
    attributes = dict([(key, attributes[key].encode("utf-8")) for key in attributes])
    element = Element(name.encode("utf-8"), attributes)
    if self.nodeStack:
      parent = self.nodeStack[-1]
      parent.addChild(element)
    else:
      self.root = element
    self.nodeStack.append(element)

  def EndElement(self, name):
    # self.nodeStack[-1].pop()
    # I think following is exact.
    self.nodeStack.pop()

  def CharacterData(self, data):
    if data.strip():
      data = data.encode("utf-8")
      element = self.nodeStack[-1]
      element.cdata += data

  def parse(self, string):
    Parser = expat.ParserCreate()
    Parser.StartElementHandler = self.StartElement
    Parser.EndElementHandler = self.EndElement
    Parser.CharacterDataHandler = self.CharacterData
    ParserStatus = Parser.Parse(string, True)
    return self.root
