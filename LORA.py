import serial
import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
TX_PIN = 14
RX_PIN = 15
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN)

# Configure the serial port with GPIO pins
ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=9600,
    timeout=0.5,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

try:
    ser.open()
    print("Serial port opened successfully.")

    # Send configuration commands to the LoRa module
    ser.write(b"AT+ADDRESS=1\r\n")
    time.sleep(0.1)
    ser.write(b"AT+NETWORKID=5\r\n")
    time.sleep(0.1)
    ser.write(b"AT+BAND=433\r\n")
    time.sleep(0.1)

    while True:
        if ser.in_waiting:
            incomingString = ser.readline().decode("utf-8").strip()
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
    if ser.is_open:
        ser.close()
        print("Serial port closed.")
    GPIO.cleanup()
