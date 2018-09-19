import os

def run(**args):
    print '[*] In Dir module.'
    files = os.listdir('.') #Get list of files by listing current directory.

    return str(files)
