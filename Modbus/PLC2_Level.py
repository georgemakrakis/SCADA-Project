from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import os, sys

from twisted.internet.task import LoopingCall

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
    context = a[0]
    register = 3
    slave_id = 0x01
    address = 0x01
    values = context[slave_id].getValues(register, address, count=2)
    values = flow_level.read_levels()

    # If the values entered by use exceed we maintain the lowest possible
    if(int(values[0]) > 100):
        values[0] = 100
    if(int(values[1]) < 20):
        values[1] = 20

    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)

def run_server():

    # Discrete Inputs, Coil Outputs, Input Registers, Output Registers
    # By default it maps 0-7 to 1-8. The use of zero_mode=True maps 0-7 to 0-7
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100)) 
    
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    time = 3  # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False) # initially delay by time
    StartTcpServer(context, identity=identity, address=("localhost", 5021))

if __name__ == "__main__":
    run_server()
    