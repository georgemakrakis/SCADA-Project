# from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusTlsClient

# client = ModbusTcpClient('127.0.0.1',5020)
client = ModbusTlsClient('127.0.0.1',5020)

client.connect()
# Temperature
# result = client.read_input_registers(1,2)

# Level
result = client.read_input_registers(1,3)

print(result.registers)
client.close()