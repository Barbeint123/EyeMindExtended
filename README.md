# Table of Content

1. [Overview](#Overview)
2. [Citation](#Citation)
3. [License](#License)
4. [Hardware and Software Requirements](#Hardware-and-Software-Requirements)
    
   4.1. [Hardware Requirements](#Hardware-Requirements)

    4.2. [Software Requirements](#Software-Requirements)

5. [Installation Procedure](#Installation-Procedure)

    5.1. [Eye-Tracking Server Installation](#Eye-Tracking-Server-Installation)

    5.2 [EyeMind App Installation](#EyeMind-App-Installation)

6. [User Manual](#User-Manual)

    6.1. [Data Collection](#Data-Collection)

   6.1.1. [Important Notes](#Important-Notes)

   6.1.2. [Setup of The Experimental Workflow in The EyeMind App](#Setup-of-The-Experimental-Workflow-in-The-EyeMind-App)

   6.1.3. [Starting the Eye-Tracking Server](#Starting-the-Eye-Tracking-Server)

   6.1.4. [Calibration of the Eye-tracking device](#Calibration-of-the-Eye-tracking-device)

   6.1.5. [Recording of The Eye-tracking Data using the EyeMind App](#Recording-of-The-Eye-tracking-Data-using-the-EyeMind-App)

   6.1.6. [Required Interactions with the EyeMind App and The Eye-Tracking Server When The Recording Is Over](#Required-Interactions-with-the-EyeMind-App-and-The-Eye-Tracking-Server-When-The-Recording-Is-Over)

   6.1.7. [General Notes](#General-Notes-Data-Collection)

   6.2. [Analysis](#Analysis)

   6.2.1. [File Import](#File-Import)

   6.2.2. [File Export](#File-Export)

   6.2.3. [Fixation Filter](#Fixation-Filter)

   6.2.4. [Heatmap and Overlays](#Heatmap-and-Overlays)

   6.2.5. [Gaze Offset Correction](#Gaze-Offset-Correction)

   6.2.6. [General Notes](#General-Notes-Analysis)

   6.2.7. [Other Comments](#Other-Comments)

7. [Interpreting EyeMind Data](#Interpreting-EyeMind-Data)

    7.1. [Mapping Gaze Points to The Process Model or UI Elements](#Mapping-Gaze-Points-to-The-Process-Model-or-UI-Elements)

8. [Demonstration and Validation](#Demonstration-and-Validation)

   8.1. [Video Demonstration](#Video-Demonstration) 
   
   8.2 [Demonstration Material](#Demonstration-Material)

   8.3. [Validation of Data Quality](#Validation-of-Data-Quality)

   8.4. [Test Cases](#Test-Cases)

    8.4.1 [EyeMind App Test Cases](#Eye-Mind-App-Test-Cases)

   8.4.2 [Eye-Tracking Server Test Cases](#Eye-Tracking-Server-Test-Cases)

# Overview

EyeMind is a tool that supports eye-tracking experiments on large and interactive process models.
Among the key features of EyeMind are the following:
- Experimental workflow configuration
- Automated mapping of gazes to dynamic areas of interests (corresponding to the process model elements)
- Analysis of eye-tracking data: gaze correction, fixation filter, heatmaps and overlays

The following video demonstrates the features of EyeMind https://andaloussi.org/SoftwareX2023/demo.html.

# Citation

   ```
  Abbad-Andaloussi A., Lübke D. & Weber B. (2023). 
  Conducting Eye-tracking Studies on Large Process Models Using EyeMind.
  Software X (101564).
  ```

# License

MIT License

Copyright (c) 2023 EyeMind.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



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

## Data Collection

### Important Notes

- **Supported Features:** The application supports 
   - Scrolling (using the mouse wheel or by dragging the model canvas) and zooming
   - Navigation between files
   - Changing the order of tabs, and horizontal scrolling on the tabs pane using either the mouse wheel or the left and right arrow icons on the tab pane to view more tabs.
   - Use for a secondary screen as long as the EyeMind is shown on the **primary screen**
-  **Unsupported Features:** The application does not support
   - Reading while scrolling
   - zooming the whole app (e.g., using the magnifier accessibility feature of Windows)
   - Using groups in the BPMN models.


### Setup of The Experimental Workflow in The EyeMind App

#### Running the EyeMind App

- Navigate to the EyeMind App folder:

    ```
    cd <root path>\EyeMind\EyeMindApp\
    ```

- Run the EyeMind App:

    ```
    npm start
    ```

#### Configuration

- Your computer should be plugged to a single screen
- To enable Symbolic links and breadcrumb navigation, the collapsed subprocess should have the same id as the sub-process file (you can do this use Camunda modeler)
-  The main process model should have the id "main" or "Main"
- The sub-processes should be stored in different files (avoid using the sub-processes links available in bpmn.io where one collasped sub-process, leads you to the underlying model)
- You should know in advance the following information

    - a. screen resolution (recommended 1920-1080)

    - b. screen dimension in inches
  
    - c. distance between the eye-tracker and the participant
-  There should be no display scalling in your computer

##### Models Import

- You can use "drag and drop" to add models
- The models should have unique file names (these files names should result in a unique pattern after applying filename.replace(/[\W_,.]/g,""))
- The order in which the files appear corresponds to the order in which they will show up in the file explorer
- Models of different processes should be asigned different group names

#### Questions Import

- The questions should be formatted in a csv file, with a structure similar to  [Examples/video demonstration material/Experiment-workflow/questions.csv/](Examples/video%20demonstration%20material/Experiment-workflow/questions.csv)
- The questions should have a unique id
- The type of each question can be "open-question" or "multiple-choice". If "multiple-choice", then the options should be provided in the following format: "<option 1>;<option 2>;<option 3>"
- Each question should be mapped to a specific process using the attribute model-group

####  Saving and Importing of Experimental Worflows for Future Data Collection

- After importing the models and the questions, you can press the red recording button at the top of the main view, provide the eye-tracking recoding settings and then save the session (with models, questions and eye-tracking settings)
- Afterwards, you can import this session and directly start the recording

#### Data Recording

- Once the models and the questions are loaded, or a session is loaded, you are ready to start the data collection 
- The tool will be set to full screen, but you can use the meta key to navigate to other tools

### Starting the Eye-Tracking Server


- Navigate to the EyeTrackingServer folder:

    ```
    cd <root path>\EyeMind\EyeTrackingServer
    ```

- Run the Eye-Tracking Sever using the following terminal command:

    ```
   python main.py
    ```

- Wait until you see "found tobii tracker at ...". If no eye-tracker is found. Please try again in about a minute (this is because the eye-tracker needs time to be recognized by the computer when connected)


### Calibration of the Eye-tracking device

- Use Tobii Pro Eye Tracker Manager to calibrate the eye-tracking device (cf.  https://andaloussi.org/SoftwareX2023/demo.html).

### Recording of The Eye-tracking Data using the EyeMind App

- Instruct the participants *NOT TO* to press the following: ctrl+r (refresh the app), ctrl+esc (go out from the full screen), alt (show advanced menu)

-  No window should superpose the recording window at any time
	
- Go to EyeMind tool and press the recording (red) buttom

- You must provide/see the following information in the form before you can proceed
  - X Screen dimension in pixels
  - Y Screen dimension in pixels
  - Screen distance in centimeters
  - Monitor size in inches
  - Recording ID
  
- Press start recording
- The main model and the first question will show up
- When the experiment is over, you can press the black sqaure (which refers to stop recording)

### Required Interactions with the EyeMind App and The Eye-Tracking Server When The Recording Is Over

- By the end of the recording, you will see the tool rendering some snapshots of your interactions with the process models. This is part of the procedure. Just wait.
- Wait until you see a message informing you that the data is saved. The message shows also the path of the saved data (i.e., <root path>EyeMind\EyeMindApp\outputData)
- After saving the file, wait a few seconds, then check that the file is in your folder before refreshing the app using crt+R

### General Notes:

- You can always start a new data collection session using ctrl+r (refresh). Remember that when you refresh all the non-saved data is deleted.
- In case the processing takes very long, you can use ctrl+shift+i to the open the developer tool and inspect the error.
- It is recommended to start a new instance of Eye-Mind for every new data collection or analysis session.

## Analysis

### File Import

- You can import several files corresponding to several data collection sessions.

### File Export

- You can export the following:
    - Analysis data (json)
    - Gaze data (csv)
    - Fixation data (csv) (you need to apply the fixation filter before you can export the fixation data)

### Fixation Filter
   - Use green filter button on the top menu access the fixation filter

### Heatmap and Overlays
  - Use the rainbow colored button to see the heatmaps and overlays
  - Choose one or several participants, question, metric, aggregation, timestamp unit and which BPMN elements to additionally include (activites, events, gateways, labels, data objects are included by default)
  - Use the file explorer to access the models 
  - To exit the heatmap and overlays press the same icon again

### Gaze Offset Correction
  - Use the red pointer icon on the top menu to access the gaze correction feature
  - Choose the data sample percentage on which you want to see the projections (for better performance, it is recommended to choose a small sample)
  - Use the file explorer to see the snapshots with gaze projections on each model
  - use the "general offset correction" menu to set corrections on the x and y axes. Note that the corrections here are only made to the data sample. so no data is affected yet.
  - Use the file explorer to see the snapshots with gaze projections on each model after the correction
  - If you are satisified with the correction you can apply it to the whole dataset. For this press "Apply correction to data", then a pop-up will open, press start, and wait until the rendering of snapshots (to redo the mapping between gazes and dynamic AOIs) is complete
  - Very Important note: for now, the gaze projections and corrections were tested on a computer with the same resolution on which the data collection has occurred.
  - To exit the gaze offset correction press its icon again

### General Notes
  - you can always start a new analysis session using ctrl+r (refresh). Remember that when you refresh all the non-saved data is lost. 
  - In case the processing takes very long, you can use ctrl+shift+i to the open the developer tool and inspect the error.


# Interpreting EyeMind Data

## Mapping Gaze Points to The Process Model or UI Elements

- In the log files (i.e., fixation file, gaze data file, analysis file), the attribute "element" refers to the element gazed by the user
- This element can be one of the following
    - The id of a model element (e.g, activitiy, gateway)
    - File explorer (visible in the no-link mode)
        - File explorer area
            - file-explorer-area
        - Folder 
            - Pattern: file-explorer-folder_<Folder name>
        - File
            - Pattern: file-explorer-file_<Model name>
    - Process hierarchy explorer (visible in the breadcrumb mode)
        - Pattern: process-hierarchy-sub-process-link-to_<Subprocess activity label || main>
    - Tabs
        - Tab header
            - Pattern: tab-header-tab-link-to_<Model name>
        - File Name in tab header
            - Pattern: tab-link-to_<Model name>
        - Close button in tab header
            - Pattern: close-button-tab-link-to_<Model name>
    - Quetions
        - Question area
            - Pattern: question-area-for-questionID_<Question id (i.e, as provided in the questions file)>
        - Question title
            - Pattern: title-for-questionID_<Question id>
        - Answer area
            - Pattern: answer_area_for_questionID_<Question id>
        - Input field for open questions
            - Pattern: long-answer-for-questionID_<Question id>
        - Radio buttons for multiple choice questions
            - Pattern: option-answer-for-questionID_<Question id>_option_<Option text (i.e., as provided in the questions file>
        - Next button
            - Pattern: next-button-area-in-questionID_<Question id>

## Interpreting Click Events

- The following click events are recorded in the gaze file and analysis file

    - Model
        - Clicks on sub processes
            - Pattern: .<Subprocess activity id
    - File explorer
        -  File
            - Pattern: file-explorer-file_<Model name>
    - Process hierarchy explorer (visible in the breadcrumb mode)
      - Pattern: process-hierarchy-sub-process-link-to_<Subprocess activity label || main>
    - Tabs
        - File Name in tab header
            - Pattern: tab-link-to_<Model name>
        - Close button in tab header
            - Pattern: close-button-tab-link-to_<Model name>
    - Questions
        - Input field for open questions
            - Pattern: long-answer-for-questionID_<Question id>
        - Radio buttons for multiple choice questions
            - Pattern: option-answer-for-questionID_<Question id>_option_<Option text (i.e., as provided in the questions file>				
        - Next button
            - Pattern: next-button-area-in-questionID_<Question id>


# Demonstration and Validation

## Video Demonstration

The following video demonstrates the features of EyeMind

https://andaloussi.org/SoftwareX2023/demo.html

## Demonstration Material

The material used in the demonstration video and generated throughout the demonstration video is available in [Examples/Video demonstration material](Examples/video%20demonstration%20material).

- [Experiment-workflow](Examples/video%20demonstration%20material/Experiment-workflow): This directory contains the material used for the data collection (i.e., Process models in a BPMN format, questions file in a csv format, eye-tracking session pre-loaded with all the experimental workflow files (models, questions) and settings)

- [collectedData](Examples/video%20demonstration%20material/Collected-data): This directory contains the data collected during the demo (i.e., EyeMind json file containing all the recorded raw data, fixation and gaze data in CSV format)

## Data Collection Material

The material (i.e., process models and questions) used in the experiment validating EyeMind is available at [DataCollectionValidation/experimentMaterial/](DataCollectionValidation/experimentMaterial/).

## Validation of Data Quality

To validate the quality of the eye-tracking data collected with EyeMind, we compared random data samples collected with EyeMind with corresponding samples recorded simultaneously using the commercial tool Tobii Pro Lab (cf. https://www.tobii.com/products/software/behavior-research-software/tobii-pro-lab?gclid=EAIaIQobChMIzMXW9padgAMVM0GRBR0gxgC9EAAYASABEgLnEvD_BwE). 

The comparison involved confirming if both EyeMind and Tobii Pro Lab captured the same quantity of gaze events in each data collection session and if the events recorded by EyeMind matched those of Tobii Pro Lab in terms of timestamps and gaze coordinates. 
The results showed successful matching in all instances. 

Our Python Notebook in [DataCollectionValidation/dataCollectionValidation.ipynb](DataCollectionValidation/dataCollectionValidation.ipynb)  provides a comprehensive walkthrough of the comparison process.

## Test Cases


#### EyeMind App Test Cases


The test cases for the EyeMind App are written using the playwright library (i.e., https://playwright.dev/).
They can be found under [EyeMindApp/test/tests/playwright](EyeMindApp/test/tests/playwright)

To run the automated testing procedure, use the following terminal commands

- Start the Eye-Tracking Server in Test Mode

    ```
    cd <root path>\EyeMind\EyeTrackingServer
   python main.py testMode
    ```

- Run the tests using npm
    ```
    cd <root path>\EyeMind\EyeMindApp\
    npm test
    ```

In total **57** functional test cases were formulated. These test cases are distributed over several files (cf. [EyeMindApp/test/tests/playwright](EyeMindApp/test/tests/playwright)) as follows. 

- **canvas.test.ts** [EyeMindApp/test/tests/playwright/canvas.test.ts](EyeMindApp/test/tests/playwright/canvas.test.ts) _(4 tests)_: The file contains functional test cases testing the canvas (i.e., the area where the process models are shown) of the EyeMind App. 
- **clicks.test.ts** [EyeMindApp/test/tests/playwright/clicks.test.ts](EyeMindApp/test/tests/playwright/clicks.test.ts)  _(6 tests)_:  The file contains functional test cases testing different click interaction events registered by the EyeMind App.
- **file-explorer.test.ts** [EyeMindApp/test/tests/playwright/file-explorer.test.ts](EyeMindApp/test/tests/playwright/file-explorer.test.ts) _(1 test)_: The file contains a functional test case testing the file explorer (i.e., side-bar with file names) of the EyeMind App.
- **import.test.ts** [EyeMindApp/test/tests/playwright/import.test.ts](EyeMindApp/test/tests/playwright/import.test.ts) _(19 tests)_: The file contains functional test cases testing the import of files to the EyeMind App.
- **loaded-content.test.ts** [EyeMindApp/test/tests/playwright/loaded-content.test.ts](EyeMindApp/test/tests/playwright/loaded-content.test.ts) _(6 tests)_: The file contains functional test cases testing the loading of content to the EyeMind App.
- **mapping.test.ts** [EyeMindApp/test/tests/playwright/mapping.test.ts](EyeMindApp/test/tests/playwright/mapping.test.ts) _(3 tests)_: The file contains functional test cases testing the mapping between gazes and dynamic AOIs in the EyeMind App.
- **process-hierarchy-explorer.test.ts** [EyeMindApp/test/tests/playwright/process-hierarchy-explorer](EyeMindApp/test/tests/playwright/process-hierarchy-explorer.test.ts) _(3 tests)_: The file contains functional test cases testing the process hierarchy explorer (shown in the breadcrumb view mode) of the EyeMind App.
- **questions.test.ts** [EyeMindApp/test/tests/playwright/questions.test.ts](EyeMindApp/test/tests/playwright/questions.test.ts) _(3 tests)_: The file contains functional test cases testing the interactions with questions in the EyeMind App.
- **tabs.tests.ts** [EyeMindApp/test/tests/playwright/tabs.test.ts](EyeMindApp/test/tests/playwright/tabs.test.ts) _(4 tests)_: The file contains functional test cases testing the interactions with tabs in the EyeMind App.
- **takesnapshot.test.ts** [EyeMindApp/test/tests/playwright/takesnapshot.test.ts](EyeMindApp/test/tests/playwright/takesnapshot.test.ts) _(8 tests)_: The file contains functional test cases testing the recording of snapshots in the EyeMind App.

To run the test cases for a specific test file, use the following commands:

- Start the Eye-Tracking Server in Test Mode

    ```
    cd <root path>\EyeMind\EyeTrackingServer
   python main.py testMode
    ```

- Run the specific test file using
    ```
    cd <root path>\EyeMind\EyeMindApp\
    npx playwright test <<test_file_name>>
    ```

#### Eye-Tracking Server Test Cases

The test cases for the Eye-Tracking Server are written using the unittest Library in Python

In total **6** test cases were formulated. To run them, please use the following commands 


- Start the Eye-Tracking Server in Test Mode

    ```
    cd <root path>\EyeMind\EyeTrackingServer
   python main.py testMode
    ```

- Run the individual test cases
    ```
    cd <root path>\EyeMind\EyeTrackingServer\test
    python -m unittest tests.Tests.<<testName (see test names below)>>
    ```

The Eye-Tracking Server tests (cf. [EyeTrackingServer/test/tests.py](EyeTrackingServer/test/tests.py)) are the following:

- **test_ET_setup:** testing the setup of an eye-tracking session by the Eye-Tracking Server.
- **test_addSnapshot:** testing the recording of snapshots identifiers by the Eye-Tracking Server.
- **test_logFullSnapshot:** testing the recording of the full snapshots with their code by the Eye-Tracking Server.
- **test_addClickEvents:** testing the recording of click events by the Eye-Tracking Server.
- **test_addQuestionEvents:** testing the recording of question events by the Eye-Tracking Server.
- **test_mockGazeData:** testing the final processing of mock gaze data by the Eye-Tracking Server. 
