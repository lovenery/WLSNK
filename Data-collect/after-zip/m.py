#!/user/bin/env python3
import os
from api import *
from control import *

logger=logging.getLogger()
logging.basicConfig(level=logging.INFO)

def getMaxCount(dirname, location, power, sf) :
    all_filenames=os.listdir(dirname)
    if len(all_filenames)==0 :
        return 0
    match_filenames=[ re.match('{}_{}_{}_\d+'.format(location, power, sf), filename).group()
                     for filename in all_filenames ]
    if len(match_filenames)==0 :
        return 0
    numbers=[ int(re.split('_', filename)[3])
             for filename in match_filenames ]
    return max(numbers)

def save(dirname, location, power, sf, count, data) :
    with open('{}/{}_{}_{}_{}.json'.format(dirname, location, power, sf, count), 'w') as f :
        json.dump(data, f)
    
if __name__ == '__main__' :
    jwt=getToken()
    location='test'
    devEUI='008000000000c095' #'008000000000e331'
    devSerial='/dev/tty.usbmodem1423' #'com3'
    dirname='./testData'
    power=20    # 1 ~ 20
    sf=7        # 7 ~ 10

    con=Control(devEUI, devSerial)
    con.start()
    con.setPower(power)
    con.setSF(10-sf)
    count=getMaxCount(dirname, location , power, sf)+1
    while True :
        nodeRssi, nodeSnr=con.test()
        logger.debug('test(rssi={}, snr={})'.format(nodeRssi[0], nodeSnr[0]))
        data=getFrame(devEUI, jwt)
        tx, txTime, txPhy=data[0]['txInfo'], data[0]['createdAt'], data[0]['phyPayloadJSON']
        rx, rxTime, rxPhy=data[1]['rxInfoSet'], data[1]['createdAt'], data[1]['phyPayloadJSON']
        if tx and rx and len(rx)>0 :
            logger.debug('rx  : {}'.format(rx))
            logger.debug('time: {}'.format(rxTime))
            logger.debug('phy : {}'.format(rxPhy))
            logger.debug('tx  : {}'.format(tx))
            logger.debug('time: {}'.format(txTime))
            logger.debug('phy : {}'.format(txPhy))
            for r in rx :
                print('{} up   link:(rssi, snr)=({}, {})'.format(r['mac'], r['rssi'], r['loRaSNR']))
            print('{} down link:(rssi, snr)=({}, {})'.format(tx['mac'], nodeRssi[0], nodeSnr[0]))
            save(dirname, location, power, sf, count,
                 { 'rx' : rx, 'rxTime' : rxTime, 'rxPhy' : rxPhy,
                   'tx' : tx, 'txTime' : txTime, 'txPhy' : txPhy,
                   'nodeRssi' : nodeRssi, 'nodeSnr': nodeSnr } )
            count+=1
		
