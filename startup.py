#!/usr/bin/python
import os
import time
import serial

ser = serial.Serial( '/dev/ttyUSB0', 115200, timeout=0 )
a=[]
def hello_text():
    ser.write(b'\n\r')
    ser.write(b'python_test>')

cursor = 0
count_string_max = 0
flag = 0
while True:
    s = ser.read()
    if s:

        if s == b'\r':
            hello_text()
            cursor = 0
            count_string_max = 0
            #string = ''.join([i.decode("utf-8")  for i in a])
            print(a)
            del a[:]
        elif s == b'\x1b':
            flag = 1
        elif flag == 1 and s == b'[':
            flag += 1
        elif flag == 2 and s == b'D':
            flag = 0
            cursor-=1
            if cursor < 0:
                cursor = 0
                continue
            ser.write(b'\x1b'+b'['+b'D')
        elif flag == 2 and s == b'C':
            flag = 0
            cursor+=1
            if cursor > count_string_max:
                cursor = count_string_max
                continue
            ser.write(b'\x1b'+b'['+b'C')
        elif s == b'\x08':
            cursor-=1
            if cursor < 0:
                cursor = 0
                continue
            ser.write(b'\x1b' + b'[' + b'D')
            ser.write(b'\x1b' + b'[' + b'P')
            del a[-1]
        elif flag == 2 and s == b'3':
            flag = 3
        elif flag == 3 and s == b'~':
            flag = 0
            count_string_max-=1
            if count_string_max < 0:
                count_string_max = 0
                continue
            ser.write(b'\x1b' + b'[' + b'P')
            del a[cursor]
        elif flag == 0:
           a.append(s)
           ser.write(s)
           cursor +=1
           count_string_max += 1
