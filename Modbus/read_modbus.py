from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1',5020)

client.connect()

result = client.read_holding_registers(1,2)
print(result.registers)
client.close()