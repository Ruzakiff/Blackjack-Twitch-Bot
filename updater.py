import pyautogui
import schedule
import datetime

template='/users/ryan/Desktop/grunt2/resources/template.png'

def getScreen():
	pyautogui.screenshot(template)
	print ("Screen Updated:",datetime.datetime.now().strftime("%a, %d %B %Y %I:%M:%S"))

schedule.every(1).second.do(getScreen)
while 1:
	schedule.run_pending()
	