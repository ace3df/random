from pykeyboard import PyKeyboard
import sys, re, codecs, socket, time

class TwitchChatPlays:

    socket = None
    connected = False

    def __init__(self):
        self.socket = socket.socket()
        #nick
        nickname = "twitch username"
        #pass
        password = "TWITCH OUTH KEY"
        #channels
        channels = "#twitch channel"
        # irc temp
        ircserv = "irc.twitch.tv"

        # Connect and send commands to login
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ircserv, 6667))
        self.send("PASS %s" % password)
        self.send("NICK %s" % nickname)
        self.send("JOIN %s" % channels)

        # What I've defined each button w/e
        right = "l"
        left = "k"
        up = "o"
        down = "m"
        a = "a"
        b = "b"
        select = "u"
        start = "y"

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

                if repy['msg'] == "a":
                  a =+ 1 
                  # Press button that is defind as 'a' on emulator
                  k.press_key(a)
                  time.sleep(0.5)
                  k.release_key(a)

                if repy['msg'] == "b":
                  b =+ 1 
                  # Press button that is defind as 'b' on emulator
                  k.press_key(b)
                  time.sleep(0.5)
                  k.release_key(b)

                if repy['msg'] == "up":
                  up =+ 1 
                  k.press_key(o)
                  time.sleep(0.5)
                  k.release_key(o)

                if repy['msg'] == "down":
                  down =+ 1 
                  k.press_key(m)
                  time.sleep(0.5)
                  k.release_key(m)

                if repy['msg'] == "left":
                  left =+ 1 
                  k.press_key(k)
                  time.sleep(0.5)
                  k.release_key(k)

                if repy['msg'] == "right":
                  right =+ 1 
                  k.press_key(l)
                  time.sleep(0.5)
                  k.release_key(l)

                if repy['msg'] == "start":
                  start =+ 1 
                  k.press_key(y)
                  time.sleep(0.5)
                  k.release_key(y)

                if repy['msg'] == "select":
                  select =+ 1 
                  k.press_key(u)
                  time.sleep(0.5)
                  k.release_key(u)

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
