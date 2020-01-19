import os
import sys
print "Choose directory to commit genocide on the files."
Dir = raw_input("> ")
def deleteFiles(path):
    currentDir = os.listdir(path)
    for i in currentDir:
        i = path + "/" + i
        if os.path.isfile(i):
            print "deleting",i
            os.remove(i)
        else:
            print "found folder:",i
            deleteFiles(i)
            os.rmdir(i)
    
deleteFiles(Dir)
