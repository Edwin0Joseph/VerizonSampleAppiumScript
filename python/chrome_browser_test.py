import sys
import os
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
import time
import unittest
import logging
import datetime
import mysql.connector
import socket
import sh

 
from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class SimpleAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        self.device_id = str(sys.argv[1])
        desired_caps['platformName'] = 'Android'
        desired_caps['udid'] = self.device_id
        desired_caps['deviceName'] = self.device_id
        desired_caps['noReset'] = True
        desired_caps['newCommandTimeout'] = 1000
        desired_caps['browserName'] = 'Chrome'
        desired_caps['browser'] = 'Chrome'

#        desired_caps['chromedriverExecutable'] = "/home/pbox/chromedrivers/2.40/chromedriver"
#        desired_caps['headspin.appiumVersion'] = "1.8.1"
        desired_caps['headspin:capture'] = True
        desired_caps['headspin:autoDownloadChromedriver'] = True
        self.device_id = str(sys.argv[1])
        url = str(sys.argv[2])
        self.status = "Fail"

        self.driver = webdriver.Remote(url, desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get('https://fast.com')
        



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

