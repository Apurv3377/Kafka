#!/usr/bin/python
import datetime
import string
import random
import os
import uuid
import time
import sys
from datetime import timezone, datetime
from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    
    
messages_number =  20000000000
j=0
itr=0
MAX_ITR=int(sys.argv[1])
total_docs=0
pid=os.getpid()

#random data generation
def random_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))

def random_hexgenerator():
    hexN="0x"+uuid.uuid4().hex
    return hexN[:18]
def timestamp_gen():
    ts=int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return ts

f = open('/home/apurv/Readings_pers_%s.csv' % pid, 'w+')


startf = datetime.now();
while itr<MAX_ITR: 
    start = datetime.now();
    for index in range(messages_number):
        try:
            ts = timestamp_gen()
            value = random.random()
            syscall_nr=random.randint(1,101)
            syscall_name=random_generator(6,"abcdefghijklmnopqrstuvwxyz")
            dtb=random_hexgenerator()
            rsp=random_hexgenerator()
            rip=random_hexgenerator()
            pid=random.randint(1,10000)
            vmid="vm"+random_generator(2,'1234')
            logtype=random_generator(3,'xyz')
            document = {
                'value' : value,
                'syscall_nr':syscall_nr,
                'syscall_name':syscall_name,
                'dtb':dtb,
                'rsp':rsp,
                'rip':rip,
                'pid':pid,
                'vmid':vmid,
                'logtype':logtype,
                'ts':ts 
                }
          
            producer.send('FirstTest',value=document)
            index += 1;
            
            #calculate the time for the insert
            timec=int((datetime.now() - start).total_seconds())

            if timec==1:
                j=j+1
                f.write("%d,%d\n" %(j, index))
                itr=itr+1
                total_docs=total_docs + index
                break
                   
        except:
            print ('Unexpected error:', sys.exc_info()[0], ', for index ', index)
            raise

print (' inserted ',total_docs, ' in ', (datetime.now() - startf).total_seconds(), 's')
f.close()
