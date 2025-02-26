import numpy as np
import matplotlib.pyplot as plt
import sys

# Define the path to the raw data file
data_file ='/Users/jorgemontes/Documents/Dish tailgater/Tailgater-Microwave-Imaging-Original/examples/raw-data-20230321-193653.txt'# Update with the correct file path
scan_params_file ='/Users/jorgemontes/Documents/Dish tailgater/Tailgater-Microwave-Imaging-Original/examples/scan-settings-20230321-193653.txt'# Update with the correct file path

# Open the filename passed at runtime (raw data file)
print('Loading data file.')
with open(data_file, 'r') as file_name:
    sky_data = np.loadtxt(file_name)

# Pull timestamp from filename (there's probably a better way to do this)
header, *filename_parts = str(file_name).split('-')
file_name = str(filename_parts[2])
header, *split = file_name.split('.')
timestamp = (filename_parts[1] + '-' + header)

# Loading scan settings (azimuth and elevation parameters, resolution)
print('Loading parameters of scan.')
scan_params = np.loadtxt(scan_params_file)  # Scan settings are loaded here
az_start = int(scan_params[0])
az_end = int(scan_params[1])
el_start = int(scan_params[2])
el_end = int(scan_params[3])
resolution = int(scan_params[4])

# Printing scan parameters for confirmation
print(f'Azimuth Range: {az_start} to {az_end}')
print(f'Elevation Range: {el_start} to {el_end}')
print(f'Resolution: {resolution}')

if resolution == 1:  # Standard low resolution
    # Trim off the messy edges of the array (probably an ugly hack)
    cleaned_data = np.delete(sky_data, obj=0, axis=0)
    cleaned_data = np.delete(cleaned_data, obj=0, axis=1)
    # Optionally remove any edge data if needed: cleaned_data = np.delete(cleaned_data, obj=(az_end-az_start-1), axis=1)

    # Set up custom axis labels for low resolution
    x = np.array([0, (az_end - az_start - 1) / 2, az_end - az_start - 2])
    az_range = np.array([az_end, (az_start + az_end) / 2, az_start])
    plt.xticks(x, az_range)
    y = np.array([0, (el_end - el_start - 1) / 2, el_end - el_start - 1])
    el_range = np.array([el_end, (el_start + el_end) / 2, el_start])
    plt.yticks(y, el_range)

elif resolution == 2:  # Higher resolution
    # Trim off the messy edges of the array (probably an ugly hack)
    cleaned_data = np.delete(sky_data, obj=0, axis=0)
    cleaned_data = np.delete(cleaned_data, obj=0, axis=1)
    # Optionally remove more data for higher resolution

    # Set up custom axis labels for high resolution
    x = np.array([0, (((az_end - az_start) * 5) - 1) / 2, ((az_end - az_start) * 5) - 2])
    az_range = np.array([az_end, (az_start + az_end) / 2, az_start])
    plt.xticks(x, az_range)
    y = np.array([0, (((el_end - el_start) * 3) - 1) / 2, ((el_end - el_start) * 3)])
    el_range = np.array([el_end, (el_start + el_end) / 2, el_start])
    plt.yticks(y, el_range)

else:
    # Medium resolution not implemented yet
    print('Medium resolution not implemented.')

# Display message
print('Processing heatmap...')

# Display the heatmap
plt.imshow(cleaned_data, cmap='inferno')  # Change 'viridis' to any other colormap you prefer
plt.colorbar(location='bottom', label='RF Signal Strength')
plt.xlabel("Azimuth (dish uses CCW heading)")
plt.ylabel("Elevation")
plt.title(f"Microwave Imager Scan {timestamp}")

# Show the plot
#'hot'
#'viridis'
#'inferno'
#'plasma'
#'magma'
#'cividis'
#'coolwarm'
#'spring'
#'summer'
#'winter'
#'rainbow'

plt.show()
