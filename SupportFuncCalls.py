import os
import subprocess
import can
from can import Message


class SupportFuncCalls:

    def inf_validator(self,inf_name):
        self.inf_name_chk = subprocess.call(["ifconfig",inf_name], stdout=open(os.devnull, 'wb'))
        #Check if the interface name exists
        if self.inf_name_chk == 1:
            return self.inf_name_chk
            #print("Wrong interface name, please check the CAN Bus interface name from ifconfig.\n")
        elif self.inf_name_chk == 0:
            #Check if the interface is up
            bash_cmd_inf = "ip a show " + inf_name
            process = subprocess.Popen(bash_cmd_inf.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            bus = can.interface.Bus(inf_name, bustype='socketcan')
            if "DOWN" in output:
                print("The CAN Bus interface is DOWN, please activate it and start the RPiCanBusFuzzer again...")
                exit()
            else:
                bus = can.interface.Bus(inf_name, bustype='socketcan')
                return bus

        else:
            print ("Something went wrong please restart the application....")
            exit()  

    #Packet count validator
    def packet_counter(self):
        self.packet_count = input("How many packets you would like to capture? (0-1000):")
        try:
            int(self.packet_count)
        except ValueError:
            print("\nThe number of the packets shall be an integer value! (0-1000)")
            self.packet_counter()
        else:
            if int(self.packet_count) > 1000 or int(self.packet_count) < 0:
                print("\nPacket range not valid! Acceptable range: 0-1000)")
        return(self.packet_count)

    #Generate random arbitration IDs in the menu selection 2
    def gen_random_id_menu(self,filename):
        self.random_arbid = input("No packets, captured do you want to use random CAN IDs from a predefined list(11-bits) Y/N? : ")
        if self.random_arbid == "Y" or random_arbid == "y":
            return
        elif self.random_arbid == "N" or random_arbid == "n":
            exit()
        else:
            print ("Only Y/N are accepted.")
            gen_random_id_menu(filename)