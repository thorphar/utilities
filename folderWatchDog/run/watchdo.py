#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import pysftp

import os
import sys

# In[2]:


if __name__ == "__main__":
    #print(sys.argv[1])
    file_path = sys.argv[1]
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


# In[3]:


#def on_created(event):

#def on_deleted(event):

def on_modified(event):
    event_file = event.src_path
    if event_file.endswith('.png'):
        event_file = os.path.abspath(event_file)
        srv = pysftp.Connection(host="192.168.1.113", username="bacton1",password="admin123")
        with srv.cd('test'): #chdir to public
            srv.put(event_file) #upload file to nodejs/

        # Closes the connection
        srv.close()
        
        print(f"EVENT[1]:{event.src_path} has been sent to sftp server")
    else:
        print(f"EVENT[0]:{event.src_path} has been modified")

#def on_moved(event):

#my_event_handler.on_created = on_created
#my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
#my_event_handler.on_moved = on_moved

path = file_path
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)


my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
