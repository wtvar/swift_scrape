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
from settings import TELEGRAM_TOKEN
from settings import my_telegram_id

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
#TODO: check i need all these imports

"""
https://www.programiz.com/python-programming/datetime/strptime
datetime get date from Mon, 04 May

"""
#webdriver path
#DRIVER_PATH = 'C:\\Users\\user\\Downloads\\chromedriver87\\chromedriver.exe' #driver path for windows laptop
DRIVER_PATH = "C:\\Users\\chris\\Desktop\\python\\chromedriver\\chromedriver.exe" #driver path for windows pc
#DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'	#driver path for pi/linux

index_url = "https://www.swiftqueue.co.uk/westsuffolk.php" #TODO: ask for link?
date_to_check = '2021-04-22' #TODO: ask for date?

#telegram login details
#imported from settings.py now

""" logging details"""
# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='C:\\Users\\chris\\Desktop\\python\\swiftqueueswiftqueue.log',
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
def telegram_send(message):
	""" sends a telegram message """
	requests.get("https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage?chat_id=" + my_telegram_id + "&text={}".format(message))

"""options for webdriver"""
"""options = Options()
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": download_folder, # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)"""
#options.headless = True
#options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(DRIVER_PATH)
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

timings = []
logging.info('empty list made')
time.sleep(5) #TODO: do i need this?
try:
    list_of_times = driver.find_element_by_xpath('//*[@id="timescreen"]/div[1]/h3').text
    logging.info('looking for dates on site')
except:
    logging.info('unable to find dates')

print('##############################')
print(f' date found is {list_of_times}')
print('##############################')
print(f'type is {type(list_of_times)}')
print('##############################')
print(f'text of date is {list_of_times}')
print('##############################')

list_of_times += ' 2021' #adding 2021 as the date doesnt have this
dt_obj = datetime.datetime.strptime(list_of_times, '%a, %d %b %Y') #making into datetime object
date_proper_format = datetime.datetime.strptime(date_to_check, '%Y-%m-%d')

print(f'current time found is {dt_obj}')
print(f'time to compare to is {date_proper_format}')
current_page = driver.current_url

if dt_obj < date_proper_format:
	print('date is good')
	try:
        telegram_send(f'appointment is available on {dt_obj} \n {current_page}')
        logging.info('telegram message sent')
    except:
        logging.info('unable to send telegram message')
else:
	print('date is bad')
	

	
""" pseudo code

go to link [x]
press link [x]
check it worked. [x]
see the current dates [x]
pick earliest date [x]
convert to datetime [x]
if date is before certain date. [x]
give us a message with link to book [x]

TODO:
get several available times if these are all before my given date [ ]
give the available times as well as just the date [ ]
set a time of day for appointment we want [ ]
compare the time available to time set at start [ ]

"""
