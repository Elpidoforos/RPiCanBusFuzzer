" ---------- Developed by Elpis as part of Master Thesis project elpidoforos@gmail.com ------------------------"
import re
import hashlib
import data as data
#import can

#Try to receiver  CAN Frames and keep then in file
#If no can frames for 5 mins then run the default file against all the possible data packets (8 bytes)

def main():
    unique_ids = extract_can_frame_ids()
    can_send(unique_ids)

def extract_can_frame_ids():
    try:
        # Open the kept logfile, if not revert to a default one
        with open('logfile.txt', 'r') as afile:
            logs = afile.readlines()
            all_frame_ids = []
            for line_log in logs:
                id = re.search(r"(ID: )([0-9a-fA-F]+)", line_log)
                data = re.search(r"([0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+)",
                                 line_log)
                all_frame_ids.append(id.group(2).lstrip('0'))
    except:
        with open('logfile1.txt', 'r') as afile:
            logs = afile.readlines()
            for line_log in logs:
                print line_log
    # Keep all the unique frame ids only
    unique_ids = list(set(all_frame_ids))
    return unique_ids

def can_send(unique_ids):
    (byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7) = (1, 2, 3, 4, 5, 6, 7, 8)
    data_format = [byte0, byte1, byte2, byte3, byte4, byte5, byte6, byte7]
    for id in unique_ids:
        arbitration_id_format = '0x' + id
	msg = can.Message(arbitration_id=arbitration_id_format data=data_format)

#def can_receive:


if __name__ == "__main__":
    # execute only if run as a script
    main()
