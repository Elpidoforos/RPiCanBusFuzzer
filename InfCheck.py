import can
from can import Message
from time import sleep
import subprocess
import os


class InfCheck:

    def inf_status(self, inf_name):
        self.bus = ""
        # Return 1 upon error, and 0 upon succes
        self.inf_name_check = subprocess.call(
            ["ifconfig", self.inf_name], stdout=open(os.devnull, 'wb'))
        # Check if the interface name exists
        if self.inf_name_check == 1:
            print("ERROR: Wrong interface name, please check the CAN Bus interface name and restart the application.\n")
            exit()
        elif self.inf_name_check == 0:
            # Check if the interface is up"
            self.get_can_inf = "ip a show " + self.inf_name
            process = subprocess.Popen(
                self.get_can_inf.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            self.bus = can.interface.Bus(self.inf_name, bustype='socketcan')
            if "DOWN" in output:
                print(
                    "ERROR: The CAN Bus interface is DOWN, please activate it and restart the application.")
                exit()
            else:
                self.bus = can.interface.Bus(
                    self.inf_name, bustype='socketcan')
            return self.bus
