import urllib2
from os.path import basename
from os import path
import os
import re
from urlparse import urlsplit
from bs4 import BeautifulSoup as BeautifulSoup
import json

class MangaDownloader:
	print "Simple Manga Downloader v0.1 - Python 2.7 - Open source: http://bombch.us/VBz \n"
	print "What do you want to do?\n"
	print "1. Download Manga"
	print "2. Search Manga (doesn't work don't use yet plz)"
	print "3. Get Manga info (doesn't work don't use yet plz)"
	print "4. Check for new Chapter(s)"
	print "5. Options"
	print ""
	optionSet = int(raw_input("Enter Num: "))
	while optionSet >= 6 or optionSet <= 0:
		print "Please enter a valid number..."
		optionSet = int(raw_input("Enter Num: "))

	def MangaDownload(mangaurl, chapstart, chapend):
		''' Load Json Options '''
		jsonfile = open("options.json", "r")
		data = json.load(jsonfile)
		jsonfile.close()	
		MangaSaveLocation = data["MangaSaveLocation"]
		OverWriteWarning = data["OverWriteWarning"]
		SubChapterFolder = data["SubChapterFolder"]
		MangaDetails = data["MangaDetails"]
		''' Load Json Options '''
		print "Starting..."
		alreadyDown = True
		MangaTitle = mangaurl
		nonowords = [" ", "!", "+", "-", ",", ".", "\'", "(", ")", ";", ":"]
		if any(x in mangaurl for x in nonowords):
		    mangaurl = mangaurl.replace("!", " ")
		    mangaurl = mangaurl.replace("+", " ")
		    mangaurl = mangaurl.replace("-", " ")
		    mangaurl = mangaurl.replace(",", " ")
		    mangaurl = mangaurl.replace(".", " ")
		    mangaurl = mangaurl.replace("\'", " ")
		    mangaurl = mangaurl.replace(")", " ")
		    mangaurl = mangaurl.replace("(", " ")
		    mangaurl = mangaurl.replace(";", " ")
		    mangaurl = mangaurl.replace(":", " ")
		    mangaurl = mangaurl.title()
		    mangaurl = mangaurl.replace(" ", "")
		url = "http://www.mangasee.com/manga/?series=" + mangaurl + "&chapter=0&index=1&page=1"
		AnimeChap = ""
		try:
			urlContent = urllib2.urlopen(url).read()
			soup = BeautifulSoup(''.join(urlContent))
			try:
				Chap0 = False
				AnimeChap = soup.findAll('p', style="color:#F00; font-size:16px; margin-bottom:5px; font-weight:bold;")[0].text
			except:
				Chap0 = True
		except urllib2.HTTPError, e:
			Chap0 = False
		if chapstart == -1:
			print MangaTitle + " - Downloading all avilable chapters!"
		else:
			print "Downloading: " + MangaTitle + " - Chapter(S): " + str(chapstart) + " to " + str(chapend)
		if str(Chap0) == "True":
			chapstart = 0
		else:
			chapstart = 1
		while chapstart <= chapend:
			url = "http://www.mangasee.com/manga/?series=" + mangaurl + "&chapter=" + str(chapstart) + "&index=1"
			try: 
			    urlContent = urllib2.urlopen(url).read()
			    soup = BeautifulSoup(''.join(urlContent))
			    AnimeName = soup.findAll('a', style="font-size:20px;")[0].text
			    AnimeChap = soup.findAll('option', selected="selected")[0].text
			    imgTags = soup.findAll('img')
			    chapstart += 1
			except urllib2.HTTPError, e:	
				print "URL Error! Make sure Manga URL String is correct and that the chapter is out!"
				raw_input("Press Enter to close...")
			except:
				print "Download Complete!"
				print "Location Saved: " + os.path.dirname(MangaSaveLocation) + "/" + AnimeName
				raw_input("Press Enter to close...")
				raise SystemExit
			if any(x in AnimeName for x in nonowords):
			    AnimeName = AnimeName.replace(":", " ")
			    AnimeName = AnimeName.title()
			# Probs a better way to do this but w/e
			if not os.path.exists(MangaSaveLocation+"/"+AnimeName):
			    os.makedirs(MangaSaveLocation+"/"+AnimeName)
			if not os.path.exists(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap):
			    os.makedirs(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap)
			else:
				if alreadyDown == True:
					print "Chapter Already Downloaded, Sure You Want To Continue?"
					alreadyDown = False
					raw_input("Press Enter to continue...")
					print "Continuing Download..."
				else:
					pass
			# download all images
			for imgTag in imgTags:
			    imgUrl = imgTag['src']
			    try:
			        imgData = urllib2.urlopen(imgUrl).read()
			        fileName = AnimeName + " - " + AnimeChap + " - " + basename(urlsplit(imgUrl)[2])[5:]
			        output = open(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+fileName,'wb')
			        output.write(imgData)
			        output.close()
			        os.remove(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+ AnimeName + " - " + AnimeChap + " - " + "02.gif") # Remove that shitty viewer count
			        try:
			        	os.remove(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+ AnimeName + " - " + AnimeChap + " - " + "domNo]@x01") # This shows up sometimes no idea why
			        except:
			        	pass
			    except:
			        pass
			print "Downloaded: " + AnimeName + " - " + AnimeChap
		print "Download Complete!"
		print "Location Saved: " + MangaSaveLocation+"\\" + AnimeName
		raw_input("Press Enter to Close...")
