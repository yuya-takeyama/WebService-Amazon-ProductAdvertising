# -*- coding: utf-8 -*-

import unittest
import sys
import os
from time import strftime, gmtime
from urllib2 import quote
sys.path.append('../lib')
from webservice import amazon

# You have to save keys on textfiles.
dir = os.path.dirname(os.path.abspath(__file__))
LICENSE_KEY        = open(dir + '/license_key.dat').read().rstrip()
SECRET_LICENSE_KEY = open(dir + '/secret_license_key.dat').read().rstrip()

class ProductAdvertisingTestCase(unittest.TestCase):

  def setUp(self):
    self.pa = amazon.ProductAdvertising(
      licenseKey       = LICENSE_KEY,
      secretLicenseKey = SECRET_LICENSE_KEY,
      locale           = 'jp'
    )

  def testLicenseKey(self):
    self.assertEqual(self.pa.getLicenseKey(), LICENSE_KEY, "getLicenseKey is exact.")
    self.pa.setLicenseKey("changed license key")
    self.assertEqual(self.pa.getLicenseKey(), "changed license key", "setLicenseKey is exact.")

  def testSecretLicenseKey(self):
    self.assertEqual(self.pa.getSecretLicenseKey(), SECRET_LICENSE_KEY, "getSecretLicenseKey is exact.")
    self.pa.setSecretLicenseKey("changed secret license key")
    self.assertEqual(self.pa.getSecretLicenseKey(), "changed secret license key", "setSecretLicenseKey is exact.")

  def testLocale(self):
    self.assertEqual(self.pa.getLocale(), "jp", "getLocale is exact.")
    self.pa.setLocale("us")
    self.assertEqual(self.pa.getLocale(), "us", "setLocale is exact.")

  def testMakeUrl(self):
    timestamp    = self.pa.getTimestamp()
    encTimestamp = quote(str(timestamp))
    self.assert_(self.pa.makeUrl(Timestamp=timestamp).startswith("http://ecs.amazonaws.jp/onca/xml?AWSAccessKeyId=" + LICENSE_KEY + "&Service=AWSECommerceService&Timestamp=" + encTimestamp))
    self.pa.setLocale("ca")
    self.assert_(self.pa.makeUrl(Timestamp=timestamp).startswith("http://ecs.amazonaws.ca/onca/xml?AWSAccessKeyId=" + LICENSE_KEY + "&Service=AWSECommerceService&Timestamp=" + encTimestamp))
    self.pa.setLocale()
    self.assert_(self.pa.makeUrl(Timestamp=timestamp).startswith("http://ecs.amazonaws.com/onca/xml?AWSAccessKeyId=" + LICENSE_KEY + "&Service=AWSECommerceService&Timestamp=" + encTimestamp))

  def testCallItemLookup(self):
    item = self.pa.call('ItemLookup', ItemId='B0007OH64W').Items[0].Item[0]
    attr = item.ItemAttributes[0]
    self.assertEqual(item.ASIN[0].getData(), 'B0007OH64W')
    self.assertEqual(attr.Artist[0].getData(), 'Pentagram')
    self.assertEqual(attr.Title[0].getData(), 'Relentless')

  def testCallItemSearch(self):
    elem = self.pa.call("ItemSearch", SearchIndex='Music', Keywords='Pentagram')
    self.assertEqual(elem.Items[0].Request[0].IsValid[0].getData(), "True")

unittest.main()
