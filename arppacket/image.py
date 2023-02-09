#!/usr/bin/env python

import os
import argparse
import socket
import time

id_user =  os.stat("./arp_spy.py").st_uid 
try:
  import requests
  from bs4 import BeautifulSoup    
except :
   os.system('pip install lxml /dev/null 2>1')
   os.system("pip install requests  /dev/null 2>1")
   os.system("pip install bs4  /dev/null 2>1")
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
              self.parent_dir= os.path.abspath("./capture/"+str(self.args.Target)+"/"+"Roaming")
              with open(self.parent_dir,'r') as file_url :
                   self.url_list = file_url.read().replace('http://','').replace('https://','').replace('[+] ',"https://").split()                           
      def DownLoad_Images(self):
         try:
            Count_images = 8
            Imagepath = os.chdir("./capture/"+str(self.args.Target)+"/"+"Images/")   
            for url in self.url_list[4:] : 
               try: 
                  if '/' not in url[0]:        
                     url = url[0:]+"/"
                  else:
                      url=url
                  request = requests.get(url)
                  socket.setdefaulttimeout(6) 
                 # connect  = BeautifulSoup(request.text,'html.parser')
                  connect   = BeautifulSoup(request.text, "lxml-xml")             
                  images = connect.find_all('img')
                  for img in images:
                      try:
                         Count_images -=1
                         if Count_images == 0 :
                             break
                         name = img['alt']
                         link = img['src']
                         with open (name +".png",'wb+') as links :
                            im = requests.get(link)
                            links.write(im.content)
                            os.chown("*.* ", id_user, id_user)

                      except Exception as f :
                         continue 
               except requests.exceptions.ConnectionError  :
                      continue
         except Exception  :          
                with open(str(Imagepath)+"Images.txt",'w') as file_url :
                     os.chown(str(Imagepath)+"Images.txt", id_user, id_user)
                     print ("[+] No Images has been Capture") 
                     url_list = file_url.write("\n [+] No Images has been Capture" ) 
                     exit()
                                                                              
if __name__=='__main__':
   ImagesDownLoad()   
   
   
         
