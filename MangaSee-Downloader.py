import urllib2
from os.path import basename
import os
import re
from urlparse import urlsplit
from bs4 import BeautifulSoup as BeautifulSoup

baseurl = "http://www.mangasee.com/manga/?series="
mangaurl = raw_input("Manga Name URL String: ")
afterurl = "&chapter="
chapterurl = int(raw_input("Chapter Number Start: "))
chapend = int(raw_input("Chapter Number End: "))
after2url = "&index=1"

mangaurl = mangaurl.title()
# Don't remember how to do all this in one line so I'm doing it this way :<
nonowords = [" ", "!", "+", "-", ",", ".", "\'", "(", ")"]
if any(x in mangaurl for x in nonowords):
    mangaurl = mangaurl.replace(" ", "")
    mangaurl = mangaurl.replace("!", "")
    mangaurl = mangaurl.replace("+", "")
    mangaurl = mangaurl.replace("-", "")
    mangaurl = mangaurl.replace(",", "")
    mangaurl = mangaurl.replace(".", "")
    mangaurl = mangaurl.replace("\'", "")
    mangaurl = mangaurl.replace(")", "")
    mangaurl = mangaurl.replace("(", "")

while chapterurl <= chapend:
	url = baseurl + mangaurl + afterurl + str(chapterurl) + after2url
	try: 
	    urlContent = urllib2.urlopen(url).read()
	    soup = BeautifulSoup(''.join(urlContent))
	    AnimeName = soup.findAll('a', style="font-size:20px;")[0].text
	    AnimeChap = soup.findAll('option', selected="selected")[0].text
	    imgTags = soup.findAll('img')
	    chapterurl += 1
	except urllib2.HTTPError, e:
		print "URL Error! Make sure Manga URL String is write and that the chapter is out!"
		raw_input("Press Enter to continue...")

	# Probs a better way to do this but w/e
	if not os.path.exists(AnimeName):
	    os.makedirs(AnimeName)
	if not os.path.exists(AnimeName+"/"+AnimeChap):
	    os.makedirs(AnimeName+"/"+AnimeChap)
	else:
		print "Chapter Already Downloaded, Sure You Want To Continue?"
		raw_input("Press Enter to continue...")
		print "Continuing Download..."

	# download all images
	for imgTag in imgTags:
	    imgUrl = imgTag['src']
	    try:
	        imgData = urllib2.urlopen(imgUrl).read()
	        fileName = AnimeName + " - " + AnimeChap + " - " + basename(urlsplit(imgUrl)[2])[5:]
	        output = open(AnimeName+"/"+AnimeChap+"/"+fileName,'wb')
	        output.write(imgData)
	        output.close()
	        os.remove(AnimeName+"/"+AnimeChap+"/"+ AnimeName + " - " + AnimeChap + " - " + "02.gif") # Remove that shitty viewer count
	    except:
	        pass
	print "Downloaded: " + AnimeName + " - " + AnimeChap
print "Download Complete!"
raw_input("Press Enter to continue...")	 
