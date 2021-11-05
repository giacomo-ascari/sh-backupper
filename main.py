#import pysftp
import os
from dotenv import load_dotenv
from utils import log
import time
import datetime
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

def save_data(data, item, date):
    if not os.path.exists(date):
        os.mkdir(date)
    with open(date + "/" + item["desc"]+".json", "w") as f:
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

        d = datetime.datetime.now()
        date = "{:%Y%m%d-%H%M%S}".format(d)
        log("main", "Started: "+ date)
        log("main", "Loading hosts.json...")
        with open("hosts.json") as f:
            items = json.load(f)
        log("main", "Hosts.json loaded")

        for item in items:

            if type(item["desc"]) is str and type(item["type"]) is str and type(item["info"]) is dict:
                log(item["desc"], "Preliminary fields checked")
            else:
                raise Exception("Wrong preliminary fields' type")
            
            if item["type"] in supported_types.keys():
                try:
                    log(item["desc"], "Supported. Now starting...")
                    data = supported_types[item["type"]](item)
                    save_data(data, item, date)
                    log(item["desc"], "Saved")
                except:
                    log(item["desc"], "ERROR. Not saved")
            else:
                log(item["desc"], "ERROR. Not supported")
        try:
            if os.path.exists(date):
                log("sftp", "Establishing connection...")
                srv = pysftp.Connection(host=os.getenv("SFTP_IP"), username=os.getenv("SFTP_USER"), password=os.getenv("SFTP_PW"))
                data = srv.listdir()
                srv.close()
                for i in data:
                    print(i)
        except:
            log("sftp", "ERROR")


    except Exception as e:
        log("error", "Unhandled error", e)

if __name__ == "__main__":
    main()