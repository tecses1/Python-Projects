import os, sys, shutil
import ctypes
if ctypes.windll.shell32.IsUserAnAdmin() != True:
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
class FileCopier:
    def __init__(self,source,target):
        self.totalSize = 0
        self.totalFiles = 0
        self.totalDirectories = 0
        self.uncopiedFiles = 0
        if os.path.exists(target)!= True:
            os.mkdir(target)
        self.copyTo(source,target)
    def copyTo(self,sourcepath,targetpath):
        try:
            Dir = os.listdir(sourcepath)
        except WindowsError, err:
            print err
            return err
        for i in Dir:
            csource = sourcepath + "/" + i
            ctarget = targetpath + "/" + i
            if os.path.isfile(csource):
                if os.path.exists(ctarget) != True:
                    print "Copying",csource
                    self.totalFiles += 1
                    self.totalSize += (os.path.getsize(csource)/1000)
                    try:
                        shutil.copyfile(csource,ctarget)
                    except IOError, e:
                        print e
                        
                    except WindowsError, e:
                        print e
                        
                else:
                    print "Skipping dupe",csource
                    self.uncopiedFiles += 1
            else:
                self.totalDirectories += 1
                if os.path.exists(ctarget):
                    self.copyTo(csource,ctarget)
                else:
                    try:
                        os.mkdir(ctarget)
                        self.copyTo(csource,ctarget)
                    except WindowsError, err:
                        print err
                        return
print("What is the source directory?")
source = raw_input("> ")
print ("What is the target directory?")
target = raw_input("> ")
fileboi=FileCopier(source,target)
print "Total Files: " + str(fileboi.totalFiles) + "\nTotal Directories: " + str(fileboi.totalDirectories)\
      + "\nTotal Size (MB): " + str(fileboi.totalSize / 1000)
if fileboi.uncopiedFiles > 0:
    print "Uncopied Files: " + str(fileboi.uncopiedFiles)
raw_input()
    
