class shell():
    def __init__(self,ser):
        self.__cursor__ = 0
        self.__count_string_max__ = 0
        self.__flag__ = 0
        self.__a__ = []
        self.ser = ser
        self.hello_string = b'ProcessorShell:'
        self.path = []
    def hello_text(self):
        self.ser.write(b'\n\r')
        self.ser.write(self.hello_string+b'/'.join(self.path)+b'>')

    def command_not_found(self,a):
        self.ser.write(b'\n\rCommand not found: ')
        [self.ser.write(i) for i in a]
    def print_string(self,string):
        self.ser.write(b'\n\r'+string)
    def treatment(self,hello=True):
        while True:
            s = self.ser.read()
            if s == b'\r':
                string = ''
                try:
                    string = ''.join([i.decode("utf-8")  for i in self.__a__])
                except:
                    self.command_not_found(self.__a__)
                if not string:
                    self.hello_text()
                self.__cursor__ = 0
                self.__count_string_max__ = 0
                del self.__a__[:]
                if string:
                    break
            elif s == b'\x1b':
                self.__flag__ = 1
            elif self.__flag__ == 1 and s == b'[':
                self.__flag__ += 1
            elif self.__flag__ == 2 and s == b'D':
                self.__flag__ = 0
                self.__cursor__-=1
                if self.__cursor__ < 0:
                    self.__cursor__ = 0
                    continue
                self.ser.write(b'\x1b'+b'['+b'D')
            elif self.__flag__ == 2 and s == b'C':
                self.__flag__ = 0
                self.__cursor__+=1
                if self.__cursor__ > self.__count_string_max__:
                    self.__cursor__ = self.__count_string_max__
                    continue
                self.ser.write(b'\x1b'+b'['+b'C')
            elif s == b'\x08':
                self.__cursor__ -=1
                if self.__cursor__  < 0:
                    self.__cursor__ = 0
                self.ser.write(b'\x1b' + b'[' + b'D')
                self.ser.write(b'\x1b' + b'[' + b'P')
                del self.__a__[-1]
            elif self.__flag__ == 2 and s == b'3':
                self.__flag__ = 3
            elif self.__flag__ == 3 and s == b'~':
                self.__flag__ = 0
                self.__count_string_max__-=1
                if self.__count_string_max__ < 0:
                    self.__count_string_max__ = 0
                    continue
                self.ser.write(b'\x1b' + b'[' + b'P')
                del self.__a__[self.__cursor__]
            elif s and self.__flag__ == 0:
               self.__a__.append(s)
               self.ser.write(s)
               self.__cursor__ +=1
               self.__count_string_max__ += 1
        return string