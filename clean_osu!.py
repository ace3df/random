''' Imports 
os - To get Dirs
glob - Match filetype
time - Less chance of Python being dumb
'''
import os, glob, time
 
''' Delete all 'extra' filetypes, create empty array and set total deleted size '''
types = ('*.wav', '*.jpg', '*.png', '*.avi', '*.db')
files_grabbed = []
total_del = 0

''' Get user to input osu! Location '''
osuDir = raw_input("osu.exe Folder Location (Leave blank if Program Files (x86)): ")

''' If empty then set default Loc '''
if osuDir == "":
	try:
		osuDir = os.path.dirname(os.path.realpath(__file__))[0:3] + "Program Files (x86)\\osu!\\"
		''' Test if osu! in the folder. If not try most common drive name '''
		print(osuDir.exists("/osu!.exe"))
	except:
		osuDir = "C:\\Program Files (x86)\\osu!\\" 

''' Quick check if the user misunderstood and linked the Songs folder '''
if "Songs" in osuDir:
		pass
else:
		osuDir = osuDir + "BOB\\"

''' For each folder in the Songs folder: 
Print the Map Folder name (so the user knows where it's at)
Change Dir to the map folder
For each file in the map folder check if the filetype is in the list types
Place each file from there into the empty array
For each file in the array, delete.
Print error incase it happens '''
print "Deleting..."
for songfolder in os.listdir(osuDir):
	try:
		os.chdir(osuDir + songfolder)
		for infolder in types:
			files_grabbed.extend(glob.glob(infolder))
		for file in files_grabbed:
			try:
				total_del = total_del + os.path.getsize(osuDir + songfolder + "\\" + file)
				os.remove(osuDir + songfolder + "\\" + file)
			except:
				pass
	except:
		print "Error: ", songfolder
		print "Passing..."
		pass
		
total_del = (total_del / 1024) / 1024
print("Total Space Saved: ") + str(total_del) + "MB"
raw_input("Finished deleting extra files!")