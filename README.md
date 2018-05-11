# RPiCanBus
This SW is developed for the purspose of my Thesis. The developement board which the thesis is based upon is a RPi with a PICAN2 module. 

A log in the logfile.txt shall look like the snipset below:
Timestamp: 1525196535.167178        ID: 0123    S          DLC: 8    ff ff ff ff ff ff ff ff

*Timestamp : When the frame has been caught
*ID: The frame ID of the packet
*DLC: The size of the data frame
*The last field ff ff ff ff...  are the data of the frame.
