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
# for passing options into chromedriver
from selenium.webdriver.chrome.options import Options
import os
import json


def waitUntilElementLoaded(element):
	try:
		WebDriverWait(browser, 10).until(
			EC.presence_of_all_elements_located((By.CLASS_NAME, element)))
		element = browser.find_element_by_class_name(element)
		return element
	except:
		printAndLog("ERROR: timed out waiting for " + str(element), debugFile)


def waitUntilIDLoaded(element):
	try:
		wait.until(EC.presence_of_all_elements_located((By.ID, element)))
		element = browser.find_element_by_id(element)
		return element
	except:
		printAndLog("ERROR: timed out waiting for " + str(element), debugFile)


def waitUntilXpathElementLoaded(path):
	try:
		#printAndLog("waiting for " + path, debugFile)
		wait.until(EC.presence_of_all_elements_located((By.XPATH, path)))
		element = browser.find_element_by_xpath(path)
		return element
	except:
		printAndLog("ERROR: timed out waiting for " + str(element), debugFile)


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


def getLoginDetails(path):
	try:
		info = json.load(open(path, 'r'))
		return info['login'], info['secret']
	except:
		printAndLog("failed to read info", debugFile)


def printAndLog(output, file):
	file.write(output+"\n")
	print(output)


# returns booking times in an array and appends the room number on the end
def getBookings():
	times = []

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
				if (len(col) == 3 and len(times) <= 8):
					timeparts = col[0].split(":")
					if int(timeparts[0]) > firstSuitableBookTime and int(timeparts[0]) < lastSuitableBookTime:
						times.append(col[0])
				else:
					# change this number if you want to do smaller or bigger room bookings
					if len(times) >= bookingLengthBlocks:
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


def fieldWrite(fieldID, keys):
	field = browser.find_element_by_id(fieldID)
	field.clear()
	field.send_keys(keys)


print("running Auto Booker...")
# hours in which to book a room
firstSuitableBookTime = 10
lastSuitableBookTime = 17
bookingLengthBlocks = 8

# open the log file for writing
debugFile = open('log.txt', 'w')

# login with provided details
# /home/roland/projects/login.json
login, secret = getLoginDetails('login.json')

# for running headless
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

browser = webdriver.Chrome(
	executable_path="webdriver/ubuntu/chromedriver", options=options)
browser.implicitly_wait(600)
wait = WebDriverWait(browser, 10)

# open login page
browser.get("https://pcbooking.swin.edu.au/cire/login.aspx?ViewSimpleMode=false")
printAndLog("going to login page", debugFile)

# login
printAndLog("writing username and secret", debugFile)
fieldWrite("username", login)
fieldWrite("password", secret)

# signInButton
printAndLog("clicking sign in button", debugFile)
waitUntilIDLoaded("signInButton").click()

# verify we landed on the desktop page
try:
	checkPageTitle("Room and PC Booking")
	waitUntilElementLoaded("locationTable")
	printAndLog("landed on booking table", debugFile)
except:
	printAndLog("didnt land on the booking page", debugFile)

# get a period of appropriate bookings
try:
	timeslots = getBookings()
	# get the room number at the end of the array then discard it
	roomNum = timeslots[-1]
	timeslots.pop()
	printAndLog("Room number: " + str(roomNum), debugFile)
	printAndLog("Timeslots: " + str(timeslots), debugFile)
except:
	printAndLog("ERROR: didnt get any bookings!", debugFile)

# form the alt text for the first booking
query = str(timeslots[0]) + " to " + str(timeslots[1])

# get the box to click on
try:
	printAndLog("getting the box to click on", debugFile)
	element = browser.find_element_by_xpath(
		"//div[@id='bookingStrip" + str(roomNum) + "']/div[@alt='" + query + "']")
except:
	printAndLog("ERROR: Couldnt find booking box to click on", debugFile)

# try and click on the element
try:
	# might need to scroll into view so it can be clicked on
	printAndLog("scrolling to location of booking slot", debugFile)
	actions = ActionChains(browser)
	actions.move_to_element(element).perform()
	element.location_once_scrolled_into_view
	element.click()
except:
	printAndLog("ERROR: couldnt click on the booking", debugFile)

# wait a little while cos the floating book window is a little weird sometimes
browser.implicitly_wait(5000)

# get the end time field
printAndLog("getting the end time dropdown", debugFile)
query = "//div[@class='formFieldContent']/select[@name='endTime']"
select = Select(waitUntilXpathElementLoaded(query))
printAndLog("selecting latest timeslot: " + timeslots[-1], debugFile)
select.select_by_visible_text(str(timeslots[-1]))

browser.implicitly_wait(5000)
# find and click the submit button
printAndLog("finding and clicking the submit button", debugFile)
staleElement = True
attempts = 0
while (staleElement and attempts < 100):
	try:
		waitUntilXpathElementLoaded("//input[@name = 'submitButton']").click()
		staleElement = False
		#printAndLog("submit button clicked", debugFile)
	except:
		printAndLog("ERROR: Stale element. attempt " + str(attempts), debugFile)
		attempts += 1
		browser.implicitly_wait(5000)
printAndLog("Clicked book!", debugFile)
browser.quit()
