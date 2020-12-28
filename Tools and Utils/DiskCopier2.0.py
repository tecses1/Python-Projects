import sys
import os
import time
from shutil import copyfile

def stopWatch(value):
    '''From seconds to Days;Hours:Minutes;Seconds'''

    valueD = (((value/365)/24)/60)
    Days = int (valueD)

    valueH = (valueD-Days)*365
    Hours = int(valueH)

    valueM = (valueH - Hours)*24
    Minutes = int(valueM)

    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)


    print (Days,"days;",Hours,"hours;",Minutes,"minutes;",Seconds, "seconds.")
    
def fileCopier(rootPath, copyPath):
    try:
        paths = os.listdir(rootPath)
    except WindowsError:
        return;
    if not os.path.exists(copyPath):
        os.mkdir(copyPath)
        
    for x in paths:
        fullPath = rootPath + "/" + x
        fullCopyPath = copyPath + "/" + x
        if os.path.isfile(fullPath):
            #Copy the file here

            #print ( "Copying " + fullPath + " to " + fullCopyPath )

            try:
                if os.path.exists(fullCopyPath):
                    ##print ("The file " + fullCopyPath + " already exists!")
                    pass
                else:
                    print ("Copying missed file: " + fullCopyPath)
                    copyfile(fullPath, fullCopyPath)
                    #print (" OK ")
            except IOError:
                #print (" FAILED ")
                pass
        else:

            fileCopier(fullPath, fullCopyPath)
log = ""
sys.dirPaths = []
sys.files = 0
sys.dirs = 0
sys.bytes = 0
def RecursiveFind(path):
    try:
        paths = os.listdir(path)
    except WindowsError:
        return;
    for x in paths:
        fullPath = path + "/" + x
        if os.path.isfile(fullPath):
    	    sys.bytes += os.path.getsize(fullPath)
    	    sys.files += 1
        else:
            sys.dirPaths.append(fullPath)
            sys.dirs += 1
            RecursiveFind(fullPath)


print ("List the directory you want to copy.")
path1 = input("> ")

if not os.path.exists(path1):
    print ("That path doesn't exist!")
else:
    
    print ("List the target directory.")

    path2 = input("> ")
	
    print ("Recursing to find files, this may take a while...")
    
    RecursiveFind(path1)
    
    print ("Total Directories:",sys.dirs)
    print ("Total Files:", sys.files)
    print ("Total Bytes:",sys.bytes / (1000 * 1000)," MB")
    
    print ("Ready to copy, press any key to continue...")
    
    startTime = time.time()
    input("")
    

    if not os.path.exists(path2):
        os.mkdir(path2)

    for cPath in sys.dirPaths:
        try:
            copyPath = path2 + cPath.replace(path1, "")
            
            
            if not os.path.exists(copyPath):
                os.mkdir(copyPath)
               
            
            print ("Copying " + cPath + " to " + copyPath + ": ")
            log += "Copying " + cPath + " to " + copyPath + ": \n"
            
            cPaths = os.listdir(cPath)
            for p in cPaths:

                originalFile = cPath + "/" + p
                copyFile = copyPath + "/" + p
                
                sys.stdout.write("    " + p + " ...... ")
                log += "    " + p + " ...... "
                if os.path.isfile(originalFile):
                    try:
                        if os.path.exists(copyFile):
                            print ("[FAILED] - Already Exists.")
                            log += "[FAILED] - Already Exists.\n"
                        else:
                            copyfile(originalFile, copyFile)
                            print ("[OK]")
                            log += "[OK]\n"
                    except IOError:
                        print ("[FAILED] - IOError.")
                        log += "[FAILED] - IOError.\n"
        except IOError:
            print ("[ERROR] Permission denied to dir: " + cPath)
            log += "[ERROR] Permission denied to dir: " + cPath + "\n"

    print ("Writing log...")
    
    file = open("log.txt",mode="w",encoding="utf-8")
    file.write(log)
    file.close()
        
    print ("Finished first pass. Took ")

    
    stopWatch(time.time()-startTime )
    
    input("")

    startTime = time.time()
    print ("Verifying integrity... Press CTRL+C to skip.")

    
    fileCopier(path1, path2)
    stopWatch(time.time()-startTime )
    input()
