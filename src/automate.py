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

# returns booking times in an array and appends the room number on the end
def getBookings():
	times = []
	# timeslots = []
	
	# iterate through each day
	for i in range(6):
		print("DAY: " + str(i + 1))
		rooms = getRooms()

		# for each room (room1, room2...)
		for i, room in enumerate(rooms):
			print("room: " + str(i))

			# for each cell/timeslot for that row/room
			for timeslot in room:
				# process the alt text to determine if its booked or not
				col = timeslot.get_attribute('alt').split(" ")
				if len(col) == 3:
					timeparts = col[0].split(":")
					if int(timeparts[0]) > firstSuitableBookTime and int(timeparts[0]) < lastSuitableBookTime:
						times.append(col[0])
				else:
					# change this number if you want to do smaller or bigger room bookings 
					if len(times) >= 8:
						# will change this later to add options for picking times?
						# timeslots.append(times)

						# add the room number
						times.append(1434+i)
						return times
					times = []
		# if that day returned no booking slots then go to the next day
		if len(times) == 0:
			waitUntilXpathElementLoaded("//a[@title = 'Next']")
			nextButton = browser.find_element_by_xpath("//a[@title = 'Next']")
			nextButton.click()
		else:
			break
	# fallback
	return times


print("running Auto Booker...")
# hours in which to book a room
firstSuitableBookTime = 10
lastSuitableBookTime = 17

# login with provided details
f = open('loginInfo.json', 'r')
info = json.load(f)
login = info['login']
secret = info['secret']
f.close()

# open login page
browser = webdriver.Chrome()
browser.get("https://pcbooking.swin.edu.au/cire/login.aspx?ViewSimpleMode=false")

# login username
username = browser.find_element_by_id("username")
username.clear()
username.send_keys(login)

# login password
password = browser.find_element_by_id("password")
password.clear()
password.send_keys(secret)

browser.find_element_by_id("signInButton").click()

# verify we landed on the desktop page
checkPageTitle("Room and PC Booking")
waitUntilElementLoaded("locationTable")


print("attempting to extract booking data")
# get a period of appropriate bookings
timeslots = getBookings()

# get the room number off the end of the array then discard it
print("TIMESLOTS: " + str(timeslots))
roomNum = timeslots[-1]
timeslots.pop()

# figure out the range of the booking for targeting the box to click on
query = str(timeslots[0]) + " to " + str(timeslots[1])
print("QUERY: " + query)

# get the box to click on
element = browser.find_element_by_xpath("//div[@id='bookingStrip" + str(roomNum) + "']/div[@alt='" + query + "']")

# might need to scroll into view so it can be clicked on
actions = ActionChains(browser)
actions.move_to_element(element).perform()
element.location_once_scrolled_into_view

element.click()

# wait a little while cos the floating book window is a little weird sometimes 
browser.implicitly_wait(10)

# get the end time field
element = browser.find_element_by_xpath("//div[@class = 'formFieldContent']/select[@name = 'endTime']")

# select the last time from the dropdown
options = Select(element)
print(timeslots)
# NOTE TO SELF: -3 needs testing. dont thing its reliable.
options.select_by_index(len(timeslots) - 3)

# find and click the submit button
submitBtn = browser.find_element_by_xpath("//input[@id = 'submitButton']")
submitBtn.click()
