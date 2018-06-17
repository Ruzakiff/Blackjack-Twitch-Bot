#!/bin/env python3.6
import pyautogui
import sys

hitImage="/users/ryan/Desktop/grunt2/resources/blackhit.png"

while True:
	#hitlocation=pyautogui.locateCenterOnScreen(hitImage,region=(440,533, 300, 300))
	hitlocation=pyautogui.locateCenterOnScreen(hitImage,region=(900,1090, 300, 300))
	print (hitlocation)
	if hitlocation!=None:
		print (hitlocation)
		temp=list(hitlocation)
		temp[0]=int(temp[0]/2)
		temp[1]=int(temp[1]/2)
		middle=tuple(temp)
		print (middle)
		pyautogui.click(middle)