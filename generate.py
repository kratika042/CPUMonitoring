import time

import random
import logging
from netaddr import IPNetwork
from os import path
import os
import sys

if(len(sys.argv)!=2):
    print("Invalid number of arguments.Request should be like: python generate.py DATA_PATH")
    exit(0) 
fn=sys.argv[1]
if(not path.exists(fn)):
    os.mkdir(fn)
file_name=fn+"/cpu.log"
log_format=" %(message)s"           #format for logging data into the file.
logging.basicConfig(filename=file_name,level=logging.DEBUG, format=log_format)

logging.info("Timestamp IPAddress CPU_Id CPU_Usage")        #initial line of fields of log file, representing the data in sequence below.

#initializing variables needed for generating logs
cpu_id1=0
cpu_id2=1
max_time=1440
count=1
timestamp=int(time.time())

list_ip=[ip for ip in IPNetwork('192.0.0.0/22')]        #192.0.0.0/22 will be the subnet to generate 1000 servers, generated IPs are stored in list_ip
if(path.exists(file_name)):         #file has successfully created and logs are being generated
        print("logs are being generated, Please wait!, It will take some time")
else:
    print("Some error occurred while creating log file, Please check your permission settings")         #error message if file cannot be created.
    exit(0)
for t in range(max_time+1):             #loop for generating records for 1 day
    for i in range(1000):               #loop for generating 1000 servers
        cpu_usage1=random.randint(0,100)        #randomly generating CPU Usage for 1st CPU of a server
        cpu_usage2=random.randint(0,100)        #randomly generating CPU Usage for 2nd CPU of a server
        data=str(timestamp)+" "+str(list_ip[i])+" "+str(cpu_id1)+" "+str(cpu_usage1)        #data with the requested fields is generated for 1st CPU
        logging.info(data)          #data for 1st CPU is logged into the file cpu.log
        data=str(timestamp)+" "+str(list_ip[i])+" "+str(cpu_id2)+" "+str(cpu_usage2)        #data with the requested fields is generated for 2nd CPU
        logging.info(data)          #data for 2nd CPU is logged into the file cpu.log
    timestamp+=60           #timestamp is increased to show 1 min increment
print("Logs have successfully generated with filename cpu.log")    