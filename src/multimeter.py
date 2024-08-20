import pandas
import serial
import matplotlib
import serial.tools.list_ports
import time
import math

def switch_sign(byte0):
    sign = {
        0x2B: "+",
        0x2D: "-"
    }
    return sign.get(byte0)


def switch_unit(byte10):
    unit = {
        0x00: "°F",
        0x02: "°C",
        0x04: "F",
        0x08: "Hz",
        0x10: "hFE",
        0x20: "Ω",
        0x40: "A",
        0x80: "V"
    }
    return unit.get(byte10)


def switch_range(byte9):
    rnge = {
        0x00: "",
        0x10: "M",
        0x20: "k",
        0x40: "m",
        0x80: "µ"
    }
    return rnge.get(byte9)


def getdigits(byte123456):
    fst = chr(byte123456[0])
    snd = chr(byte123456[1])
    trd = chr(byte123456[2])
    fth = chr(byte123456[3])
    decpos = byte123456[5] & 0x07

    output = {
        0x00: (fst, snd, trd, fth),
        0x01: (fst, ".", snd, trd, fth),
        0x02: (fst, snd, ".", trd, fth),
        0x03: (fst, snd, trd, ".", fth),
        0x04: (fst, snd, trd, ".", fth)
    }
    return output.get(decpos, "NaN")


def parseBlock(block):
    sign = switch_sign(block[0])

    if (block[11] > 60 and block[10] == 0x20):
        dgts = 'OL'
    else:
        dgts = getdigits(block[1:7])
        #print(float(''.join(dgts)))
    rnge = switch_range(block[9] & 0xF0)
    unit = switch_unit(block[10])

    return (sign, ''.join(dgts), rnge, unit)


def parseBlockAndCalcTemp(block):
    rnge = {
        0x00: 10 ** 0,
        0x10: 10 ** 6,
        0x20: 10 ** 3,
        0x40: 10 ** -3,
        0x80: 10 ** -6
    }
    if len(block) > 10:
        if block[10] == 0x20:
            if block[11] < 60:
                resistance = float(''.join(getdigits(block[1:7]))) * rnge[
                    block[9]]  # berechne korrekten Wiederstand, Ziffern kommen als String aus getDigits()
                temp = calcTemp10KNTC(resistance)
                return temp
        else:
            return "NaN"
    else:
        return "NaN"


def calcTempPT100(R):
    R=R-wire_res
    if 180 < R < 1300:
        if R < 603:
            R += (603-R)/41.8
        R0 = 1000  # PT1000
        a = 3.9083 * 10 ** -3
        b = -5.775 * 10 ** -7
        # c = 202  # PT100: -4.183 * 10 ** -4
        # print('R= ', R, ', R0= ', R0)
        temp = (-a * R0 + math.sqrt((a * R0)*(a * R0) - 4 * b * R0 * (R0 - R))) / (2 * b * R0)  # Formel zur Berechnung der Temperatur (Wiederstandsthermometer)
        temp = int(temp)
    else:
        temp = "R not IR"
    return temp
def calcTemp10KNTC(R):
    R = R - 2 # Abziehen Kabelwiderstand von gemessenem Widerstand
    if 1000 < R < 30000:
        
        # Umrechnung f�r 10K NTC
        # x = ln(R/R0)
        # temp = 1/(a + b*x + c*x^2 + d*x^3)-273.15
        R0 = 10000
        x = math.log(R/R0)
        a = 0.0033540154
        b = 0.00025627725
        c = 0.000002082921
        d = 0.000000073003206
        temp = 1/(a + b*x + c*x**2 + d*x**3)-273.15
        temp = round(temp, 1) # Runden Temp. auf eine Nachkommastelle
    else:
        temp = 21.0
    return temp

if __name__ == '__main__':
    print("Available ports: ")
    print([comport.device for comport in serial.tools.list_ports.comports()])
    comport = 'COM7'#'input("Enter COM-Port: ")

    # while True:
    #     i = 3904
    #     while i > 185:
    #         print('Res: ' + str(i) + ' Temp: ' + str(calcTemp(i)))
    #         i = i-30
    #     input("exit")
    ser = serial.Serial(comport,
                        baudrate=2400,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)

    wire_res=6

    if(ser.isOpen()):
        while True:
            #input("Press ENTER to read data ")
            #time.sleep(0.5)
            #data = ser.read(14)
            #output = parseBlock(data)
            #print("%s %s %s%s" % output)
            #time.sleep(1)
            data = ser.read(14)
            output2 = parseBlockAndCalcTemp(data)
            print(str(output2)+" °C")
            print('')

    else:
        exit("Please restart Script")

