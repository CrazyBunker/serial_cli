#!/usr/bin/python
import os
import time
import serial
import ProcessorShell

ser = serial.Serial( '/dev/ttyUSB0', 115200, timeout=0 )
sh = ProcessorShell.shell(ser)
path = './root'
while True:
   cmd = sh.treatment()
   if cmd == '?' or cmd =='help':
       dir_lst = b' '.join([ i.encode('utf-8') for i in os.listdir(path=path+'/'+b'/'.join(sh.path).decode('utf-8'))])
       print(dir_lst)
       sh.print_string(dir_lst)
   elif cmd == "..":
       try:
          del sh.path[-1]
       except IndexError:
           pass
   else:
       path_string = b'/'.join(sh.path).decode('utf-8')
       sep = ''
       if path_string:
           sep = '/'
       cmd_split = '/'.join(cmd.split())
       if os.path.isdir(path+sep+path_string+'/'+cmd_split):
           for i in cmd.split():
               sh.path.append(i.encode('utf-8'))
       else:
           print(path+sep+path_string+'/'+cmd_split)
           sh.print_string(b'Command: '+cmd.encode('utf-8'))

   sh.hello_text()




