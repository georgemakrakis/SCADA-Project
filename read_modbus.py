# from pymodbus.client.sync import ModbusTcpClient

# client = ModbusTcpClient('localhost',port=5020)
# client.write_coil(1, True)
# result = client.read_coils(1,1)
# print(result.bits[0])
# client.close()


import socket

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5020))

# Returns a message or Application Data Unit (ADU) specific for doing
# Modbus TCP/IP.
# message = tcp.write_multiple_registers(slave_id=1, starting_address=1, values=[1, 0, 1, 1])

# Response depends on Modbus function code. This particular returns the
# amount of coils written, in this case it is.
# response = tcp.send_message(message, sock)

for i in range(2):
    message = tcp.read_holding_registers(slave_id=1, starting_address=i, quantity=1)

    response = tcp.send_message(message, sock)

    print(str(response))

sock.close()