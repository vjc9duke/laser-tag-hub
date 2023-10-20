import serial

# Configure the serial port
ser = serial.Serial('/dev/serial0', 9600)  # Use the appropriate serial port and baud rate

try:
    while True:
        # Read data from the serial port
        received_data = ser.readline().decode('utf-8').strip()
        
        # Process the received data
        print("Received: {}".format(received_data))

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Serial communication stopped.")
    ser.close()  # Close the serial port when the program is interrupted
