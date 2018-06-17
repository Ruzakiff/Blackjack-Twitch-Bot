from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
import pyautogui
import re
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

clickTarget=[]

re1='(!)'	# Any Single Character 1
re2='((?:[a-z][a-z]+))'	# Word 1

rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)


s = openSocket()
joinRoom(s)
readbuffer = ""

prefix="!"
roundTime=15
voteFile="/Users/ryan/Desktop/grunt2/votes"


def findImage(target,threshold):
	global clickTarget

	template='/users/ryan/Desktop/grunt2/resources/template.png'

	img = cv2.imread(template,0)
	img2 = img.copy()
	template = cv2.imread(target,0)
	w, h = template.shape[::-1]

	# All the 6 methods for comparison in a list
	#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
	           # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

	#for meth in methods:
	img = img2.copy()
	method = eval("cv2.TM_CCOEFF_NORMED")

	# Apply template Matching
	res = cv2.matchTemplate(img,template,method)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
	#if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
	#top_left = min_loc
	#else:
	print (max_val)
	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)

	print (top_left)
	clickTarget=list(top_left)
	clickTarget[0]=int(clickTarget[0]+(w/2))
	clickTarget[1]=int(clickTarget[1]+(h/2))

	cv2.rectangle(img,top_left, bottom_right, 255, 2)

	# plt.subplot(121),plt.imshow(res,cmap = 'gray')
	# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
	# plt.subplot(122),plt.imshow(img,cmap = 'gray')
	# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
	# plt.suptitle("cv2.TM_SQDIFF")
	# plt.show()
	if max_val<threshold:
		return False
	else:
		return True

#def main():
while True:

	if findImage('/users/ryan/Desktop/grunt2/resources/dealerwin.png',.85):
		sendMessage(s,"Dealer Won!")
		pyautogui.click()
		if findImage('/users/ryan/Desktop/grunt2/resources/placebet.png',.85):
			if findImage('/users/ryan/Desktop/grunt2/resources/deal.png',.85):
				sendMessage(s, "Deal Clicked")
				pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				sendMessage(s,"Begin New Round!")
			else:
				sendMessage(s, "Cant Find Deal Button")
				sys.exit("Could Not Find Deal Button")
	#elif findImage('/users/ryan/Desktop/grunt2/resources/sadchip.png',.85):
	#	sendMessage(s,"Out of Credits!")
		#if findImage('users/ryan/desktop/grunt2/resources/newgame.png',.85):
		#	pyautogui.click(x=clickTarget[0]/2,y=clickTarget[1]/2)
		#	sendMessage(s,"New Game Started!")
	elif findImage('/users/ryan/Desktop/grunt2/resources/win.png',.85):
		sendMessage(s,"Yay We Won!")
		pyautogui.click()
		if findImage('/users/ryan/Desktop/grunt2/resources/placebet.png',.85):
			if findImage('/users/ryan/Desktop/grunt2/resources/deal.png',.85):
				sendMessage(s, "Deal Clicked")
				pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				sendMessage(s,"Begin New Round!")
			else:
				sendMessage(s, "Cant Find Deal Button")
				sys.exit("Could Not Find Deal Button")

	readbuffer = readbuffer + s.recv(1024).decode("utf-8")
	temp = readbuffer.split("\n")
	readbuffer = temp.pop()
	for line in temp:
		print(line)
		if "PING" in line:
			s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			break
		user = getUser(line)
		message = getMessage(line)
		print (user + " typed :" + message)
		cmd = rg.search(message)
		if cmd:
			prefix=cmd.group(1)
			action=cmd.group(2)
			print ("("+prefix+")"+"("+action+")"+"\n")

			if action=="hit":
				sendMessage(s, "Hit Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Hit\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/hit.png',.85):
					sendMessage(s, "Hit Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"Hit Button Not Found!")
			elif action=="help":
				sendMessage(s,"@"+user+"Hi, to use me, use '!' and your blackjack command\nEx:!hit to hit in blackjack")

			elif action=="deal":
				sendMessage(s, "Deal Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Deal\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/deal.png',.85):
					sendMessage(s, "Deal Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"Deal Button Not Found!")
				
			elif action=="stand":
				sendMessage(s, "Stand Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Stand\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/stand.png',.85):
					sendMessage(s, "Stand Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"Stand Button Not Found!")
				
			elif action=="insure":
				sendMessage(s, "Insure Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Insure\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/insure.png',.85):
					sendMessage(s, "Insure Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"Insure Button Not Found!")

			elif action=="split":
				sendMessage(s, "Split Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Split\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/split.png',.85):
					sendMessage(s, "split Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"split Button Not Found!")

			elif action=="double":
				sendMessage(s, "Double Acknowledged")
				with open(voteFile+".txt", "a") as out:
					out.write("'"+user+"' Voted: Double\n")
				if findImage('/users/ryan/Desktop/grunt2/resources/double.png',.85):
					sendMessage(s, "Double Clicked")
					pyautogui.click(x=clickTarget[0]/2, y=clickTarget[1]/2)  # move to 100, 200, then click the left mouse button.
				else:
					sendMessage(s,"Double Button Not Found!")
						
#if __name__=="__main__":
 #   main()