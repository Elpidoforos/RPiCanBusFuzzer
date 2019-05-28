import os
import subprocess
import can
from can import Message
import random

class SupportFuncCalls:

    # Extract the IDs from a CAN Bus log file
    def extract_can_frame_ids(self, file_name):
        all_frame_ids = []
        filename_id = file_name + ".ids.log"
        try:
            # Open the kept logfile, if not revert to a default one arbitration_ids
            with open(file_name, 'r') as afile:
                logs = afile.readlines()
                for line_log in logs:
                    id = re.search(r"(ID: )([0-9a-fA-F]+)", line_log)
                    # Regular expression to extract the data field. README has more info on how the data look like
                    data = re.search(r"([0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+)",
                                     line_log)
                    all_frame_ids.append(id.group(2).lstrip('0'))
        except:
            print("ERROR: Cannot load the CAN log file.")

        # Keep all the unique frame ids only
        unique_ids = list(set(all_frame_ids))

        print("\nGenerating " + file_name +
              " with the captured CAN Frame ids")
        self.gen_id_file(file_name, all_frame_ids)
        return unique_ids

    #Generate Random Frame ID file
    def gen_random_ids(self, file_name):
        all_frame_ids = []
        # If there were no valid frame ids because of no frames then create a random one and send it on the bus
        with open('arbitration_ids', 'r') as afile:
            logs = afile.readlines()
            #TODO: Give the number with how many random ids! 
            for i in range(0, 50):
                all_frame_ids.append(random.choice(logs).rstrip())
        # Keep all the unique frame ids only
        unique_ids = list(set(all_frame_ids))

        print("\nGenerating " + file_name +
              " with all the random CAN Frame ids")
        self.gen_id_file(file_name, all_frame_ids)
        return unique_ids

    # Generate a CAN ID log file (only contaning the random or real IDs)
    def gen_id_file(self, file_name, ids):
        filename_id = file_name + ".ids.log"
        with open(filename_id, 'w')as idfile:
            for id in ids:
                idfile.write(id + "\n")

    # Generate a random data field for the CAN frame
    def random_hex(self):
        return random.randint(0, 255)
