import pysftp
from dotenv import load_dotenv
import os

load_dotenv()

srv = pysftp.Connection(host=os.getenv("SFTP_IP"), username=os.getenv("SFTP_USER"), password=os.getenv("SFTP_PW"), private_key="./Path/To/File")
'''
with srv.cd(os.getenv("SFTP_FOLDER")):
    srv.put('test.txt')

srv.close()'''
data = srv.listdir()

# Closes the connection
srv.close()

# Prints out the directories and files, line by line
for i in data:
   print(i)