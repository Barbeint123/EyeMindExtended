# Table of Content
1. [Overview](#Overview)

2. [Hardware and Software Requirements](#Hardware-and-Software-Requirements)
    
   2.1. [Hardware Requirements](#Hardware-Requirements)

    2.2. [Software Requirements](#Software-Requirements)

3. [Installation Procedure](#Installation-Procedure)

    3.1. [Eye-Tracking Server Installation](#Eye-Tracking-Server-Installation)

    3.2 [EyeMind App Installation](#EyeMind-App-Installation)

4. [Features](#Features)

# Overview

An integration of  [EyeMind](https://github.com/aminobest/EyeMind) with [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace). Read the paper [paper](./paper.pdf) for details explaining background and the necessity of such a tool.

# Hardware and Software Requirements

### Hardware Requirements:
- Eyetracker with Tobii SDK access.  
  *Note: This application has only been tested with **Tobii Pro X3-120**, but it should work with other Tobii eyetrackers that support the SDK.*
- Webcam.  

These devices must be connected to the computer running the application. Note that some Tobii eye-trackers require a connection to a USB 3 port.

### Software Requirements:
- **64-bit Windows 10 or 11**  
  *Note: Windows 11 is currently supported but will not be in future versions with wristband data.*
- [**Python 3.8.6**](https://www.python.org/downloads/release/python-386/) (choose AMD64 for Win32).
- [**Pip**](https://phoenixnap.com/kb/install-pip-windows).
- [**NPM & Node.js**](https://nodejs.org/en/download/package-manager).
- [**Tobii 1.10.1 SDK**](https://pypi.org/project/tobii-research/1.10.1/).
- [**Tobii Eye Tracker Manager**](https://developer.tobiipro.com/eyetrackermanager/etm-installation-information.html).  
  - *For discontinued eyetrackers, download **Tobii Pro Eye Tracker Manager 2.6.1** instead from [here](https://connect.tobii.com/s/article/new-Tobii-Pro-SDK-and-ETM?language=en_US).*
- [**Visual Studio 2017**](https://visualstudio.microsoft.com/vs/older-downloads/)  
  *Alternatively, install the 64-bit Visual C++ Redistributable Package from [here](https://aka.ms/vs/16/release/vc_redist.x64.exe).*


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


# Features
The EyeMind features is explained in the following video https://andaloussi.org/SoftwareX2023/demo.html. 

The added OpenFace functionality is incorporated behind the scenes, and its output data is found under the same output directory as the EyeMind functionality.
