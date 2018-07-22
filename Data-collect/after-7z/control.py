#!/usr/bin/env python3 
import logging, time, re, json
from mySerial import AT

logger=logging.getLogger(__name__)

class Control(object) :
    sleep_second=3
    baud=115200
    def __init__(self, eui, serial='/dev/ttyXRUSB0') :
        self.logger=logging.getLogger(__name__)
        self.eui=eui
        self.serial=serial

    def start(self) :
        self.init_node()
        self.join()

    def init_node(self) :
        self.at=AT(self.serial, self.baud)
        
    def join(self):
        self.at.test()

        self.logger.info('Node set ack enable')
        self.logger.debug(self.at.say('AT+ACK=1'))
        
        self.logger.info('Node public network join...')
        self.logger.debug(self.at.say('AT+PN=1'))

        self.logger.info('Node set application EUI...')
        self.logger.debug(self.at.say('AT+NI=0,86e4efc7104f6829'))

        self.logger.info('Node set application key...')
        self.logger.debug(self.at.say('AT+NK=0,a346b6faef2bd33c16fe9b1d8d47a11d'))

        self.logger.info('Node set frequency subband...')
        self.logger.debug(self.at.say('AT+FSB=1'))

        joinResult = self.at.join()
        
        self.logger.info('Join Result : {}'.format(joinResult))

        if(joinResult is not True):
            raise JoinFailedError(self.eui, self.serial)

    def setPower(self, power) :
        self.logger.debug(self.at.say('AT+TXP={}'.format(power)))

    def setSF(self, sf) :
        self.logger.debug(self.at.say('AT+TXDR={}'.format(sf)))

    def test(self) :
        self.logger.debug(self.at.say('AT+SEND=123'))
        rssi=self.at.say('AT+RSSI')
        snr=self.at.say('AT+SNR')
        self.logger.debug('rssi: {}, snr: {}'.format(rssi, snr))
        return re.split(',', rssi[1]), re.split(',', snr[1])

class JoinFailedError(Exception):
    failMsg = "Join Failed. Please try to join again."

    def __init__(self, devEUI, serial):
        self.devEUI = devEUI
        self.serial = serial

    def __str__(self):
        return self.failMsg
    

def save(location_name, power, sf, count, data) :
    filename='data/{}_{}_{}_{}.txt'.format(location_name, power, sf, count)
    with open(filename, 'w') as f :
        json.dump(data, f)
    logger.info('write JSON into : {}'.format(filename))
    logger.debug(data)

