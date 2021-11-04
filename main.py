#import pysftp
import os
from dotenv import load_dotenv
from utils import log
import json
import requests
load_dotenv()

def handle_http(item):
    r = requests.get(item["info"]["url"], auth=('user', 'pass'))
    data = {
        "status": r.status_code,
        "text": r.text,
        "elapsed": str(r.elapsed),
        "headers": str(r.headers),
        "url": r.url,
    }
    return data

def save_data(data, item):
    with open(item["desc"]+".json", "w") as f:
        json.dump(data, f, indent=4)

supported_types = {
    "http":handle_http
}

'''
srv = pysftp.Connection(host=os.getenv("SFTP_IP"), username=os.getenv("SFTP_USER"), password=os.getenv("SFTP_PW"), private_key="./Path/To/File")
data = srv.listdir()

# Closes the connection
srv.close()

# Prints out the directories and files, line by line
for i in data:
   print(i)
'''

def main():
    try:

        log("main", "Started. Loading hosts.json...")
        with open("hosts.json") as f:
            items = json.load(f)
        log("main", "Hosts.json loaded")

        for item in items:

            if type(item["desc"]) is str and type(item["type"]) is str and type(item["info"]) is dict:
                log(item["desc"], "Preliminary fields checked")
            else:
                raise Exception("Wrong preliminary fields' type")
            
            if item["type"] in supported_types.keys():
                log(item["desc"], "Supported. Now starting...")
                data = supported_types[item["type"]](item)
                save_data(data, item)
            else:
                log(item["desc"], "Not supported")
                raise Exception("Unsopported type")

    except Exception as e:
        log("error", e)

if __name__ == "__main__":
    main()