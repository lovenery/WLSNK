#!/usr/bin/env python3
# pip install myserial
import logging, re, time, serial

eui='008000000000e32c'

class AT(object) :
    def __init__(self, port, baudrate) :
        self.logger=logging.getLogger(__name__)
        self.ser=serial.Serial(port, baudrate, timeout=0.5)
        if not self.ser.isOpen() :
            self.ser.open()
        self.logger.info('port state : {}'.format(self.ser.isOpen()))

    def test(self, count=1) :
        for _ in range(count) :
            lines=self.say('AT')
            self.logger.debug('test : {}'.format(lines))

    def say(self, message) :
        message='{}\n'.format(message)
        if isinstance(message, str) :
            message=message.encode()
        if isinstance(message, bytes) :
            self.ser.write(message)
            lines=[]
            while True:
                line=self.ser.readline()
                if len(line)<=0 :
                    continue
                if isinstance(line, bytes) :
                    line=line.decode()
                line=line.rstrip()
                lines.append(line)
                if re.match('ERROR', line) or re.match('OK', line) :
                    return lines
            self.logger.warning('size too big')
            return
        self.logger.error('input message( {} ) type ERROR type: {}'.format(message, type(message)))

    def join(self, try_time=10) : 
        self.logger.info('Node join network')
        for _ in range(try_time) :
            njs=self.say('AT+NJS')
            self.logger.debug('Network Join State : {}'.format(njs))
            if 'Successfully joined network' in njs  or '1' in njs :
                return True
            result=self.say('AT+join')
            self.logger.debug('Join Output : {}'.format(result))
        return False

if __name__=='__main__' :
    at=AT('/dev/tty.usbmodem1423', 115200)
    at.test()
    print(at.say('AT+TXP=11'))
    print(at.say('AT+TXDR=7'))
    print(at.say('AT+ACK=0'))
    print(at.say('AT+NJS'))
    print(at.say('AT+SEND=123'))
    print(at.say('AT+RSSI'))
    print(at.say('AT+SNR'))
