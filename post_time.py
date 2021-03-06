"""
The program  looks for the times that a Facebook user posted.
Use developer tools of the browser.

This is JavaScript snippet
---------------------------
abbr_tags = document.getElementsByTagName("abbr") #fill the abbr_tags variable 
						  #with all of the <abbr> tags
						  #that are currently found on the page

#walk through each of the abbr tags in our array and keep adding the timestamps to the empty string
timestamps = ""
for(var i = 0; i < abbr_tags.length; i++) { timestamps += 
			abbr_tags[i].getAttribute("data-utime") + "\r\n"; } 
			
copy(timestamps); #copy the variable into clipboard
------------------------------
"""

from datetime import datetime
import pprint
import csv
 
timestamps = """PASTE  CLIPBOARD HERE"""

time_frequency = {}
 
for i in range(24):
    time_frequency[i] = 0
	
for timestamp in timestamps.splitlines():
    date_obj = datetime.fromtimestamp(int(timestamp))
    hour     = date_obj.hour
    time_frequency[hour] += 1
	
with open("facebook-sleep.csv","wb") as csv_output:
    
    fieldnames=["Hour","Posts"]
    writer = csv.DictWriter(csv_output, fieldnames)
    writer.writeheader()
    
    for record in time_frequency:
        row = {}
        row['Hour']  = record
        row['Posts'] = time_frequency[record]
        writer.writerow(row)
    
    print "[*] Done writing facebook-sleep.csv!"
