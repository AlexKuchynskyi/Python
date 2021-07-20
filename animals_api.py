#!/usr/bin/python3

#################################################################
'''
## Setup
To get started make sure you have Docker, or some way to run  provided container

1. Start by downloading the Docker image: (it's in the local storage currently - lp-programming-challenge-1-1625758668.tar.gz)
2. Load the container: `docker load -i lp-programming-challenge-1-1625758668.tar.gz`.
3. The output there should tell you what it imported. Go ahead and run it, and be sure to expose port `3123`
   so you can access it: `docker run --rm -p 3123:3123 -ti lp-programming-challenge-1`
4. Try opening  `http://localhost:3123/` to see if things are working.

## The API
The `animals` API is running on port `3123` and it has a few endpoints:

### `/animals/v1/animals`
Make a `GET` here to list the collection of animals. You'll receive a limited set of animals,
and have request each page to unroll the whole list. Use the `page` query param to get other pages.

### `/animals/v1/animals/<id>`
Make a `GET` here to get the details for an animal.
`<id>` should be the `id` in the listing response.

### `/animals/v1/home`
This endpoint accepts `POST` request with a JSON array of Animal detail responses, with some minor changes:
1. The `friends` field must be translated to an array from a comma-delimited string.
1. The `born_at` field, if populated, must be translated into an ISO8601 timestamp in UTC.

Think of this one as a separate server, but bundled here for simplicity.

### `/docs`
The OpenAPI docs for the server. Take a look through here to see schema details.

There is one pain point to contend with:
* The server can randomly pause for 5-15 seconds.
* The server can randomly return HTTP 500, 502, 503 or 504.


This script does:
1. Fetch all Animal details
2. Transform `friends` into an array
3. `POST`   Animals to `/animals/v1/home`.
The goal is to write code that can reliably load every animal.
'''
###################################################################

import requests
import json
import time
from datetime import datetime, timezone

# getting total amount of animals
initial_response = requests.get("http://localhost:3123/animals/v1/animals/").json()
total_pages=initial_response["total_pages"]
print("Total pages: " + str(total_pages))
initial_response = requests.get("http://localhost:3123/animals/v1/animals?page=" + str(total_pages)).json()
last_id=list(initial_response["items"])
last_id=(dict(last_id[-1])['id'])
print ("Total amount of animals (Last ID): " + str(last_id))
time.sleep(5)

list_of_IDs = list(range (1, last_id+1))
exceptions_list = []

# will write details for each animal to the file for logging purpose and the ability to self check
loaded_file = "animals_get.json"
json_file = open(loaded_file, mode='w', encoding='latin_1')

# will write possible POST errors to the file for logging purpose the ability to self check
post_file = "post_file.txt"
txt_file = open(post_file, mode='w', encoding='latin_1')

# as server randomly returns 5** errors - these errors will be written to the exceptions_list
# and then make requests again with the IDs from this exceptions_list
# to make sure that every animal is loaded
while len(list_of_IDs) > 0:
    print ("======================== new loop===============")
    for ID in list_of_IDs:
        try:
            get_response = requests.get("http://localhost:3123/animals/v1/animals/" + str(ID)).json()
        except:
            exceptions_list.append(ID)
        else:
            print (str(ID))
            print (get_response)

                        # translating 'born_at` field  into an ISO8601 timestamp in UTC
            if get_response["born_at"]: get_response["born_at"]=datetime.utcfromtimestamp(get_response["born_at"]/1000).isoformat()

                        # translating 'friends` field  to an array
            get_response["friends"]=get_response["friends"].split(",")
            print ('Corrected request: ' + str(get_response))
            json_file.write(str(get_response))
            json_file.write('\n')

                        # organizing payload for POST request
            payload = json.dumps([get_response])
            post_response = requests.post("http://localhost:3123/animals/v1/home", data=payload)
            if post_response.status_code != 200:
                print ("======================== 5** ERROR during POST - waiting for 5 seconds and try again ===============")
                txt_file.write(str (ID) + '  ' + str(post_response))
                txt_file.write('\n')
                time.sleep(5)
                post_response = requests.post("http://localhost:3123/animals/v1/home", data=payload)
            print ('POST response: ' + str(post_response))
            txt_file.write(str (ID) + '  ' + str(post_response))
            txt_file.write('\n')
    list_of_IDs = exceptions_list
    if len (exceptions_list) > 0:
        print ('\n')
        print ('These IDs got to the list of exceptions (will be requested again):')
        print (exceptions_list)
        print ("======================== 5** ERRORS during GET - waiting for 10 seconds before new loop ===============")
    exceptions_list = []
    time.sleep(10)

json_file.close()
txt_file.close()
