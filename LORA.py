import aioserial
from serial import EIGHTBITS, PARITY_NONE,  STOPBITS_ONE
import time

port = '/dev/ttyS0'
baudrate = 9600
parity = PARITY_NONE
bytesize = EIGHTBITS
stopbits = STOPBITS_ONE
timeout = None

aio = aioserial.AioSerial(
          port = port,
          baudrate = baudrate,
          parity = parity,
          bytesize = bytesize,
          stopbits = stopbits,
          timeout = timeout)

async def ATcmd(cmd: str = '') -> int:
    command = 'AT' + ('+' if len(cmd) > 0 else '') + cmd + '\r\n'
    global aio
    count : int  = await aio.write_async(bytes(command, 'utf8'))
    return count

async def main_func():
    # Define the LoRa serial port
    # lora = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    GPIO.setup(self.RST,GPIO.OUT,initial=GPIO.HIGH) # the default anyway

# Send configuration commands to the LoRa module
# lora.write(b'AT+ADDRESS=1\r\n')
# time.sleep(0.1)
# lora.write(b'AT+NETWORKID=5\r\n')
# time.sleep(0.1)
# lora.write(b'AT+BAND=433\r\n')
# time.sleep(0.1)

    await ATcmd('ADDRESS=1')
    await ATcmd('NETWORKID=5')
    await ATcmd('BAND=433')

    try:
        while True:
            # if lora.in_waiting:
                # incomingString = lora.readline().decode("utf-8").strip()
                # print(incomingString)

                # data = incomingString.split(',')
                # if len(data) >= 4:
                   #  received_data = data[3]
                    # print("Received data:", received_data)
            if aio.in_waiting > 0:
                data = await aio.read_async(size=1)
                print(data)

    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting...")
    except Exception as e:
        print("Error:", str(e))
    finally:
        lora.close()

main_func()
