import serial
import time

# Define the LoRa serial port
lora = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

# Send configuration commands to the LoRa module
lora.write(b'AT+ADDRESS=1\r\n')
time.sleep(0.1)
lora.write(b'AT+NETWORKID=5\r\n')
time.sleep(0.1)
lora.write(b'AT+BAND=433\r\n')
time.sleep(0.1)

try:
    while True:
        if lora.in_waiting:
            incomingString = lora.readline().decode("utf-8").strip()
            print(incomingString)

            data = incomingString.split(',')
            if len(data) >= 4:
                received_data = data[3]
                print("Received data:", received_data)

except KeyboardInterrupt:
    print("Keyboard Interrupt. Exiting...")
except Exception as e:
    print("Error:", str(e))
finally:
    lora.close()
