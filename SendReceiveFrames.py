import os
import sys
import subprocess
import can
import time
from can import Message
from SupportFuncCalls import *


class SendReceiveFrames:
    supp_func = SupportFuncCalls()

    # Receive CAN traffic and save it to file
    def can_rcv(self, file_name, bus_obj):
        (count, err_msg_recv, packet_count) = (0, 0, 1000)
        print("Receiving CAN Frames please wait............")
        while(1):
            message = bus_obj.recv(timeout=2)
            # print "The received message is: " + str(message)
            if message is None:
                print("ERROR: No traffic on the bus.")
                err_msg_recv += 1
                if err_msg_recv > 3:
                    print(
                        'ERROR: Connection timeout occured, please check your connection and try again.')
                    sys.exit()
            else:
                for message in bus_obj:
                    with open(file_name, 'a') as afile:
                        afile.write(str(message) + '\n')
                        count += 1
                        if count > packet_count:
                            print(
                                str(packet_count) + " CAN Frames have been captured and saved in the: " + file_name)
                            return

    # Replay CAN traffic from an existing log file
    def can_replay(self, file_name, bus_obj):
        frame_ids = self.supp_func.extract_can_frame_ids(file_name)
        self.can_send(frame_ids, bus_obj)

    # Generate random CAN Frame IDs and replay
    def can_replay_random(self, file_name, bus_obj):
        try:
            frame_ids = self.supp_func.gen_random_ids(file_name)
        except:
            print("ERROR: Cannot load the CAN log file.")
        self.can_send(frame_ids, bus_obj)

    def can_send(self, frame_ids, bus_obj):
        print("Sending CAN Frames...")
        (cnt_send, cnt_err) = (0, 0)
        while(1):
            for id in frame_ids:
                data_format = [self.supp_func.random_hex(), self.supp_func.random_hex(), self.supp_func.random_hex(), self.supp_func.random_hex(
                ), self.supp_func.random_hex(), self.supp_func.random_hex(), self.supp_func.random_hex(), self.supp_func.random_hex()]
                arbitration_id_format = int(id, 16)
                msg = can.Message(
                    extended_id=False, arbitration_id=arbitration_id_format, data=data_format)
                try:
                    bus_obj.send(msg)
                    time.sleep(0.2)
                except:
                    print("ERROR: CAN Frame trasmission timeout, please try again...")
                    cnt_err += 1
                    if cnt_err > 5:
                        sys.exit()
