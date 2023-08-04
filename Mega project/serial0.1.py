import serial

arduinoData=serial.Serial("COM3",9600)

def led_on():
    arduinoData.write('1')

def led_off():
    arduinoData.write('0')

led_on()
