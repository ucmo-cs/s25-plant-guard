import bme680
from datetime import datetime, timezone
import busio
import board
import adafruit_tsl2591
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from email.utils import format_datetime

pieId = "raspPi2"

i2c = busio.I2C(board.SCL, board.SDA)

timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def init_bme(i2c):
    try:
        bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        print("BME680 initialized")
        return bme
    except Exception as e:
        print("Error initializing BME680")
        return None

def init_tsl(i2c):
    try:
        tsl = adafruit_tsl2591.TSL2591(i2c)
        print("TSL2591 initialized")
        return tsl
    except Exception as e:
        print("Error initializing TSL2591")
        return None

def init_ads(i2c):
    try:
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P0)
        print("ADS1115 initialized")
        return ads, chan
    except Exception as e:
        print("Error initializing ADS1115")
        return None

def read_sensors():

    bme = init_bme(i2c)
    tsl = init_tsl(i2c)
    ads, chan = init_ads(i2c)
    
    try:
        if bme:
            temperature = bme.data.temperature
            humidity = bme.data.humidity
            pressure = bme.data.pressure
            gas = bme.data.gas_resistance
            print("bme\n")
        else:
            print("bme failed\n")
            temperature = -1
            humidity = -1
            pressure = -1
            gas = -1
    except Exception as e:
        print("sensor error", e)
        
    try:
        if tsl:
            lux = tsl.lux
            print("tsl\n")
        else:
            print("tsl failed\n")
            lux = -1
    except Exception as e:
        print("sensor error", e)
        
    try:
        if ads and chan:
            rawVal = chan.value
            volts = chan.voltage
            print("ads\b")
        else:
            print("ads failed\n")
            rawVal = -1
            volts = -1
    except Exception as e:
        print("sensor error", e)        
    
    return {
        "pieId" : pieId,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "gas resistance": gas,
        "lux": lux,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "rawVal" : rawVal,
        "volts" : volts
    }
