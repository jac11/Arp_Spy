#!/usr/bin/env python


import argparse
import subprocess
import sys
import os
import time 
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
               if self.args.repate:
                    args = '-I '+self.args.Interface+' -T '+ self.args.Target +' -M ' +self.args.dest +' -R '+ self.args.repate+' '
               else:
                    args = "-I "+self.args.Interface+" -T "+ self.args.Target +" -M " +self.args.dest 
               command_proc = 'gnome-terminal  -e ' +'"'+' ./arp_attack.py ' + args +'"'                  
               call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)     
        def arg_pares_on(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
            parser.add_argument( '-I',"--Interface"  ,dest = "Interface" ,required=True  , metavar='' , action=None )
            parser.add_argument( '-M',"--dest"       ,dest = "dest"      ,required=True  , metavar='' , action=None )
            parser.add_argument( '-T',"--Target"     ,dest = "Target"    ,required=True  , metavar='' , action=None )
            parser.add_argument( '-R',"--repate"     ,dest = "repate"    ,required=False , metavar='' , action=None )
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
               pass
            else:
               parser.print_help()
               exit()  
if __name__=='__main__':
     Controll()
  
       

