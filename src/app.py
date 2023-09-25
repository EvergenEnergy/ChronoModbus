from pymodbus.client import ModbusTcpClient
import csv
import time
from datetime import datetime


# Function to write to Modbus slave
def write_to_modbus(client, address, value):
    client.write_register(address, value, 1)


# Read CSV file and store data
csv_data = []
with open('../data/24H_1M_Industrial_Refrigeration_Data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        csv_data.append(row)

# Remove header if exists
if csv_data[0][0] == 'Time':
    csv_data.pop(0)

# Initialize Modbus client
client = ModbusTcpClient(host='0.0.0.0', port=5022)
client.connect()

current_row_index = 0

# Find the closest matching time in the CSV that is either equal to or earlier than the current time
current_time = datetime.now().strftime('%H:%M')
while current_row_index < len(csv_data):
    csv_time, _ = csv_data[current_row_index]
    if csv_time >= current_time:
        break
    current_row_index += 1

# If you've reached the end of csv_data, reset current_row_index to 0
if current_row_index == len(csv_data):
    current_row_index = 0

some_address = 40500

try:
    while current_row_index < len(csv_data):
        # Get system time in HH:MM format
        current_time = datetime.now().strftime('%H:%M')

        # Get the time and value for the current row from CSV
        csv_time, csv_value = csv_data[current_row_index]
        csv_value = int(float(csv_value))

        csv_time = csv_time[:5]

        print(f"Time is {csv_time} while current time is {current_time}")

        # If current time matches CSV time, write value to Modbus and move to the next row
        if current_time == csv_time:
            print(f"Writing to Modbus at time {current_time}: {csv_value} kW")  # Print time and value

            write_to_modbus(client, some_address, csv_value)
            current_row_index += 1  # Move to the next row

        # Wait before checking the time again
        time.sleep(10)  # You can adjust this duration based on your needs

finally:
    client.close()