########################################

	# This is REALLY messy but w/e
	def MangaUpdate():
		''' Load Json Options '''
		jsonfile = open("options.json", "r")
		data = json.load(jsonfile)
		jsonfile.close()	
		MangaSaveLocation = data["MangaSaveLocation"]
		OverWriteWarning = data["OverWriteWarning"]
		SubChapterFolder = data["SubChapterFolder"]
		MangaDetails = data["MangaDetails"]
		''' Load Json Options '''
		print MangaSaveLocation
		dirname = path.dirname(MangaSaveLocation)
		# Get folder names
		dlManga = os.listdir(MangaSaveLocation)
		print dlManga
		# Get what chapter each one
		for e in dlManga:
			print e
			newE = e
			nonowords = [" ", "!", "+", "-", ",", ".", "\'", "(", ")", ";", ":"]
			if any(x in e for x in nonowords):
				    e = e.replace("!", " ")
				    e = e.replace("+", " ")
				    e = e.replace("-", " ")
				    e = e.replace(",", " ")
				    e = e.replace(".", " ")
				    e = e.replace("\'", " ")
				    e = e.replace(")", " ")
				    e = e.replace("(", " ")
				    e = e.replace(";", " ")
				    e = e.replace(":", " ")
				    if " " in e:
				       e = e.title()
				    e = e.replace(" ", "")
			# GET total chapter number
			url = "http://www.mangasee.com/manga/?series=" + e + "&chapter=1&index=1&page=1"
			try:
			    urlContent = urllib2.urlopen(url).read()
			    soup = BeautifulSoup(''.join(urlContent))
			    totalChaptersOut = soup.findAll('select', name_="chapter")
			    totalChapters = soup.findAll('option', totalChaptersOut)[-1].text
			    totalChapters = map(int, re.findall(r'\d+', totalChapters))
			    chapterName = soup.findAll('option', totalChaptersOut)[-1].text
			    chapterName = ''.join([i for i in chapterName if not i.isdigit()])[:-1]
			except urllib2.HTTPError, e:
				print "URL Error! Make sure Manga URL String is correct and that the chapter is out!"
				print url
				raw_input("Press Enter to close...")
			# START
			i = 1
			while i <= totalChapters:
				nonowords = [" ", "!", "+", "-", ",", ".", "\'", "(", ")", ";", ":"]
				if any(x in e for x in nonowords):
					    e = e.replace("!", " ")
					    e = e.replace("+", " ")
					    e = e.replace("-", " ")
					    e = e.replace(",", " ")
					    e = e.replace(".", " ")
					    e = e.replace("\'", " ")
					    e = e.replace(")", " ")
					    e = e.replace("(", " ")
					    e = e.replace(";", " ")
					    e = e.replace(":", " ")
					    if " " in e:
					       e = e.title()
					    e = e.replace(" ", "")
				curChap = dirname + newE + "\\" + chapterName + " " + str(i)
				chapdown = os.path.exists(curChap)
				if chapdown == True:
					i += 1
				elif chapdown == False:
					url = "http://www.mangasee.com/manga/?series=" + e + "&chapter=" + str(i) + "&index=1"
					# Download
					try:
					    urlContent = urllib2.urlopen(url).read()
					    soup = BeautifulSoup(''.join(urlContent))
					    AnimeName = soup.findAll('a', style="font-size:20px;")[0].text
					    AnimeChap = soup.findAll('option', selected="selected")[0].text
					    imgTags = soup.findAll('img')
					    chapStop = False
					    print "Downloading: " + newE + " - Chapter: " + str(i)
					except urllib2.HTTPError, e:
						print "URL Error! Make sure Manga URL String is correct and that the chapter is out!"
						print url
						raw_input("Press Enter to close...")
					except:
						chapStop = True
						print "Downloaded: " + str(i - 2) + " Chapter(s)"
							# Probs a better way to do this but w/e
					if chapStop == True:
						print newE + " is up-to-date!"
						raw_input("Press Enter to continue...")
						break
					elif chapStop == False:
						if not os.path.exists("manga/"+AnimeName):
							os.makedirs("manga/"+AnimeName)
						if not os.path.exists("manga/"+AnimeName+"/"+AnimeChap):
							os.makedirs("manga/"+AnimeName+"/"+AnimeChap)
					if chapdown == True:
						print "Check Folder something might have gone wrong"
						raw_input("Press Enter to close...")
					elif chapdown == False:
						for imgTag in imgTags:
						    imgUrl = imgTag['src']
						try:
						    imgData = urllib2.urlopen(imgUrl).read()
						    fileName = AnimeName + " - " + AnimeChap + " - " + basename(urlsplit(imgUrl)[2])[5:]
						    output = open(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+fileName,'wb')
						    output.write(imgData)
						    output.close()
						    os.remove(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+ AnimeName + " - " + AnimeChap + " - " + "02.gif") # Remove that shitty viewer count
						    try:
						        os.remove(MangaSaveLocation+"/"+AnimeName+"/"+AnimeChap+"/"+ AnimeName + " - " + AnimeChap + " - " + "domNo]@x01") # This shows up sometimes no idea why
						    except:
						        pass
						except:
						    pass
					i += 1
			else:
				print "Download Complete!"
		print "Everything is up-to-date!"
		raw_input("Press Enter to close...")


	def options():
		jsonfile = open("options.json", "r")
		data = json.load(jsonfile)
		jsonfile.close()	
		MangaSaveLocation = data["MangaSaveLocation"]
		OverWriteWarning = data["OverWriteWarning"]
		SubChapterFolder = data["SubChapterFolder"]
		MangaDetails = data["MangaDetails"]
		''' Print Json Settings'''
		print ""
		print "Current Settings:"
		print "1. Manga Download Location: " + MangaSaveLocation
		print "2. Over Write Warning: " + OverWriteWarning
		print "3. Sub Chapter Folders: " + SubChapterFolder
		print "4. Show Manga Details before downloading: " + MangaDetails
		''' End Json Print '''
		while True:
			jsonfile = open("options.json", "r")
			data = json.load(jsonfile)
			jsonfile.close()	
			MangaSaveLocation = data["MangaSaveLocation"]
			OverWriteWarning = data["OverWriteWarning"]
			SubChapterFolder = data["SubChapterFolder"]
			MangaDetails = data["MangaDetails"]
			editOp = int(raw_input("Enter # to edit: "))
			while editOp >= 6 or editOp <= 0:
				print "Stop being a cunt"
				editOp = int(raw_input("Enter # to edit: "))
			if editOp == 1:
				print ""
				print "Editing Manga Download Location"
				print "Current Location: " + MangaSaveLocation
				newOption = raw_input("Enter New Location: ")
				if not os.path.exists(newOption):	
					print "Location doesn't exist"
					yesno = raw_input("Create Patch? (y/n)")
					if yesno == "y":
						try:
							os.makedirs(newOption)
							print newOption + " Created!"
						except:
							print "Couldn't create path. Did you make a mistake?"
					elif yesno == "n":
						print "kek"
				tmp = data["MangaSaveLocation"]
				data["MangaSaveLocation"] = newOption
				jsonFile = open("options.json", "w+")
				jsonFile.write(json.dumps(data))
				jsonFile.close()

			elif editOp == 2:
				print ""
			elif editOp == 3:
				print ""
			elif editOp == 4:
				print ""			


