#!/usr/bin/env python
import re 
import os
import argparse
import sys
class Gerp_Links :
      
      def __init__(self):
          self.arg_parse()
          listBox = []
          listbrowser=[
             'google chrome','google','firefox','opera','safari','internet explorer',
             'slimjet','duckduckgo','maxthon','slimbrowser','netscape','uc'
            ]
          with open ("./capture/"+str(self.args.Target)+'/service','w') as service :
               service.write('\n'+"="*30+'\n'+ "DNS and SErvice" + '\n'+'='*40+'\n')
          with open ("./capture/"+str(self.args.Target)+'/Roming','w') as Roming1 :
               Roming1.write('\n'+"="*30+'\n'+ "Web_vist_list" + '\n'+'='*40+'\n')
          path= str(os.getcwd())+"/capture/"+str(self.args.Target)+'/'+str(self.args.Target)
          command = 'strings -n 10 '+path+' > '+ str(os.getcwd())+'/capture/'+str(self.args.Target)+'/data'
          os.system(command )    
          with open ("./capture/"+str(self.args.Target)+'/data','r') as Data:
               Adata = Data.readlines()   
          for line in Adata:
              domain = str(re.search('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', line)).split()
              ip_re = (domain[-1][7:-2])
              if ip_re not in listBox:
                 listBox.append(ip_re)
          with open("./capture/"+str(self.args.Target)+"/.Web.txt",'w') as data:
               data = data.write(str("\n".join(listBox)))
          with open("./capture/"+str(self.args.Target)+"/.Web.txt",'r') as data:
               data = data.readlines()
          for line in data :
               if "."in line[0] or ".digicert" in line or 'crl' in line\
                  or 'pkiops' in line or 'pki' in line or 'com0' in line\
                  or 'external' in line  or 'clients3' in line\
                  or 'fonts.' in line  : 
                     with open ("./capture/"+str(self.args.Target)+"/service",'a') as service:
                          service_Dns = service.write('[+] '+line)
               else:        
                    if 'http' in line[1:5] :
                       with open ("./capture/"+str(self.args.Target)+'/Roming','a') as Roming1:
                           Roming = Roming.write('[+] '+line[1:])
                    elif 'https'in line[0:5]:
                       with open ("./capture/"+str(self.args.Target)+'/Roming','a') as Roming1:
                           Roming = Roming1.write('[+] '+str(line))
                    elif 'www' in line[0:3]:
                        if '0'in line[-2] or '1' in line[-2]:
                              pass
                        else:
                             with open ("./capture/"+str(self.args.Target)+'/Roming','a') as Roming1:
                                Roming = Roming1.write('[+] '+line)
                    else:
                         for browser in listbrowser:
                             if browser  in line:                                        
                                with open ("./capture/"+str(self.args.Target)+'/Roming','a') as Roming1:
                                     Roming = Roming1.write('[+] '+str(line))
      def arg_parse(self):
             parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
             parser.add_argument( '-I',"--Interface")
             parser.add_argument( '-M',"--dest"     )  
             parser.add_argument( '-T',"--Target"   )
             parser.add_argument( '-R',"--repate"   )
             parser.add_argument( '-W',"--Wireshark",action='store_true')
             self.args = parser.parse_args()
             if len(sys.argv)> 1 :
                pass
             else:
               parser.print_help()
               exit()  
if __name__=='__main__':
     Gerp_Links()



