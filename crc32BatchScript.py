import os, sys
import zlib # crc32 shit
from os import rename, listdir
import fnmatch

''' Doesn't support big files (around 1~gb don't know away around this :|)
    
    Place the .py in where you want to batch rename
    have the files like so: WhatEver.mkv - it'll rename the .mkv to [crc32].mkv keeping the name and whatnot.

'''

crcDir = os.path.dirname(os.path.realpath(__file__)) + "\\"
filePre = ".mkv"

for file in os.listdir(crcDir):
    try:
        if fnmatch.fnmatch(file, '*.mkv'):
                tempcrfc = " [" + "%X"%(zlib.crc32(open(crcDir+file,"rb").read()) & 0xFFFFFFFF) + "]"
                if tempcrfc in file:
                    continue
                rename(crcDir+file, crcDir+file.replace(filePre, tempcrfc + filePre))
    except MemoryError:
        print "MemoryError - Filesize too big"
        raw_input("Press Enter")
        sys.exit()
    except:
        print "Unknown Error"
        raw_input("Press Enter")
        sys.exit()
