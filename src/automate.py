from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json


def waitUntilElementLoaded(element):
	try:
    		element = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, element))
    	)
	finally:
    		browser.quit


def checkPageTitle(title):
	try:
    		WebDriverWait(browser, 10).until(
                    EC.title_is(title)
            )
	finally:
    		browser.quit
	
	print(title + " passed validation ")


def get_rows():
	return browser.find_elements_by_css_selector("#tsWht")

print("start: ")
f = open('loginInfo.json', 'r')
info = json.load(f)
login = info['login']
secret = info['secret']

browser = webdriver.Chrome()
browser.get("https://pcbooking.swin.edu.au/cire/login.aspx?ViewSimpleMode=false")



username = browser.find_element_by_id("username")
username.clear()
username.send_keys(login)

password = browser.find_element_by_id("password")
password.clear()
password.send_keys(secret)

browser.find_element_by_id("signInButton").click()

checkPageTitle("Room and PC Booking")
waitUntilElementLoaded("locationTable")


f = open("output.txt", "w")
# print(browser.find_element_by_tag_name("title"))
print("attempting to extract booking data")

room1 = browser.find_elements_by_css_selector("#bookingStrip1434 .ts")

for room in room1:
	col = room.get_attribute('alt')
	f.write(col + "\n")
	print(col)
