# -*- coding: utf-8 -*-
"""
This is an implementation of Amazon Product Advertising API in Python.

Thanks to following.
  - PyAWS
    http://pyaws.sourceforge.net/
  - python-amazon-product-api
    http://pypi.python.org/pypi/python-amazon-product-api
  - ryo_abe
    http://d.hatena.ne.jp/ryo_abe/20100416/1271384372
"""

from base64 import b64encode
import hmac
from time import strftime, gmtime
from urllib2 import quote, urlopen
from xml2obj import Xml2Obj

try:
  from hashlib import sha256
except ImportError:
  from Crypto.Hash import SHA256 as sha256
 
__author__  = "Yuya Takeyama <sign.of.the.wolf.pentagram@gmail.com>"
__version__ = "0.0.1"

DEFAULT_API_VERSION = '2009-11-01'

LOCALE_DOMAINS = {
  None : "ecs.amazonaws.com",
  "ca" : "ecs.amazonaws.ca",
  "de" : "ecs.amazonaws.de",
  "fr" : "ecs.amazonaws.fr",
  "jp" : "ecs.amazonaws.jp",
  "uk" : "ecs.amazonaws.co.uk",
  "us" : "ecs.amazonaws.us"
}

class ProductAdvertising:

  def __init__(self, licenseKey, secretLicenseKey, locale=None):
    self.setLicenseKey(licenseKey)
    self.setSecretLicenseKey(secretLicenseKey)
    self.setLocale(locale)
    self.parser = Xml2Obj()

  def call(self, operation, **kwds):
    kwds['Operation'] = operation
    url = self.makeUrl(**kwds)
    return self.parser.parse(urlopen(url).read())

  def makeUrl(self, **kwds):
    param = self.makeParam(kwds)
    signature = self.makeSignature(kwds)
    return "http://" + LOCALE_DOMAINS[self.getLocale()] + "/onca/xml?" + param + "&Signature=" + signature

  def setLicenseKey(self, licenseKey=None):
    self.__licenseKey = licenseKey
    return self

  def getLicenseKey(self):
    return self.__licenseKey

  def setSecretLicenseKey(self, secretLicenseKey=None):
    self.__secretLicenseKey = secretLicenseKey

  def getSecretLicenseKey(self):
    return self.__secretLicenseKey

  def setLocale(self, locale=None):
    self.__locale = locale
    return self

  def getLocale(self):
    return self.__locale

  def getTimestamp(self):
    return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

  def makeParam(self, args):
    for key, val in args.items():
      if val is None:
        del args[key]

    if 'Version' not in args:
      args['Version'] = DEFAULT_API_VERSION
    if 'Service' not in args:
      args['Service'] = 'AWSECommerceService'
    if 'Timestamp' not in args:
      args['Timestamp'] = self.getTimestamp()
    args['AWSAccessKeyId'] = self.getLicenseKey()

    keys = sorted(args.keys())
    return '&'.join('%s=%s' % (key, quote(str(args[key]))) for key in keys)

  def makeSignature(self, args):
    param = self.makeParam(args)
    msg = 'GET'
    msg += '\n' + LOCALE_DOMAINS[self.getLocale()]
    msg += '\n' + "/onca/xml"
    msg += '\n' + param.encode('utf-8')
    return quote(b64encode(hmac.new(self.getSecretLicenseKey(), msg, sha256).digest()))
