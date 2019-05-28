import os
import subprocess
import can
from can import Message


class SupportFuncCalls:

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

'''
    def extract_can_frame_ids(filename):
        all_frame_ids = []
        filename_id = filename + ".ids.log"
        try:
            # Open the kept logfile, if not revert to a default one arbitration_ids
            with open(filename, 'r') as afile:
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

        print ("\nGenerating the " + filename_id + " with all the captured or generated ids")
        gen_id_file(filename, all_frame_ids)
        return unique_ids

    def can_send(unique_ids, bus):
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
                    print "Error on CAN Frame trasmission, please try again..."
                    count_err += 1
                    if count_err>5:
                        return
                    else:
                        continue

    def restart_can_interface(can_int_name):
        print("Restarting the CAN Bus interface.....")
        sleep(1)
        bashCommandCanInfDown = "sudo /sbin/ip link set " + can_int_name + " down"
        process = subprocess.Popen(bashCommandCanInfDown.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        sleep(2)
        bashCommandCanInfUp ="sudo /sbin/ip link set " + can_int_name + " up type can bitrate 125000"
        process = subprocess.Popen(bashCommandCanInfUp.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        sleep(2)


    #Menu in order to generate random arbitration IDs in the menu selection 2
    def gen_random_id_menu(filename):
        random_arbid = raw_input("No packets, captured do you want to use random CAN IDs from a predefined list(11-bits) Y/N? : ")
        if random_arbid == "Y" or random_arbid == "y":
            return
        elif random_arbid == "N" or random_arbid == "n":
            exit()
        else:
            print ("Only Y/N are accepted.")
            gen_random_id_menu(filename)

    def data_filename():
        filename = raw_input("Enter filename for the CAN Bus log:")
        return filename

    #Packet count validator
    def packet_log_count():
        packet_count = raw_input("How many packets you would like to capture? (0-1000):")
        try:
            int(packet_count)
        except ValueError:
            print("\nThe number of the packets shall be an integer value! (0-1000)")
            packet_log_count()
        else:
            if int(packet_count) > 1000 or int(packet_count) < 0:
                print("\nPacket range not valid! Acceptable range: 0-1000)")
        return(packet_count)

    #Generate a CAN ID log file (only contaning the random or real IDs)
    def gen_id_file(filename,ids):
        filename_id = filename + ".ids.log"
        with open(filename_id, 'w')as idfile:
            for id in ids:
                idfile.write(id + "\n")

    #Generate a random data field for the CAN frame
    def random_hex():
        return random.randint(0,255)

'''