#####
###		tmp = data["MangaSaveLocation"]
#		data["MangaSaveLocation"] = "D:\FOLDERS\MangaSee Downloader\\"
#		data["two"] = "5"

		jsonFile = open("options.json", "w+")
		jsonFile.write(json.dumps(data))
		jsonFile.close()
		raw_input()
########################################
	if optionSet == 1:
		# Manga Name
		mangaurl = raw_input("Manga Name: ")
		print "Use -1 to download all avilable chapters!"
		# Chapter Number Start
		try:
			chapstart = int(raw_input("Chapter Number Start: "))
		except ValueError:
			print "That's not a number!"
		while chapstart <= -2:
			print "Chapeter Start # is wrong!"
			try:
				chapstart = int(raw_input("Chapter Number Start: "))
			except ValueError:
				print "That's not a number!"
		# Chapter Number End
		if chapstart == -1:
			chapend = 5000
		else:
			try:
				chapend = int(raw_input("Chapter Number End: "))
			except ValueError:
				print "That's not a number!"
		while chapend < chapstart:
			print "Chapeter End # is wrong!"
			try:
				chapend = int(raw_input("Chapter Number End: "))
			except ValueError:
				print "That's not a number!"
		print "==============================================="
		MangaDownload(mangaurl, chapstart, chapend)
	elif optionSet == 2:
		MangaSearch()
	elif optionSet == 3:
		MangaInfo()
	elif optionSet == 4:
		MangaUpdate()
	elif optionSet == 5:
		options()
	else:
		print "Option Set error"
