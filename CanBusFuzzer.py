import sys
from SupportFuncCalls import *
from can import Message
from InfCheck import *
import argparse
from CanSendReceive import *

def main():
    #Parse the arguments
    args = parse_arguments()
    welcome_screen()
    #Instanciate the Support Functions Class
    supp_func = SupportFuncCalls()
    inf_chk = InfCheck()
    can_send_receive = CanSendReceive()

    #Get interface name
    inf_name = args.inf

    #Check that the CAN Interface it is up
    bus_obj = inf_chk.inf_status(inf_name)

    #Save Replay of Save and Replay option
    if args.save:
        print("Save Menu")
        file_name = args.save
        can_send_receive.can_rcv(file_name,bus_obj)
    elif args.replay:
        print("Replay")
        file_name = args.replay
    elif args.save_replay:
        print("Save Replay")
        file_name = args.save_replay

def parse_arguments():
    parser = argparse.ArgumentParser()
    #Adding Arguments
    parser.add_argument("--inf_name","-i",dest="inf", help="Add the needed CAN Bus Interface", type=str, required=True)
    #Only one of the arguments shall be accepted
    save_or_replay = parser.add_mutually_exclusive_group()
    save_or_replay.add_argument("--save_log","-s",dest="save", help="Capture the traffic and save it in a file", type=str, required=False)
    save_or_replay.add_argument("--replay_log","-r", dest="replay",help="Replay the traffic from a file", type=str, required=False)
    save_or_replay.add_argument("--save_replay_log","-sr", dest="save_replay",help="Capture the traffic and replay it with random data", type=str, required=False)
    return parser.parse_args()


#Welcome screen during the script initialization
def welcome_screen():
    print ("\n" + "---------------------------------------------------------------" 
        + "\n" + "-------------  Welcome to the RPiCanBusFuzzer  ----------------" 
        + "\n" + "if you have any questions please contact elpidoforos@gmail.com" 
        + "\n" + "---------------------------------------------------------------\n")

if __name__ == "__main__":
    main()


'''
        1.Capture CAN Bus traffic
        2.Capture CAN Bus traffic and extract the Frame IDs
        3.Capture Traffic and Replay on the CAN Bus with random CAN data
        4.Replay Traffic from captured or random ID list (if ID list exist replay, otherwise generate IDs and replay)
        5.Persistent attack with random data (if ID list exist replay, otherwise generate IDs and replay)
        6.Restart the CAN Bus Interface
'''