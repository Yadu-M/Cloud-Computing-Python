#!/usr/bin/env python
import pika, time
from hashlib import sha256


def getDeminerID() -> int:
    prompt = 'Enter deminer id: '
    while True:
        try:
            rover_id = input(prompt)
            if ((int (rover_id) > 2) or (int (rover_id) < 1)):
                raise ValueError
            break
        except ValueError:
            prompt = 'Please deminer id: '
            pass
    return rover_id


def disarm_mine(serialNum: str) -> int:    
    pin = 0
    temp_mine_key = str(pin) + serialNum
    hashed_data = sha256(temp_mine_key.encode()).hexdigest()
    print(f' [-] Initial Hash: {hashed_data}')
    while True:
        if hashed_data[0:6] == '000000':
            print(f' [-] Completed Hash: {hashed_data}')
            return pin
        temp_mine_key = str(pin) + serialNum
        hashed_data = sha256(temp_mine_key.encode()).hexdigest()
        pin += 1


getDeminerID()

# Establishing connection with rabbit MQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
demineChannel = connection.channel()
demineChannel.queue_declare(queue='Demine-Queue', durable=True)
print(' [*] Waiting for mine defusal requests')


def callback(ch, method, properties, body: bytearray):
    mine_info = body.decode()
    print(f" [X] Received {mine_info}")
    row = mine_info.split()[0]
    col = mine_info.split()[1]
    pin = disarm_mine(mine_info.split()[2])
    print(f" [-] Finished disarming mine. Pin: {pin}")    
    ch.basic_ack(delivery_tag=method.delivery_tag)    
    
            
    # Sending confirmation to server
    defusedMineChannel = connection.channel()
    defusedMineChannel.queue_declare(queue='Defused-Mines', durable=True)
    defusedMineChannel.basic_publish(exchange='',
                          routing_key='Defused-Mines',
                          body=f'Mine defused at ({row}, {col}) with Pin: {pin}')
    
    defusedMineChannel.close()    


demineChannel.basic_qos(prefetch_count=1)
demineChannel.basic_consume(queue='Demine-Queue', on_message_callback=callback)

demineChannel.confirm_delivery
demineChannel.start_consuming()