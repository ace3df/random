import webbrowser, urllib, json
import threading
import time

IRCUsername, IRCPassword, APIKey = "", "", ""

def Setup():

	if raw_input("Enable IRC Mode? (y/n): ") == "y":
		IRCUsername = raw_input("osu! (IRC) Username: ")
		IRCPassword = raw_input("IRC Password (NOT osu! password (type \"NONE\" if you don't have one): ")
		if IRCPassword == "NONE":
			webbrowser.open('https://osu.ppy.sh/p/ircauth')
			IRCPassword = raw_input("Input password: ")
			# ADD CONNECT TO SEVER SHIT HERE
			GetUserPPLoad(APIKey, IRCUsername, IRCPassword)
	elif raw_input("Enable IRC Mode? (y/n): ") == "n":

		APIKey = "old"
		IRCUsername = "Ace3DF"
		GetUserPPLoad(APIKey, IRCUsername, IRCPassword)
	else:
		raw_input("Enable IRC Mode? (y/n): ")

def GetUserPPLoad(APIKey, IRCUsername, IRCPassword):

	url = "http://osu.ppy.sh/api/get_user?k=" + APIKey + "&u=" + IRCUsername + ""
	response = urllib.urlopen(url);
	dataFirst = json.loads(response.read())
	ppOld = float(dataFirst[0]["pp_raw"])
	print "Current Raw PP: ", float(ppOld)
	ScoreSubmitted(url, ppOld)

def ScoreSubmitted(url, ppOld):

	response = urllib.urlopen(url);
	dataFirst = json.loads(response.read())
	ppNew = float(dataFirst[0]["pp_raw"])
	ppNew = ppNew + 2
	print ppNew
	if ppNew != ppOld: 
		ppChange = ppNew - ppOld
		if ppChange > ppOld:
			print "+ " + str(ppChange)
		else:
			print ppChange

	threading.Timer(60, ScoreSubmitted).start()


Setup()
