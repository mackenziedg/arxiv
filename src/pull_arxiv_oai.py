import pickle
import requests
from time import sleep, time
import xml.etree.ElementTree as ET

wait_time = 10
text = []

url = "http://export.arxiv.org/oai2"
payload = {"verb": "ListRecords",
            "set": "cs",
            "metadataPrefix": "arXiv"}

r = requests.get(url, params=payload)
if r.status_code == 200:
    text.append(r.text)

old_time = time()

e = [ET.fromstring(i) for i in text]
res_token = e[-1][2][-1].text
num_records = e[-1][2][-1].attrib["completeListSize"]
print(res_token+" out of "+str(num_records))

while True:
    p = {"resumptionToken": res_token,
        "verb": "ListRecords"}

    if time() - old_time < wait_time:
        sleep(wait_time - (time()-old_time))
    r = requests.get(url, params=p)
    if r.status_code == 200:
        text.append(r.text)
    else:
        sleep(wait_time)
        continue

    old_time = time()
    e = [ET.fromstring(i) for i in text]
    try:
        res_token = e[-1][2][-1].text
        print(res_token+" out of "+str(num_records))
    except:
        print("Done reading in.")
        with open("cs_arxiv.pickle", "wb") as f:
            pickle.dump(file=f, obj=e)
