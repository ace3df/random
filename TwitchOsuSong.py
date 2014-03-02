import sys, re, codecs, socket, os, time
import base64
import win32gui

class TwitchOsuSong:

    socket = None
    connected = False
    # Define what will trigger it
    ircTrigger = ['song?', 'what is the song']

    def __init__(self):

        w = win32gui
        self.socket = socket.socket()
        try:
          with open('settings.txt', 'r') as f:
            lines=f.readlines()
            nickname = lines[0]
            password = lines[5]
            ircserv  = lines[1]
            channels = lines[2]
            OsuMulti = lines[3]
            OsuTrigger = lines[4]
            ircserv = ircserv.strip()
            f.close()
        # If settings.txt isn't there to read we create it!
        except IOError:
            #nick
            nickname = raw_input("Enter your IRC username: ")
            #Twitch OAUTH
            password = raw_input("Enter Twitch OAUTH: ")
            #channels
            channels = raw_input("Enter IRC channels (start with # :: seperate with ,): ")
            # IRC Server (Twitch)
            ircserv = "irc.twitch.tv"

            # Write what you typed 
            f = open('settings.txt','w')
            f.write(nickname+'\n')
            f.write(ircserv+'\n')
            f.write(channels+'\n')
            f.write("True"+'\n')
            f.write("True"+'\n')
            f.write(password)
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

                if ("!song" in repy['msg']) and (OsuTrigger == "True\n"):
                    time.sleep(1)
                    curWin = w.GetWindowText(w.GetForegroundWindow())
                    if curWin == "osu!":
                        self.say("Not in the middle of a song!", target)
                    elif "osu!" in curWin:
                        curWin = curWin[8:]
                        self.say("Current song: " + curWin, target)
                        curWin = curWin.replace(" ", "%20")
                        self.say("http://osu.ppy.sh/p/beatmaplist?q=" + curWin, target)
                    else:
                        self.say("Streamer currently not focused on Osu!", target)


                # The trigger! Looks for any words in ircTrigger that might be in repy['msg']
                if (any(x in repy['msg'] for x in self.ircTrigger)) and (OsuMulti == "True\n"):
                    time.sleep(1)
                    curWin = w.GetWindowText(w.GetForegroundWindow())
                    if curWin == "osu!":
                        self.say("Not in the middle of a song!", target)
                    elif "osu!" in curWin:
                        curWin = curWin[8:]
                        self.say("Current song: " + curWin, target)
                        curWin = curWin.replace(" ", "%20")
                        self.say("http://osu.ppy.sh/p/beatmaplist?q=" + curWin, target)
                    else:
                        self.say("Streamer currently not focused on Osu!", target)
   
        # To send basic IRC server talk
    def send(self, msg):
        print ">",msg
        self.socket.send(msg+"\r\n")

        # To send say commands
    def say(self, msg, to):
        self.send("PRIVMSG %s :%s" % (to, msg))

TwitchOsuSong()
