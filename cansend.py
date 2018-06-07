import can
from can import Message
from time import sleep

can_int = 'can0'
bus = can.interface.Bus(can_int,bustype='socketcan')

print "Sending CAN Frames..."
arbitration_id_format = 150
data_format=[00,11,22,33,44,55,66,77]
msg = can.Message(extended_id=False, arbitration_id=arbitration_id_format, data=data_format)
# print msg
bus.send(msg)
