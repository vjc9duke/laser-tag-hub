import serial

# Configure the serial port
ser = serial.Serial('/dev/serial0', 115200)  # Use the appropriate serial port and baud rate

try:
    while True:
        # Read data from the serial port
        message = ser.readline().decode('utf-8').rstrip()
        message_bytes = message.encode('utf-8')
        self.serial_thread.serial_port.write(message_bytes)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Serial communication stopped.")
    ser.close()  # Close the serial port when the program is interrupted
