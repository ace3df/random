import sys
import re
import codecs
import socket
import os
import json
from bs4 import BeautifulSoup as bs4 # Download BeautifulSoup4 - name folder bs4
import urllib2 # need this becuase python and something
from urllib2 import urlopen

class TwitchWR:

    socket = None
    connected = False
    modOnly = 0
    botOff = 1
    ircTrigger = ['whats wr', 'what is world record', 'what wr', 'what is wr', 'wr?', 'what\'s wr', 'what is the world record', 'what is the wr']

    def __init__(self):
        self.socket = socket.socket()
        try:
          with open('settings.txt', 'r') as f:
            lines=f.readlines()
            nickname = lines[0]
            password = lines[1]
            ircserv  = lines[2]
            channels = lines[3]
            modUser = lines[4]
            ircserv = ircserv.strip()
            f.close()
        except IOError:
            #nick
            nickname = raw_input("Enter your IRC username: ")
            #pass
            password = raw_input("Enter Twitch Oauth: ")
            #channels
            channels = raw_input("Enter IRC channels (start with # :: seperate with ,): ")
            # irc temp
            ircserv = "irc.twitch.tv"

            # Write what you typed 
            f = open('settings.txt','w')
            f.write(nickname+'\n')
            f.write(password+'\n')
            f.write(ircserv+'\n')
            f.write(channels+'\n')
            f.write(nickname+'\n')
            f.close()

        # Connect and send commands to login
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ircserv, 6667))
        self.send("PASS %s" % password)
        self.send("NICK %s" % nickname)
        self.send("JOIN %s" % channels)

        while True:
            databuff = self.socket.recv(4096)
            lines = databuff.split("\n")
            for databuff in lines:
                databuff = str(databuff).strip()

                # PONG server so it doesn't disconnect!
                if databuff.find("PING") != -1:
                  self.send("PONG")
                # If password wrong warn user why it might be!
                if databuff.find("unsuccessful") != -1:
                  print("Please check your Twitch OAUTH in settings.txt!")

                if databuff == '':
                    continue
                print "<", databuff
                
                args = databuff.split(None, 3)
                if len(args) != 4:
                    continue
                repy = {}
                repy['sender'] = args[0][1:]
                repy['type']   = args[1]
                repy['target'] = args[2]
                repy['msg']    = args[3][1:]

                # whom to reply
                target = repy['target']
                if repy['target'] == nickname:
                    target = repy['sender'].split("!")[0]

                # Get channel name cut out #
                twitchChannel = target[1:]

                if repy['msg'][0:7] == "!wrhelp":
                  self.say("!wrmod, !wrchan, !wrleave, !wrjoin", target)

                if repy['msg'][0:6] == "!wrmod" and modUser in repy['sender']:
                  if self.modOnly == 0:
                    self.modOnly = 1
                    self.say("Mod Only off!", target)
                  elif self.modOnly == 1:
                    self.modOnly = 0
                    self.say("Mod Only on!", target)

                if repy['msg'][0:6] == "!wrbot" and modUser in repy['sender']:
                  if self.botOff == 0:
                    self.botOff = 1
                    self.say("WR Bot online!", target)
                  elif self.botOff == 1:
                    self.botOff = 0
                    self.say("WR Bot offline! Use !wrbot to turn it back on!", target)
 
                if self.modOnly == 0 and modUser in repy['sender']:
                      if repy['msg'][0:7] == "!wrchan":
                          try:
                            with open('settings.txt', 'r') as f:
                              lines=f.readlines()
                              channels = lines[3]
                              f.close()
                              self.say("In current channel(s): "+channels, target)
                          except IOError:
                            self.say("Settings.txt error!", target)
                      
                      # Make bot join channel!
                      if repy['msg'][0:7] == "!wrjoin":
                          joinChan = repy['msg'][8:]
                          # Edits settings.txt and add to channel list for auto connect!
                          with open('settings.txt', 'r') as file:
                              data = file.readlines()
                          # Check if you're already in the channel!
                          Chan = data[3]
                          if joinChan in Chan:
                            self.say("Already in channel!", target)
                          else:                            
                            if "#" in joinChan:
                              self.send("JOIN %s" % joinChan)
                              data[3] = joinChan +','+ Chan
                            else:
                              data[3] = '#'+joinChan +','+ Chan
                              self.send("JOIN %s" % "#"+joinChan)
                          # and write everything back
                          with open('settings.txt', 'w') as file:
                            file.writelines(data)
                          file.close()

                      # Leave channel
                      if repy['msg'][0:8] == "!wrleave":
                        if repy['msg'][9:] == "":
                          self.say("Forgot to say channel!", target)
                        else:
                          joinChan = repy['msg'][9:]
                          if "#" in joinChan:
                            self.send("PART %s" % joinChan)
                          else:
                            self.send("PART %s" % "#"+joinChan)
                            joinChan = "#"+joinChan
                          try:
                             # Edits settings.txt and add to channel list for auto connect!
                             with open('settings.txt', 'r') as file:
                                 data = file.readlines()
                             # Get current Channel list 
                             Chan = data[3]
                             data[3] = Chan.replace(joinChan+",","")
                             # and write everything back
                          except IOError:
                            self.say("Not in that channel!", target)
                          with open('settings.txt', 'w') as file:
                            file.writelines(data)
                          file.close()

                # The trigger! Looks for any words in ircTrigger that might be in repy['msg']
                if any(x in repy['msg'] for x in self.ircTrigger) and self.botOff == 1:
                    print "Working..." # so we know it's passed and it's not just the sites
                    # Open Twitch.tv and get Channel name
                    html = "http://www.twitch.tv/"+twitchChannel
                    data = urlopen(html).read()
                    soup = bs4(data)
                    # Get what game they're playing!
                    twitchGame = soup.findAll('a', class_="game js-game")[0].text
                    # Get title to return what category
                    twitchTitle = soup.findAll('span', class_="real_title js-title")[0].text
                    # Take what game they're playing and find PBTracker json!
                    twitchGame = twitchGame.replace(":", "")
                    twitchGame = twitchGame.replace("\'", "")
                    twitchJson = twitchGame.replace(" ", "-")
                    twitchJson = twitchJson.lower()
                    # Lowercase title so we don't have to ask for too many
                    twitchTitle = twitchTitle.lower()
                    twitchTitle = twitchTitle.replace("/"," ")
                    twitchTitle = twitchTitle.replace("%"," ")
                    twitchTitle = twitchTitle.replace("-"," ")
                    twitchTitle = twitchTitle.replace("\'"," ")
                    # This is a really bad way to do this but it works. 
                    ###########################################################################################
                    # Game: The Legend of Zelda Ocarina of Time
                    if "100" in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 3
                    elif "child dungeon" in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 1
                    elif "rba" in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 2
                    elif "mst"in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 3
                    elif "child dungeon" in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 1
                    elif "ww wrong warp" in twitchTitle and twitchJson == "the-legend-of-zelda-ocarina-of-time":
                         twitchCAT = 6
                    # Game: The Legend of Zelda Majora's Mask
                    elif "100" in twitchTitle and twitchJson == "the-legend-of-zelda-majoras-mask":
                         twitchCAT = 2
                    # Game: Super Mario 64
                    elif "45" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 4
                    elif "16" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 0
                    elif "70" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 1
                    elif "120" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 2
                    elif "1 star" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 5
                    elif "0 star" in twitchTitle and twitchJson == "super-mario-64":
                         twitchCAT = 8
                    # Game: Super Mario World
                    elif "96" in twitchTitle and twitchJson == "super-mario-world":
                         twitchCAT = 1
                    elif "any no starworld" in twitchTitle and twitchJson == "super-mario-world":
                         twitchCAT = 2
                    elif "any no cape" in twitchTitle and twitchJson == "super-mario-world":
                         twitchCAT = 4
                    # Make sure these are always last
                    elif "any" in twitchTitle:
                         twitchCAT = 0
                    elif "100" in twitchTitle:
                         twitchCAT = 1
                    # If it gets confused it should return 0 and warn people because this shouldn't really happen
                    else:
                         twitchCAT = 0
                         self.say("Something went wrong :S")
                    try:
                       # Debug print
                       print twitchJson," : ",twitchTitle," : ",twitchCAT
                       url = urllib2.urlopen('http://www.pbtracker.net/game/'+twitchJson+'.json')
                       data_file = url.read()    
                       dataWR = json.loads(data_file)
                       # Sometimes 100% is before any% so we do these to switch them around
                       if "100" in twitchTitle and dataWR[twitchCAT]["category"] == "any%":
                        twitchCAT = twitchCAT == 1
                        print twitchCAT
                       if "any" in twitchTitle and dataWR[twitchCAT]["category"] == "100%":
                        twitchCAT = twitchCAT == 0
                        print twitchCAT
                       try:
                              runnerWR = dataWR[twitchCAT]["bk_runner"]
                              cateWR = dataWR[twitchCAT]["category"]
                              timeWR = dataWR[twitchCAT]["bk_time"]
                              videoWR = dataWR[twitchCAT]["bk_video"]
                              self.say("World Record for "+twitchGame.title()+ " in "+cateWR+" is "+timeWR+" by "+runnerWR, target)
                       except TypeError:
                      	 self.say("No best time down! Submit a time at www.pbtracker.net !", target)
                    except urllib2.HTTPError, e:
                       self.say("Game not found on www.pbtracker.net -- If it's actualy on that site please contact Ace3DF", target)

        # To send basic IRC server talk
    def send(self, msg):
        print ">",msg
        self.socket.send(msg+"\r\n")

        # To send say commands
    def say(self, msg, to):
        self.send("PRIVMSG %s :%s" % (to, msg))

    def parse_url(self,url):
        soup = BeautifulSoup(urllib2.urlopen(url))

TwitchWR()
