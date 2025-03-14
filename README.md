# <div align="center">Radio Telescope Imaging and Scanning Scripts</div>

![Figure_1_Pano](https://github.com/user-attachments/assets/3f134054-87e4-404c-a625-02e1f25c0f7c)


This repository contains three Python scripts used for interfacing with a radio telescope system. The code should be used on any dish tailgaiter models built between 2011-2015. Each script is designed to handle different aspects of the telescope's operation, including image generation, normalization, and raw data scanning. Key Python modules such as `matplotlib`, `PIL`, and `numpy` are utilized to manage image processing and data manipulation.

![Figure_3_Hotwith text](https://github.com/user-attachments/assets/adc80713-2ffc-4b0f-9bf1-a90ccf688639)

![McrowaveImagingresults_2-6-25](https://github.com/user-attachments/assets/5d7ad3a6-69da-4aa1-9bc0-138868f35e40)


## <div align="center">1. Dish Image Processing (`dish_image.py`)</div>

This script processes the raw data from the radio telescope to generate visual representations of the scans using `matplotlib` and `numpy`. It handles file input, data manipulation, and visual output to create detailed heatmaps of the received signals.

![Image 2-26-25 at 12 56 AM](https://github.com/user-attachments/assets/1caddd59-9613-4344-846a-b7a68e62fc0c) 

![IMG_0736](https://github.com/user-attachments/assets/bd6ff123-0049-4531-a0c5-231ed6183d7b)


### Features:
- **Data Loading and Processing**: Utilizes `numpy` for numerical operations on the raw data.
- **Visualization**: Employs `matplotlib` to plot and customize heatmaps with various colormap options.
- **File Management**: Handles input and output files to load scan settings and save the resulting images.

## <div align="center">2. Dish Scan Normalization (`dish_scan_normalization.py`)</div>

This script extends the functionality of the dish scanning by adding signal normalization and detailed image output. It uses `serial` for communication, `numpy` for numerical calculations, and `PIL` (Pillow) for image creation.

![Figure_2Viridis](https://github.com/user-attachments/assets/5278d25f-2eca-405b-b615-24e6cbe602be)

### Features:
- **Serial Communication**: Manages communication with the dish, sending commands and receiving responses.
- **Signal Normalization**: Uses `numpy` to normalize the signal strengths to a 0-255 range.
- **Image Generation**: Leverages `PIL` to convert normalized data into RGB images, visualizing the intensity of signals.

## <div align="center">3. Dish Raw Scan (`dish_scan.py`)</div>

This script focuses on raw data collection from the dish without normalization. It controls the dish's movement to capture raw signal data across specified azimuth and elevation ranges, using `numpy` to handle data and `PIL` for basic visualization.

### Features:
- **Direct Dish Control**: Uses `serial` to handle precise dish positioning.
- **Data Collection and Storage**: Employs `numpy` to store and manage raw signal data.
- **Simple Visualization**: Utilizes `PIL` to map signal data directly to RGB values, providing a straightforward visual output.

## <div align="center">Installation and Usage</div>

To use these scripts, clone this repository, install the required dependencies listed in `requirements.txt`, and run each script as needed with Python 3.x. Ensure your system has access to the appropriate serial port that the dish is connected to.

## <div align="center">Contributions</div>

Contributions to this project are welcome. Please fork this repository, make your changes, and submit a pull request.
