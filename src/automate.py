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


def waitUntilIDLoaded(element):
	try:
    		element = WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located(
                    	(By.ID, element))
                )
	finally:
    		browser.quit

def waitUntilXpathElementLoaded(path):
	try:
    		WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located(
                    	(By.XPATH, path))
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

def getDailyBookings():
	room1 = browser.find_elements_by_css_selector("#bookingStrip1434 .ts")
	times = []
	timeslots = []
	for i, room in enumerate(room1):
		col = room.get_attribute('alt').split(" ")
	if len(col) == 3:
		timeparts = col[0].split(":")
		print(timeparts)
		if int(timeparts[0]) > firstSuitableBookTime and int(timeparts[0]) < lastSuitableBookTime:
			times.append(col[0])
	else:
		if len(times) != 0:
			timeslots.append(times)
		times = []
	return timeslots 

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


# f = open("output.txt", "w")
# print(browser.find_element_by_tag_name("title"))
print("attempting to extract booking data")

# query = "disableGrid();retrieveHtmlFromUrl(\'bookingGrid\',\'Front.aspx?page=bookingGrid&date=26/08/2019\', \'adjustBookingGridView();\'); return false;"

# room2 = browser.find_elements_by_css_selector("#bookingStrip1435 .ts")
# room3 = browser.find_elements_by_css_selector("#bookingStrip1435 .ts")
# room4 = browser.find_elements_by_css_selector("#bookingStrip1435 .ts")

# go to the next day





firstSuitableBookTime = 9
lastSuitableBookTime = 24
# def satisfyTime(time1, time2, length):
# 	print(time1 + "\n")
# 	print(time2 + "\n")
# 	return False


for i in range(6):
	print("test1")
	waitUntilIDLoaded("bookingGridContent")
	print("test2")
	timeslots = getDailyBookings()
	print("test3")
	waitUntilXpathElementLoaded("//a[@title = 'Next']")
	print("test4")
	nextButton = browser.find_element_by_xpath("//a[@title = 'Next']")
	print("test5")
	nextButton.click()
	


# for time in timeslots:
# 	if time[0] > 
print(timeslots)
