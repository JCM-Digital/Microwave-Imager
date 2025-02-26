import serial
import time
from PIL import Image
import numpy as np
import regex as re

# Generate timestamp
timestr = time.strftime("%Y%m%d-%H%M%S")

# Define "dish" as the serial port device to interface with
dish = serial.Serial(
    port='/dev/tty.usbmodem14601',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)

print("Serial port connected")

# Helper function to send commands and handle responses
def send_command(command, retries=5, delay=1):
    """Send a command to the dish and handle retries."""
    for attempt in range(retries):
        print(f"Sending command: {command}")

        # Send each character one by one
        for char in command:
            dish.write(char.encode())  # Send character
            dish.flush()  # Ensure character is transmitted
            time.sleep(0.1)  # Short delay between characters

        # Add the line ending (CR)
        dish.write("\r".encode())
        dish.flush()

        time.sleep(delay)  # Wait for the device to process

        # Read response
        response = ''
        while True:
            line = dish.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response += line + "\n"
            else:
                break

        print(f"Raw reply: {response.strip()}")

        if response.strip():
            print(f"Valid reply: {response.strip()}")
            return response.strip()

        print(f"Warning: Empty reply from device. Retrying ({attempt + 1}/{retries})...")

    print(f"Failed to send command: {command} after {retries} retries.")
    return None

# Function to normalize signal strength to a range of 0-255
def normalize_signal(signal_strength):
    max_signal = 3000  # Assuming maximum signal strength is 3000
    min_signal = 2900  # Assuming minimum signal strength is 2900
    if signal_strength < min_signal:
        signal_strength = min_signal
    elif signal_strength > max_signal:
        signal_strength = max_signal
    normalized_signal = int(((signal_strength - min_signal) / (max_signal - min_signal)) * 255)
    return normalized_signal

# Function to save scan settings in scientific notation
def save_scan_settings(az_start, az_end, el_start, el_end, resolution):
    with open(f"scan-settings-{timestr}.txt", 'w') as file:
        file.write(f"{float(az_start):.18e}\n")
        file.write(f"{float(az_end):.18e}\n")
        file.write(f"{float(el_start):.18e}\n")
        file.write(f"{float(el_end):.18e}\n")
        file.write(f"{float(resolution):.18e}\n")

# Function to handle sweeping
def handle_sweep(azimuth, elevation):
    """Handles sweeping logic for signal measurement."""
    print(f"Azimuth: {azimuth}, Elevation: {elevation}")
    if not send_command(f"azangle {azimuth}"):
        return  # Skip this azimuth if the command fails

    response = send_command("rfwatch 1")
    signal_strength = -1  # Default placeholder value

    if response:
        try:
            reply = response.strip()
            header, *readings = reply.split('[5D')
            output = readings[0] if readings else ''
            output = re.sub(r'\p{C}', '', output)
            output = re.sub(r'[^\d]', '', output).strip()

            if output:
                signal_strength = int(output)
        except (ValueError, IndexError):
            print(f"Malformed RF data: {response}. Using placeholder value.")

    print(f"Signal: {signal_strength}")

    # Record raw data to array
    sky_data[abs(elevation - el_end) // 17, abs(azimuth - az_end)] = signal_strength
    np.savetxt(f"raw-data-{timestr}.txt", sky_data)

    # Update bitmap for valid signals
    if signal_strength >= 0:
        normalized_signal = normalize_signal(signal_strength)
        image_x = int(abs(azimuth - az_end))
        image_y = int(abs(elevation - el_end) // 17)
        data[image_x, image_y] = (normalized_signal, 0, 0)
        sky_image.save(f"result-{timestr}.png")

# Initial setup and user prompts for parameters
az_start = int(input('Starting Azimuth in degrees (0-360, default 90): ') or 90)
az_start = max(0, min(az_start, 360))
az_end = int(input('Ending Azimuth in degrees (default 270): ') or 270)
az_end = max(0, min(az_end, 360))

el_start_deg = int(input('Starting Elevation in degrees (0-70, default 0): ') or 0)
el_start_deg = max(0, min(el_start_deg, 70))
el_start = 400 + (el_start_deg * 17)

el_end_deg = int(input('Ending Elevation in degrees (default 70): ') or 70)
el_end_deg = max(0, min(el_end_deg, 70))
el_end = 400 + (el_end_deg * 17)

resolution = int(input('Resolution (1=low, 2=high, default 1): ') or 1)
resolution = 1 if resolution not in (1, 2) else resolution

# Save scan settings
save_scan_settings(az_start, az_end, el_start, el_end, resolution)

# Data and image setup
sky_image = Image.new('RGB', [az_end - az_start + 1, (el_end - el_start) // 17 + 1], 'white')
data = sky_image.load()
sky_data = np.zeros(((el_end - el_start) // 17 + 1, az_end - az_start + 1))

# Move dish to the starting position
print("Moving dish to starting position...")
if not send_command(f"azangle {az_start}"):
    print("Error: Failed to set azimuth. Exiting.")
    exit()

if not send_command(f"elangle {el_start}"):
    print("Error: Failed to set elevation. Exiting.")
    exit()

time.sleep(2)

# Main scanning loop
for elevation in range(el_start, el_end + 17, 17):
    if not send_command(f"elangle {elevation}"):
        print(f"Error: Failed to adjust elevation to {elevation}. Exiting.")
        exit()

    if (elevation - el_start) // 17 % 2 == 0:
        for azimuth in range(az_start, az_end + 1):
            handle_sweep(azimuth, elevation)
    else:
        for azimuth in range(az_end, az_start - 1, -1):
            handle_sweep(azimuth, elevation)

    time.sleep(2)

print("Scan complete!")
dish.close()
