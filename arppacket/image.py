#!/usr/bin/env python

import os
import argparse
import socket
import time
try:
  import requests
  from bs4 import BeautifulSoup    
except :
   os.system("pip install requests  /dev/nul 2>1")
   os.system("pip install bs4  /dev/nul 2>1")
   import requests
   from bs4 import BeautifulSoup 
   
class ImagesDownLoad:          
      def __init__(self):
          parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
          parser.add_argument( '-I',"--Interface")
          parser.add_argument( '-M',"--dest"     )  
          parser.add_argument( '-T',"--Target"   )
          parser.add_argument( '-R',"--repate"   )
          parser.add_argument( '-W',"--Wireshark",action='store_true')
          self.args = parser.parse_args()
          self.read_file_url()
          self.DownLoad_Images()
           
      def read_file_url(self):      
              self.parent_dir= os.path.abspath("./capture/"+str(self.args.Target)+"/"+"Roming")
              with open(self.parent_dir,'r') as file_url :
                   self.url_list = file_url.read().replace('[+] ',"https://").split()
      def DownLoad_Images(self):
         try:
            Imagepath = os.chdir("./capture/"+str(self.args.Target)+"/"+"Images/")   
            for url in self.url_list[4:] : 
               try: 
                  if '/' not in url[0]:        
                     url = url[0:]+"/"
                  else:
                      url=url[0]
                  print(url)
                  request = requests.get(url)
                  socket.setdefaulttimeout(6) 
                  connect  = BeautifulSoup(request.text,'html.parser')
                  images = connect.find_all('img')
                  for img in images:
                      try:
                         name = img['alt']
                         link = img['src']
                         with open (name +".png",'wb+') as links :
                            im = requests.get(link)
                            links.write(im.content)
                            time.sleep(0.30)
                      except Exception as f :
                         continue 
               except requests.exceptions.ConnectionError  :
                      continue
         except Exception  :          
                with open(str(Imagepath)+"Images.txt",'w') as file_url :
                     print ("[+] No Images has been Capture") 
                     url_list = file_url.write("\n [+] No Images has been Capture" ) 
                     exit()
                                                                              
if __name__=='__main__':
   ImagesDownLoad()   
   
   
         
