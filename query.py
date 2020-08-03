#required libraries are imported like below.
import os
import linecache
from collections import deque
import itertools
from itertools import islice
import datetime
import time
import sys
from netaddr import IPNetwork
#query format used "QUERY 192.0.0.57 1 2020-06-21 23:54 2020-06-22 00:15"
def validateIP(ip):
        if(ip in IPNetwork('192.0.0.0/22')):            #IP address is validated to be in a given network
            return True
        else:
            print("IP Address out of range. Sould be between 192.0.0.0 to 192.0.3.231") 
            fetch()  
def validateTime(t):            #validating start and end time formats
    try:
        datetime.datetime.strptime(t, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        print("Invalid time format. Should be YYYY-MM-DD HH:MM")
        fetch()

#function definition for fetching query data
def fetch():
    
    flag=False
    data=input("\nEnter your request:\n")        #console input is stored in a variable named data
    data=data.split(" ")        #data is converted into a list separated by space, for better manipulation
    request_type=data[0]        #1st argument will be taken as reqest_type
    if(request_type.lower()=="query"):      #checking condition of request_type being QUERY or query format
        if(len(data)!=7):
            print("Invalid number of arguments, please check again!")
            fetch()
        ip=data[1]          #requested ip address is stored in variable ip
        validateIP(ip)      #validateIP function is called to validate IP address
        cpu_id=data[2]      #requested cpu id is stored in cpu_id        
        
        if(not(int(cpu_id)==0 or int(cpu_id)==1)):      #checking condition for invalid cpu id
            print("Invalid CPU ID, Should be either 0 or 1 !!")     #error message to be displayed and then exit
            fetch()
        output=()       #initilaizing tuple to store data

        #storing different request data into variables
        start_date=data[3]
        start_time=data[4]
        end_date=data[5]
        end_time=data[6]
        final_output=deque()
        st_time=start_date+" "+start_time
        validateTime(st_time)           #validateTime function is called to validate time format 
        en_time=end_date+" "+end_time
        validateTime(en_time)           #validateTime function is called to validate time format
        input_start_timestamp=int(datetime.datetime.strptime(st_time,"%Y-%m-%d %H:%M").timestamp())       #converting requested start date and time into timestamp
        input_end_timestamp=int(datetime.datetime.strptime(en_time,"%Y-%m-%d %H:%M").timestamp())             #converting requested end date and time into timestamp
        if(input_end_timestamp<input_start_timestamp):
            print("Start date time should be earlier than End date time")
            fetch()
        with open(file_name, 'rb') as f:            #reading file to get the last_log_time
            time1= time.time()
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()    
        last_log_time=last_line.split(" ")[1]
        
        if(int(last_log_time)<input_start_timestamp):
            print("Logs are earlier than "+datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(last_log_time)),"%Y-%m-%d %H:%M")+" , please change your start date")
            fetch()
        if(int(last_log_time)<input_end_timestamp):
            input_end_timestamp=int(last_log_time)    

        with open(file_name) as f:      #condition for reading file to get the index of first occurence of the requested IP
            for num,i in enumerate(f,2):
                temp_list=i.split(" ")
                if(temp_list[2]==ip and int(temp_list[3])==int(cpu_id)):
                    n=num
                    flag=True
                    break
        
        with open(file_name) as f:        
                skipped = islice(f,n-2, None,2000)  
                for i, line in enumerate(skipped,1):
                    
                    temp_list2=line.split(" ")
                    if(int(temp_list2[1])>input_end_timestamp):      #matching condition with the timestamp, if the record timestamp is greater than the requested one, then exit.
                        break
                
                    elif(int(temp_list2[3])==int(cpu_id) and int(temp_list2[1])>=input_start_timestamp and int(temp_list2[1])<=input_end_timestamp):       #matching condition for cpu_id, start time and end time
                        dt_format=datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(temp_list2[1])),"%Y-%m-%d %H:%M")       #converting timestamp into datetime format
                        output=(dt_format,temp_list2[4].rstrip()+"%")        #generating output tuple for particular time.
                        final_output.append(output)         #appending output tuple to final_output list       
                
        if(flag):           #checking condition for displaying result
            

            if(len(final_output)):
                print("CPU"+cpu_id+" usage on "+ip+":")
                print("{} \nTotal time taken by query:{} seconds".format(list(final_output),time.time() - time1))
            
            else:
                print("Request is out of log data")    
            fetch()
            
        if(not flag):       #if flag is False then no IP is found in generated logs. Hence invalid IP Address.
            print("Invalid IP Address !!")    
            fetch()
    elif(request_type.lower()=="exit"):         #checking condition of request_type being EXIT or exit
        if(len(data)!=1):
            print("Invalid number of arguments, should be EXIT/exit only")
            fetch()
        else:    
            exit(0)
    else:           #if request_type is other than QUERY(query) format or EXIT(exit), then below error message is displayed.
        print("Invalid request type, Should be either QUERY format or EXIT !!")           
        fetch()          
if(len(sys.argv)!=2):
    print("Invalid number of arguments.Request should be like: python query.py DATA_PATH")
    exit(0)    
fn=sys.argv[1]          #fetching directory name from command line
file_name=fn+"/cpu.log"
fetch()