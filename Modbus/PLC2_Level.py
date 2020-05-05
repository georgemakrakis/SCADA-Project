from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.sync import StartTlsServer, ModbusTlsServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusTlsFramer

import os, sys
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import threading

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import flow_level

def updating_writer(a):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")
    # context = a[0]
    # register = 4
    # slave_id = 0x01
    # address = 0x01
    # values = context[slave_id].getValues(register, address, count=2)

    register = 4
    slave_id = 0x01
    address = 0x01
    contxt = a.context[slave_id]
    values = contxt.getValues(register, address, count=2)
    values = flow_level.read_levels()
    values = list(map(int, values)) 

    # TODO If out of bounds even occur, log the event
    # if(int(values[0]) > 100 or int(values[1]) < 20):
    #     values = contxt.getValues(register, address, count=3)
    #     values[2] += 1
    #     contxt.setValues(register, 0x03, values)


    # If the values entered by the user are out of bounds, we maintain the lowest possible
    if(int(values[0]) > 100  or int(values[0]) < 20):
        values[0] = 100
    if(int(values[1]) < 20 or int(values[1]) > 100):
        values[1] = 20

    log.debug("new values: " + str(values))
    contxt.setValues(register, address, values)

def run_server():

    # Discrete Inputs, Coil Outputs, Input Registers, Output Registers
    # By default it maps 0-7 to 1-8. The use of zero_mode=True maps 0-7 to 0-7
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100)) 
    
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    time = 5  # 5 seconds delay
    # loop = LoopingCall(f=updating_writer, a=(context,))
    # loop.start(time, now=False) # initially delay by time
    # StartTcpServer(context, identity=identity, address=("localhost", 5021))

    server = ModbusTcpServer(context, identity=identity,
                             address=("0.0.0.0", 5020))
    # server = ModbusTlsServer(context, framer=ModbusTlsFramer, identity=identity, certfile="Modbus/PLC2.crt",
    #              keyfile="Modbus/PLC2.key", address=("0.0.0.0", 5020))


    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    loop = LoopingCall(f=updating_writer, a=server)
    loop.start(time, now=True)
    reactor.run()

if __name__ == "__main__":
    run_server()
    