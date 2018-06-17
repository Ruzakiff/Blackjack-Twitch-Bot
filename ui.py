import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import time
kivy.require('1.0.6') # replace with your current kivy version !




voteQueue=open("/Users/ryan/Desktop/grunt/votes.txt","r")
lineVote=""
reading=False
roundLength=15
roundtime=roundLength
reading=False



class TimeApp(App):
	def build(self):
		self.main_box=BoxLayout(orientation='vertical')
		Clock.schedule_interval(self.readVote,0.1)
		Clock.schedule_interval(self.timer,1)

		self.tick=Label(text=str(roundtime))
		self.voteDisplay=Label(text="No Votes Yet!")
		self.main_box.add_widget(self.tick)
		self.main_box.add_widget(self.voteDisplay)

		return self.main_box



	def readVote(self,*args):
		global lineVote
		global reading
		whereVote=voteQueue.tell()
		lineVote=voteQueue.readline()
		reading=False
		if not lineVote:
			reading=False
			voteQueue.seek(whereVote)
		else:
			reading=True
		if(reading):
			self.voteDisplay.text=self.voteDisplay.text+"\n"+lineVote
		if(roundtime=="Round Ended!"):
			open("/Users/ryan/Desktop/grunt/votes.txt","w").close()
			self.voteDisplay.text="No Votes Yet!"

	def timer(self,*args):
		global roundtime
		if(roundtime=="Round Ended!"):
			roundtime=roundLength
		else:
			roundtime=roundtime-1
		if(roundtime<0):
			roundtime="Round Ended!"
		self.tick.text=str(roundtime)


if __name__ == "__main__":
	TimeApp().run()