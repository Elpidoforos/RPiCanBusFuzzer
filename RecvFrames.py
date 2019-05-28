import can
import random
import hashlib
from can import Message
from time import sleep
import subprocess
from InfCheck import *
from SupportFuncCalls import *

class RecvFrames:
    def can_receive_adv(self, filename, packet_count, menu, bus, inf_name):
    self.count = 0
    self.err_msg_recv = 0
    print ("Receiving CAN Frame please wait..........")
    while(1):
        self.message = bus.recv(timeout=2)
        #print "The received message is: " + str(message)
        if self.message is None:
            print ("Timeout, no message on the bus...")
            self.err_msg_recv += 1
            if self.err_msg_recv > 3:
                print ('Timeout occured, please check your connection and try again...')
                #In case of timeout for the menu 2 need to know if there is a need to generate random Arbitration IDs
                if self.menu == "2":
                    gen_random_id_menu(filename)
                    extract_can_frame_ids(filename)
                    menu_call(bus, inf_name)

                if menu == "3":
                    gen_random_id_menu(filename)
                    unique_ids = extract_can_frame_ids(filename)
                    sleep(3)
                    return unique_ids
                else:
                    exit()
        else:
            for message in bus:
                with open(filename, 'a') as afile:
                    afile.write(str(message) + '\n')
                    count += 1
                    if count > packet_count:
                       print ("Packets have been captured and saved in the filename: " + filename)
                       if menu == "2":
                           extract_can_frame_ids(filename)
                           menu_call(bus, inf_name)

                       elif menu == "3":
                           unique_ids = extract_can_frame_ids(filename)
                           sleep(3)
                           return unique_ids
                       else:
                        menu_call(bus, inf_name)