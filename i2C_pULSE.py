from microbit import *
import ustruct

MAX30100_I2C_ADDRESS = 0x57

BEATDETECTOR_INIT_HOLDOFF               = 2000  
BEATDETECTOR_MASKING_HOLDOFF            = 200     
BEATDETECTOR_BPFILTER_ALPHA             = 0.6    
BEATDETECTOR_MIN_THRESHOLD              = 20     
BEATDETECTOR_MAX_THRESHOLD              = 800    
BEATDETECTOR_STEP_RESILIENCY            = 30     
BEATDETECTOR_THRESHOLD_FALLOFF_TARGET   = 0.3     
BEATDETECTOR_THRESHOLD_DECAY_FACTOR     = 0.99   
BEATDETECTOR_INVALID_READOUT_DELAY      = 2000    
BEATDETECTOR_SAMPLES_PERIOD             = 10      

#Functions
def writeRegister(address, data):
    i2c.write(MAX30100_I2C_ADDRESS,bytearray([address, data]))
    
def readRegister(address):
    i2c.write(MAX30100_I2C_ADDRESS,bytearray([address]))
    tempByte = i2c.read(MAX30100_I2C_ADDRESS,1)
    tempByte1 = ustruct.unpack('<H', tempByte)[0]
    return tempByte1
    
def setMode(mode):
    writeRegister(0x06, mode)
    
def setLedsPulseWidth(ledPulseWidth):
    previous = readRegister(0x07)
    writeRegister(0x07, (previous & 0xFC) | ledPulseWidth)

def setSamplingRate(samplingRate):
    previous = readRegister(0x07)
    writeRegister(0x07, (previous & 0xE3) | (samplingRate << 2))

def setLedsCurrent(irLedCurrent,redLedCurrent):
    writeRegister(0x09, (redLedCurrent << 4 | irLedCurrent))

def setHighresModeEnabled(enabled):
    previous = readRegister(0x07)
    if (enabled == 1):
       writeRegister(0x07, previous | (1 << 6))
    else:
       writeRegister(0x07, previous & ~(1 << 6))

def update():
    global rawIRValue
    global rawRedValue
    i2c.write(MAX30100_I2C_ADDRESS,bytearray([0x05]))
    buffer0 = i2c.read(MAX30100_I2C_ADDRESS,1)
    buffer1 = i2c.read(MAX30100_I2C_ADDRESS,1)
    buffer2 = i2c.read(MAX30100_I2C_ADDRESS,1)
    buffer3 = i2c.read(MAX30100_I2C_ADDRESS,1)
    rawIRValue = (buffer0 << 8) | buffer1
    rawRedValue = (buffer2 << 8) | buffer3

# REAL Code
setMode(0x02)
setLedsPulseWidth(0x03)
setSamplingRate(0x01)
setLedsCurrent(0x0F, 0x0F)
setHighresModeEnabled(1)
