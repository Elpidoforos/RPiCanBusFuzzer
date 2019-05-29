# RPiCanBus
This repository will keep the scripts which are developed for the purspose of the a MSc thesis in Information Security programe in Luleå University of Technology. The developement board is a RarpberryPi with a PICAN2 module. 

In CanBusFuzzer.py the arguments which can be used are:
        -i   : Can intereface
        -s   : Capture and save traffic
        -r   : Replay traffic from log file
        -sr  : Save and Replay traffic
        -rid : Replay traffic with random CAN IDs
        
Use: CanBusFuzzer.py -i canX -s test_file

A log in the logfile.txt shall look like the snipset below:
Timestamp: 1525196535.167178        ID: 0123    S          DLC: 8    ff ff ff ff ff ff ff ff

*Timestamp : When the frame has been caught
*ID: The frame ID of the packet
*DLC: The size of the data frame
*The last field ff ff ff ff...  are the data of the frame.
