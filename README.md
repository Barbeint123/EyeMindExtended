# Table of Content
1. [Hardware and Software Requirements](#Hardware-and-Software-Requirements)
    
   1.1. [Hardware Requirements](#Hardware-Requirements)

    1.2. [Software Requirements](#Software-Requirements)

2. [Installation Procedure](#Installation-Procedure)

    2.1. [Eye-Tracking Server Installation](#Eye-Tracking-Server-Installation)

    2.2 [EyeMind App Installation](#EyeMind-App-Installation)

3. [User Manual](#User-Manual)

# Hardware and Software Requirements

## Hardware Requirements

- To run EyeMind for data collection, you need an eye-tracking device and a Computer Machine with Windows 10 or 11.

    EyeMind uses the Tobii Pro SDK (i.e., https://developer.tobiipro.com/python/python-getting-started.html) supporting Tobii Screen-based Eye-trackers (i.e., https://www.tobii.com/products/eye-trackers/screen-based). The tool was tested on Tobii X3-120 (i.e., https://connect.tobii.com/s/x3-downloads?language=en_US)

- To run EyeMind for data analysis, you need a Computer Machine with Windows 10 or 11.

## Software Requirements

- Git (i.e., https://git-scm.com/downloads) to clone the EyeMind repository from github.com
- Python 3.8.6 (i.e., https://www.python.org/downloads/release/python-386/) (Choose the distribution AMD64 on win32 which is compatible with Tobii Pro SDK)
- Pip (i.e., https://phoenixnap.com/kb/install-pip-windows) (for a quick installation of Python Libraries)
- Npm and node.js (i.e., https://nodejs.org/en/download/) to run EyeMind
- Tobii Pro Eye Tracker Manager (i.e., https://developer.tobiipro.com/eyetrackermanager/etm-installation-information.html) to install the eye-tracking device and conduct the calibration of the device

# Installation Procedure

EyeMind is composed of two services: the Eye-Tracking Server and the EyeMind App. This guide will walk you through the installation process for both services.

Start by cloning EyeMind to your local machine. In the following we will assume that the cloning folder is called "EyeMind".

    
    cd <root path>
    git clone https://github.com/aminobest/EyeMind

### Eye-Tracking Server Installation

Follow the steps below to install the Eye-Tracking Server:


- **Navigate to the EyeTrackingServer folder:**

    ```
    cd <root path>\EyeMind\EyeTrackingServer
    ```

- **Install Python dependencies:** Once you are inside the EyeTrackingServer folder, install the required Python dependencies using the following command:

    ```
    pip install -r requirements.txt --user
    ```

- **Set Permissions:** Ensure the folder "\EyeTrackingServer\out\logs" has read and write permissions (chmod 777). The eye-tracking raw data will be recorded here. Preserve this data, as it could be useful for future recovery.


### EyeMind App Installation


- **Navigate to the EyeMind App folder:** Open a new terminal window, and navigate to the EyeMind App folder using the command:

    ```
    cd <root path>\EyeMind\EyeMindApp\
    ```

- **Install dependencies:** Install the necessary dependencies using the command:

    ```
    npm run install-dependencies
    ```

- **Build the app:** Build the EyeMind App using the following command:

    ```
    npm run build
    ```


# User Manual

The video in  https://andaloussi.org/SoftwareX2023/demo.html illustrates the procedures explained in this section.