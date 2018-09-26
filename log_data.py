#" ---------- Developed by Elpis as part of Master Thesis project elpidoforos@gmail.com ------------------------"
import re
import os
import random
import hashlib
import can
from can import Message
from time import sleep
import subprocess

#Try to receiver  CAN Frames and keep then in file
#If no can frames for 5 mins then run the default file against all the possible data packets (8 bytes)

#Can interface setup for send and receive
#can_int = 'can0'
#bus = can.interface.Bus(can_int,bustype='socketcan')

def main():
    welcome_screen()
    (bus,can_int_name) = can_int_check()
    menu_call(bus,can_int_name)

def welcome_screen():
    print ("\n")
    print ("--------------------------------------------------------------")
    print ("------------  Welcome to the RPiCanBusFuzzer  ----------------")
    print ("if you have any questions please contact elpidoforos@gmail.com")
    print ("------------------------------------------------------------\n")

#Check the CAN Bus interface
def can_int_check():
    can_int_name = raw_input("Enter the CAN Bus Interface name: ")
    #Return 1 upon error, and 0 upon succes
    output_canName = subprocess.call(["ifconfig",can_int_name], stdout=open(os.devnull, 'wb'))
    #Check if the interface name exists
    if output_canName == 1:
        print("Wrong interface name, please check the CAN Bus interface name from ifconfig.\n")
        can_int_check()

    elif output_canName == 0:
        #Check if the interface is up
        bashCommandCanInf = "ip a show " + can_int_name
        process = subprocess.Popen(bashCommandCanInf.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if "DOWN" in output:
            print("The CAN Bus interface is DOWN, please activate it and start the RPiCanBusFuzzer again...")
            exit()
        else:
            bus = can.interface.Bus(can_int_name, bustype='socketcan')
    else:
        print ("Something went wrong please restart the application....")
        exit()
    return bus,can_int_name

def menu_call(bus,can_int_name):
    while(1):
        print ("""
        1.Capture CAN Bus traffic
        2.Capture CAN Bus traffic and extract the Frame IDs
        3.Capture Traffic and Replay on the CAN Bus with random CAN data
        4.Replay Traffic from captured/random ID list (send random data)
        5.Persistent attack with random captured data (Press any key)
        6.Restart the CAN Bus Interface
        7.Exit/Quit
        """)
        menu = raw_input("Select one of the actions above:")
        if menu == "1":
            filename = data_filename()
            packet_count = int(packet_log_count())
            can_receive_adv(filename, packet_count, menu, bus,can_int_name)
        elif menu == "2":
            filename = data_filename()
            packet_count = int(packet_log_count())
            can_receive_adv(filename, packet_count, menu, bus,can_int_name)
        elif menu == "3":
            filename = data_filename()
            packet_count = int(packet_log_count())
            unique_ids = can_receive_adv(filename, packet_count, menu, bus,can_int_name)
            can_send(unique_ids, bus)
        elif menu == "4":
            filename = data_filename()
            unique_ids = extract_can_frame_ids(filename)
            can_send(unique_ids, bus)
        elif menu == "5":
            filename = data_filename()
            unique_ids = extract_can_frame_ids(filename)
            try:
                while True:
                    can_send(unique_ids, bus)
            except KeyboardInterrupt:
                pass  # do cleanup here
        elif menu == "6":
            restart_can_interface(can_int_name)
        elif menu == "7":
            print("\n Goodbye....")
            exit()
        elif menu != "":
            print("\n Not Valid Choice Try again....")

def can_receive_adv(filename, packet_count, menu, bus, can_int_name):
    count = 0
    err_msg_recv = 0
    print "Receiving CAN Frame please wait.........."
    while(1):
        message = bus.recv(timeout=2)
        #print "The received message is: " + str(message)
        if message is None:
            print ("Timeout, no message on the bus...")
            err_msg_recv += 1
            if err_msg_recv > 3:
                print ('Timeout occured, please check your connection and try again...')
                #In case of timeout for the menu 2 need to know if there is a need to generate random Arbitration IDs
                if menu == "2":
                    gen_random_id_menu(filename)
                    extract_can_frame_ids(filename)
                    menu_call(bus, can_int_name)
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
                       print "Packets have been captured and saved in the filename: " + filename
                       if menu == "2":
                           extract_can_frame_ids(filename)
                           menu_call(bus, can_int_name)
                       elif menu == "3":
                           unique_ids = extract_can_frame_ids(filename)
                           sleep(3)
                           return unique_ids
                       else:
                        menu_call(bus, can_int_name)

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
    subprocess.call(["sudo /sbin/ip link set ", can_int_name, " down"], stdout=open(os.devnull, 'wb'))
    sleep(3)
    subprocess.call(["sudo /sbin/ip link set ", can_int_name, " up type can bitrate 125000"], stdout=open(os.devnull, 'wb'))
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

if __name__ == "__main__":
    main()
