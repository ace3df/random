import sys, os, urllib2
from bs4 import BeautifulSoup
from twill.commands import *

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

# Osu! link batch list (url on each line)
fname = "osubatch.txt"

# Open filename and create array
with open(fname, 'r') as f:
    lines = f.readlines()

# For every line in file do something
for url in lines:

	# First we'll get beatmap title so we can set it as the filename
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)

	bmapname = soup.find('div', class_='content-with-bg').h1.text.encode('utf-8')[19:]

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
			if "/d/" in line:
				temp = line

		# Clean up the url line to get just the end of the url
		temp = temp.split(", url='")
		temp = temp[1]
		temp = temp.split('\', text=')
		temp = temp[0]
		# Site + temp url = download /d/ link!
		osulink = "http://osu.ppy.sh" + str(temp)
		# Go to /d/ link
		go(osulink)

	# save_html is also just download so we download the map and save it as the map title + filetype
	save_html(bmapname + ".osz")
