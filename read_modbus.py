from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('localhost',port=5020)
client.write_coil(1, True)
result = client.read_coils(1,1)
print(result.bits[0])
client.close()