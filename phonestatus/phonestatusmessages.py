#created by lfane
#1/21/18; generates report of status messages pages from phone
import sys
import requests
import datetime
from bs4 import BeautifulSoup

#Check that arguments where passed
if len(sys.argv) ==3:
    #Open text file containing phone IPs
    now=datetime.datetime.now()
    filePhoneReport = open(sys.argv[2],"w")
    logfilename = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + "-statuslog.txt"
    logfile = open(logfilename, 'w')
    #Open the text file containing the phoneIPs and put the IPs into a list
    with open(sys.argv[1]) as temp_file:
        mylist = temp_file.read().splitlines()
        n = len(mylist)
        print("Starting to retrive phone status messages: ",end="")
        print (now.strftime("%Y-%m-%d %H:%M"))
        print ("There are ",end="")
        print(n,end="") 
        print(" items in your list")
        logfile.write("Starting to retrive phone status messages: ")
        logfile.write((now.strftime("%Y-%m-%d %H:%M"))) 
        logfile.write("\n")
        logfile.write("There are "+ str(n)+" items in your list")
        logfile.write("\n")
    #Loop through the IPs in the list; attempt to get URL, if the URL throws an exception, move on
    for phoneIP in mylist:
        phoneURL=("http://"+ phoneIP+"/CGI/Java/Serviceability?adapter=device.settings.status.messages")
        try:
            r=requests.get(phoneURL)
            print("Fetching the status messages for: "+ phoneIP)
            logfile.write ("Fetching the status messages for: "+ phoneIP)
            logfile.write("\n")
            page = requests.get(phoneURL)
            soup = BeautifulSoup(page.text, 'html.parser')
            table_div = soup.find('div')
            table = table_div.find('table')
    
             #Print content row separated by commas
            content=""
            for row2 in table.find_all('tr'):
                for td in row2.find_all('td')[1]:
                    content = content+ "," + td.text
            filePhoneReport.write(content[1:])
            filePhoneReport.write("\n")
        except requests.exceptions.RequestException as err:
            print("ERROR with: " + phoneIP + "...SKIPPED")
            logfile.write ("ERROR with: " + phoneIP + "...SKIPPED")
            logfile.write("\n")
            pass
    filePhoneReport.close()
    print ("Phone information gathering completed at ",end="")
    print (now.strftime("%Y-%m-%d %H:%M"))
    print ("Generated log file: " + logfilename)
    logfile.write ("Phone information gathering completed at "+now.strftime("%Y-%m-%d %H:%M"))
    logfile.close()
else:
    print("ERROR: Not enough arguments.  Please pass an input and output file")
    print("Example: python phone-info.py phoneinfo.txt myreport.csv")
    print("If the text file containing the list of IPs is not in this same directory, include the path")
    print("Exiting Now.")