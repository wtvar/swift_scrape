#! /usr/bin/python3

import re
import datetime
import csv
import requests
import sys
import logging
import time
import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#webdriver path
#DRIVER_PATH = 'C:\\Users\\user\\Downloads\\chromedriver87\\chromedriver.exe' #driver path for windows laptop
DRIVER_PATH = "C:\\Users\\chris\\Desktop\\python\\chromedriver\\chromedriver.exe" #driver path for windows pc
#DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'	#driver path for pi/linux

index_url = "https://www.swiftqueue.co.uk/westsuffolk.php"



""" logging details"""
# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='C:\\Users\\chris\\Desktop\\python\\inplay\\inplay.log',
                    #filename="/home/pi/python/inplay/inplay.log",\
                    filemode='a')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Start of logging.')

# Now, define a couple of other loggers which might represent areas in your file
logger1 = logging.getLogger('my swiftqueue logger')

"""logging end"""

""" start of program"""

#press link that takes us to page
#<a class="btn btn-lg rounded sq-green btn-block"

"""options for webdriver"""
"""options = Options()
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": download_folder, # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)"""
#options.headless = True
#options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(index_url)

#click on link for blood test site
submit = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/a').click()
logging.info('pressed on link')
#check if success?
try:
	#see if the settings button is showing. if so, then we have successfully logged in
	logout_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div[2]/div[1]/h3')
	logging.info('Sucessfully navigated to site')
except NoSuchElementException:
	#if there is no logout button, we havent logged in successfully
	logging.debug('Error when navigating to site')



""" pseudo code
go to link
press link
check it worked. how?
see the current dates
pick earliest date
if date is before certain date. how?
give us a message with link to book
"""
