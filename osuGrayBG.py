''' Imports 
os - To get Dirs and load deelete files
glob - Match filetype
time - Less chance of Python being dumb
'''
import os, glob, time

''' Delete all 'extra' filetypes and create empty array '''
types = ('*.wav', '*.jpg', '*.png', '*.avi')
files_grabbed = []

''' Get user to input osu! Location '''
osuDir = raw_input("osu.exe Folder Location (Leave blank if Program Files (x86)): ")

''' If empty then set default Loc '''
if osuDir == "":
	osuDir = os.path.dirname(os.path.realpath(__file__))[0:3] + "Program Files (x86)\\osu!\\" 

''' Quick check if the user misunderstood and linked the Songs folder '''
if "Songs" in osuDir:
		pass
else:
		osuDir = osuDir + "Songs\\"

''' For each folder in the Songs folder:
Print the Map Folder name (so the user knows where it's at)
Change Dir to the map folder
For each file in the map folder check if the filetype is in the list types
Place each file from there into the empty array
For each file in the array, delete.
Print error incase it happens '''

for songfolder in os.listdir(osuDir):
	try:
		time.sleep(1)
		print songfolder
		os.chdir(osuDir + songfolder)
		for infolder in types:
			files_grabbed.extend(glob.glob(infolder))
		for file in files_grabbed:
			print file
			try:
				os.remove(osuDir + songfolder + "\\" + file)
				print "DELETED: " + osuDir + songfolder + "\\" + file
			except:
				pass
	except:
		print "Error: ", songfolder
		print "Passing..."
		pass

raw_input("Finished! (Press Enter to close!)")
