" ---------- Developed by Elpis as part of Master Thesis project elpidoforos@gmail.com ------------------------"
import re
import random
import hashlib
import can
from can import Message
from time import sleep

#Try to receiver  CAN Frames and keep then in file
#If no can frames for 5 mins then run the default file against all the possible data packets (8 bytes)

#Can interface setup for send and receive
can_int = 'can0'
bus = can.interface.Bus(can_int,bustype='socketcan')

def main():
    can_receive()
    sleep(5)
    unique_ids = extract_can_frame_ids()
    sleep(5)
    can_send(unique_ids)
    #print testing

def can_receive():
    count = 0
    no_message_count = 0
    print "Receiving CAN Frames...."
    while(1):
        message = bus.recv(timeout=2)
        print ('Timeout, no message')
        #print message
        if message is None:
            no_message_count += 1
            if no_message_count > 20:
                return
            continue
        else:
            for message in bus:
                with open('logfile.txt', 'a') as  afile:
                    afile.write(str(message) + '\n')
                    count += 1
                    continue
                    #print count
                if count > 20:
                        return
def extract_can_frame_ids():
    all_frame_ids = []
    print "Extract CAN Frames....."
    try:
        # Open the kept logfile, if not revert to a default one arbitration_ids
        with open('logfile.txt', 'r') as afile:
            logs = afile.readlines()
            for line_log in logs:
                id = re.search(r"(ID: )([0-9a-fA-F]+)", line_log)
                #Regular expression to extract the data field. README has more info on how the data look like
                data = re.search(r"([0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+)",
                                 line_log)
                all_frame_ids.append(id.group(2).lstrip('0'))
    except:
        #If there were no valid frame ids because of no frames then create a random one and send it on the bus
        with open('arbitration_ids', 'r') as afile:
            logs = afile.readlines()
            for i in range(0,40):
                all_frame_ids.append(random.choice(logs).rstrip())
    # Keep all the unique frame ids only
    unique_ids = list(set(all_frame_ids))
    return unique_ids

def can_send(unique_ids):
    print "Sending CAN Frames..."
    count_send = 0
    count_err = 0
    while(1):
        for id in unique_ids:
            data_format = [random_hex(), random_hex(), random_hex(), random_hex(), random_hex(), random_hex(), random_hex(),random_hex()]
            arbitration_id_format =  int(id,16)
            #print arbitration_id_format
            #print data_format
            msg = can.Message(extended_id=False, arbitration_id=arbitration_id_format, data=data_format)
            #print msg
            try:
                bus.send(msg)
                count_send += 1
                sleep(0.1)
                if count_send > 40:
                    return
                else:
                    continue
            except:
                print "Error on CAN Frame trasmission"
                count_err += 1
                if count_err>20:
                    return
                else:
                    continue

#Generate a random data field for the CAN frame
def random_hex():
    return random.randint(0,255)
    #randomhex = ''.join([random.choice('0123456789ABCDEF') for x in range(2)])
    #return (hex(int(randomhex, 16) + int("0x20", 16)))

if __name__ == "__main__":
    main()