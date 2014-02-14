from pykeyboard import PyKeyboard
import sys, re, codecs, socket

class TwitchChatPlays:

    socket = None
    connected = False

    ''' What I've defined each button, change k.tap_key('_') to what you want!
     right = l
     left = k
     up = o
     down = m
     a = a
     b = b 
     select = u
     start = y

    '''

    def __init__(self):
        self.socket = socket.socket()
        #nick
        nickname = "TWITCH USERNAME"
        #pass
        password = "YOUR TWITCH OUTH HERE"
        #channels
        channels = "#YOURTWITCHCHANNEL"
        # irc temp
        ircserv = "irc.twitch.tv"

        # Connect and send commands to login
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ircserv, 6667))
        self.send("PASS %s" % password)
        self.send("NICK %s" % nickname)
        self.send("JOIN %s" % channels)

        # Let's count how many times each button is pressed!
        k = PyKeyboard()
        a = 0
        b = 0
        up = 0
        down = 0
        left = 0
        right = 0
        start = 0
        select = 0
        #########

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
                  print("Please check your Twitch OAUTH!")

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

                if repy['msg'] == "a":
                  a =+ 1 
                  # Press button that is defind as 'a' on emulator
                  k.tap_key('a')

                if repy['msg'] == "b":
                  b =+ 1 
                  # Press button that is defind as 'b' on emulator
                  k.tap_key('b')

                if repy['msg'] == "up":
                  up =+ 1 
                  k.tap_key('o')

                if repy['msg'] == "down":
                  down =+ 1 
                  k.tap_key('m')

                if repy['msg'] == "left":
                  left =+ 1 
                  k.tap_key('k')

                if repy['msg'] == "right":
                  right =+ 1 
                  k.tap_key('l')

                if repy['msg'] == "start":
                  start =+ 1 
                  k.tap_key('y')

                if repy['msg'] == "select":
                  select =+ 1 
                  k.tap_key('u')

                ## Print Stats
                if repy['msg'] == "stats" and nickname in repy['sender']:
                	print a, b, up, down, left, right, start, select	

        # To send basic IRC server talk
    def send(self, msg):
        print ">",msg
        self.socket.send(msg+"\r\n")

        # To send say commands
    def say(self, msg, to):
        self.send("PRIVMSG %s :%s" % (to, msg))

TwitchChatPlays()
