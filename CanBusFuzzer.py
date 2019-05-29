import sys
from SupportFuncCalls import *
from CanSendReceive import *
from can import Message
from InfCheck import *
import argparse


def main():
    # Parse the arguments
    args = parse_arguments()
    welcome_screen()
    # Instanciate the Support Functions Class
    supp_func = SupportFuncCalls()
    inf_chk = InfCheck()
    can_send_receive = CanSendReceive()

    # Get interface name
    inf_name = args.inf

    # Check that the CAN Interface it is up
    bus_obj = inf_chk.inf_status(inf_name)

    # Save Replay of Save and Replay option
    if args.save:
        print("Save Menu")
        file_name = args.save
        can_send_receive.can_rcv(file_name, bus_obj)
    elif args.replay:
        print("Replay Menu")
        file_name = args.replay
        can_send_receive.can_replay(file_name, bus_obj)
    elif args.save_replay:
        print("Save Replay")
        file_name = args.save_replay
        can_send_receive.can_rcv(file_name, bus_obj)
        can_send_receive.can_replay(file_name, bus_obj)
    elif args.rand_id:
        print("Random ID reply")
	file_name = args.rand_id
        can_send_receive.can_replay_random(file_name, bus_obj)


def parse_arguments():
    parser = argparse.ArgumentParser()
    # Adding Arguments
    parser.add_argument("--inf_name", "-i", dest="inf",
                        help="Add the needed CAN Bus Interface", type=str, required=True)
    # Only one of the arguments below shall be accepted
    save_or_replay = parser.add_mutually_exclusive_group()
    save_or_replay.add_argument("--save_log", "-s", dest="save",
                                help="Capture CAN traffic and save it in a log file", type=str, required=False)
    save_or_replay.add_argument("--replay_log", "-r", dest="replay",
                                help="Replay CAN traffic from a log file", type=str, required=False)
    save_or_replay.add_argument("--save_replay_log", "-sr", dest="save_replay",
                                help="Capture CAN traffic and replay on the bus", type=str, required=False)
    save_or_replay.add_argument("--random_id", "-rid", dest="rand_id",
                                help="Generate random CAN Frame ids and replay on the bus", type=str, required=False)                            
    return parser.parse_args()

# Welcome screen during the script initialization
def welcome_screen():
    print("\n" + "---------------------------------------------------------------"
          + "\n" + "-------------  Welcome to the RPiCanBusFuzzer  ----------------"
          + "\n" + "if you have any questions please contact elpidoforos@gmail.com"
          + "\n" + "---------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
