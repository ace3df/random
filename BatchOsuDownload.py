import sys, os, urllib2, time, requests
from bs4 import BeautifulSoup
from twill.commands import *

# Uses BS4 and Twill
# BS4: http://www.crummy.com/software/BeautifulSoup/
# Twill: http://twill.idyll.org/
# or you can download the .exe here: (twill is dumb and wont compile with py2exe)

# Set agent so we can connect to Osu! site
agent("Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2")
go('http://osu.ppy.sh/forum/ucp.php')
# Set username and password
username = raw_input("Username: ")
password = raw_input("Password: ")
# Show all forms that are on the site
showforms()
# Enter text in forms
fv("4", "username", username)
fv("4", "password", password)
# Submit!
submit()

def download_map(url1, bmapname):
	
	# Replace the 2 things that can stop windows from writing to file
	bmapname = bmapname.replace("*", "(star)")
	bmapname = bmapname.replace(":", "")

	# Give new agent
	agent("Opera/9.25 (Windows NT 5.1; U; en)")
	# Go to generated url
	dl = go(url1)
	# Request to download
	r = requests.get(dl, stream=True)

	# Save in chunks
	with open(bmapname, 'wb') as f:
	    for chunk in r.iter_content(chunk_size=10024): 
	        if chunk: # filter out keep-alive new chunks
	            f.write(chunk)
	            f.flush()
	return

# Osu! link batch list (url on each line)
fname = "osubatch.txt"

# Open filename and create array
with open(fname, 'r') as f:
    lines = f.readlines()

# If you download too many you will get stopped so we just add a delay so it wont happen
x = 0

# For every line in file do something
for url in lines:

	x = x + 1
	if x == 10:
		time.sleep(300)
	else:
		time.sleep(20)

	# First we'll get beatmap title so we can set it as the filename
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	bmapname = soup.find('div', class_='content-with-bg').h1.text.encode('utf-8')[19:] + ".osz"

	# Go to the beatmap URL
	go(url)

	# If it's a /d/ url it doesn't need to go through all the links to find the download button
	if "/d/" in url:
		pass
	else:
		# Twill get all links and put them in a list
		link_list = list(showlinks())
		# Loop all links untill we find the link with /d/ in it
		for line in link_list:
			line = str(line)
			if "google" in line: # google docs link has /d/ in it lol
				pass
			elif "/d/" in line:
				temp = line

		# Clean up the url line to get just the end of the url
		temp = temp.split(", url='")
		temp = temp[1]
		temp = temp.split('\', text=')
		temp = temp[0]
		# Site + temp url = download /d/ link!
		osulink = "http://osu.ppy.sh" + str(temp)
		print osulink
		# Go to /d/ link
	# Call function and return that it had downloaded!
	download_map(osulink, bmapname)
	print bmapname + " - Downloaded!"
