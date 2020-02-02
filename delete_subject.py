#!/usr/bin/env python

import requests

# put your keys in the header
headers = {
    "app_id": "00ce9042",
    "app_key": "78c2465190532840fb5ead723a9a17e5"
}

payload = {"gallery_name": "Refugees",
           "subject_id": "19940811WU"}

url = "http://api.kairos.com/gallery/remove_subject"

# make request
r = requests.post(url, json=payload, headers=headers)
print (r.content)