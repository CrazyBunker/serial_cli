#!/usr/bin/python
import os
import serial
import ProcessorShell
import subprocess
import re
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
           cmd_string = path + sep + path_string + '/' + cmd_split
           a = [path]
           for i in cmd_string.split('/')[2:]:
               if os.path.isfile(a[0]+'/'+i) or os.path.isdir(a[0]+'/'+i):
                   a[0]+='/'+i
               else:
                   a.append(i)
           std = subprocess.Popen(' '.join(a), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
           stdout = std.stdout.read().replace(b'\n',b'\n\r')
           if re.match(r"\/bin\/sh: 1: [\/]*.*:.*Permission denied",stdout.decode('utf-8')):
               stdout = 'Command '+' '.join(a)+' not found'
               stdout = stdout.replace(path,'').encode('utf-8')
           sh.print_string(stdout)
   sh.hello_text()




