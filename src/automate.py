from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# scrolling
from selenium.webdriver.common.action_chains import ActionChains
# dropdowns
from selenium.webdriver.support.ui import Select
# keyboard things
from selenium.webdriver.common.keys import Keys
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


def getRooms():
	waitUntilIDLoaded("bookingGridContent")
	room1 = browser.find_elements_by_css_selector("#bookingStrip1434 .ts")
	room2 = browser.find_elements_by_css_selector("#bookingStrip1435 .ts")
	room3 = browser.find_elements_by_css_selector("#bookingStrip1436 .ts")
	room4 = browser.find_elements_by_css_selector("#bookingStrip1437 .ts")
	room5 = browser.find_elements_by_css_selector("#bookingStrip1438 .ts")
	rooms = [room1, room2, room3, room4, room5]
	return rooms

def getBookings():
	times = []
	timeslots = []

	for i in range(6):
		print("DAY: " + str(i+1))
		rooms = getRooms()
		for i, room in enumerate(rooms):
			print("room: " + str(i))
			for timeslot in room:
				col = timeslot.get_attribute('alt').split(" ")
				if len(col) == 3:
					timeparts = col[0].split(":")
					if int(timeparts[0]) > firstSuitableBookTime and int(timeparts[0]) < lastSuitableBookTime:
						times.append(col[0])
				else:
					if len(times) >= 2:
						# will change this later to add options for picking times?
						# timeslots.append(times)

						# add the room number
						times.append(1434+i)
						return times
					times = []
		if len(timeslots) == 0:
			waitUntilXpathElementLoaded("//a[@title = 'Next']")
			nextButton = browser.find_element_by_xpath("//a[@title = 'Next']")
			nextButton.click()
		else:
			break	
	return timeslots


print("start: ")
f = open('loginInfo.json', 'r')
info = json.load(f)
login = info['login']
secret = info['secret']
f.close()

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


print("attempting to extract booking data")



firstSuitableBookTime = 10
lastSuitableBookTime = 17
# def satisfyTime(time1, time2, length):
# 	print(time1 + "\n")
# 	print(time2 + "\n")
# 	return False
timeslots = getBookings()

print("TIMESLOTS: " + str(timeslots))
roomNum = timeslots[-1]
# take the room number off the array
timeslots.pop()
query = str(timeslots[0]) + " to " + str(timeslots[1])
print("QUERY: " + query)
element = browser.find_element_by_xpath(
	"//div[@id='bookingStrip" + str(roomNum) + "']/div[@alt='" + query + "']")

# contpayment = WebDriverWait(browser, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//div[@id='bookingStrip" + str(roomNum) + "']/div[@alt='" + query + "']")))

actions = ActionChains(browser)
actions.move_to_element(element).perform()
element.location_once_scrolled_into_view

element.click()
# waitUntilXpathElementLoaded("//select[@name='EndTime']")
# waitUntilIDLoaded("EndTime")

# s = browser.find_element_by_css_selector("#ui-datepicker-div")
# browser.execute_script("document.getElementById('Dim').style.display = 'none';")
# browser.execute_script("document.getElementById('dialog0').style.display = 'fixed';")
# # browser.execute_script("document.getElementById('dialog0').style.position = 'relative';")
# browser.execute_script("document.getElementById('dialog0').style.x = '0px';")
# browser.execute_script("document.getElementById('dialog0').style.y = '0px';")
# s.send_keys(Keys.TAB)

browser.implicitly_wait(10)
element = browser.find_element_by_xpath("//div[@class = 'formFieldContent']/select[@name = 'endTime']")
print(element.text)

# s1 = Select(browser.find_element_by_id("EndTime"))
# print("options")
# print(s1.options)
# s1.select_by_visible_text(str(timeslots[-1]))
