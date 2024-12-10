# MIT License

# Copyright (c) 2022 Eye-Mind Tool (Author: Amine Abbad-Andaloussi)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Added libraries for integration with OpenFace
import cv2
import time
import subprocess
# 

import numpy as np
import tobii_research as tr
import time
import random
import os
import sys
from flask import Flask, request
import json
import math
import pandas as pd
import statistics
from scipy.spatial import distance
import threading
import copy
import pickle
from waitress import serve


# activate test mode if applicable
testMode = False
if len(sys.argv)>1 and sys.argv[1] == "testMode":
    testMode = True
    print("Test mode activated")
#############

# activate OpenFace analysis if applicable
openFaceMode = False
if len(sys.argv)>1 and sys.argv[1] == "of":
    openFaceMode = True
    print("OpenFace analysis activated")
#############

# is set to True by default to delete raw footage for privacy reasons
# change to False, if raw video footage is needed
delete_raw_video = True 


# locks
filewritingGazeLock = threading.Lock()
filewritingSnapshotLock = threading.Lock()

# TODO: don't think I actually use this...
openFaceVideoLock = threading.Lock()
# 

# constants
GAZE_BUFFER_SIZE = 10000
COMMUNICATION_PORT_WITH_EYE_MIND = 5000
N_CONNECTION_TRIALS = 10
#############

# globals
mt = None
GAZE_ATTRIBUTES = [
    ('device_time_stamp', 1),
    #  ('left_gaze_origin_validity',  1),
    #   ('right_gaze_origin_validity',  1),

    #  ('left_gaze_origin_in_user_coordinate_system',  3),
    #  ('right_gaze_origin_in_user_coordinate_system',  3),

    #  ('left_gaze_origin_in_trackbox_coordinate_system',  3),
    #  ('right_gaze_origin_in_trackbox_coordinate_system',  3),

    ('left_gaze_point_validity',  1),
    ('right_gaze_point_validity',  1),

    ('left_gaze_point_on_display_area',  2),
    ('right_gaze_point_on_display_area',  2),

     ('left_pupil_validity',  1),
     ('right_pupil_validity',  1),

    ('left_pupil_diameter',  1),
    ('right_pupil_diameter',  1),

    ('left_gaze_origin_in_user_coordinate_system',  3),
    ('right_gaze_origin_in_user_coordinate_system',  3)
]
#############


# variables to be reset at each (ET) setup
gazeData = []
gazeFullData = None
snapshotsFullData = None

gazeDataFilename = ""
snapshotsContentDataFilename = ""

filewritingGazeThreads = []
filewritingSnapshotThreads = []

currentSnapshotId = -1
currentSnapshotTimestamp = -1
currentQuestion = ""

isETready = 0

xScreenDim =  -1 # in pixel
yScreenDim =  -1 # in pixel

isETstarted = False

# Variables to 0-index EyeMind timestamps
timestamp_offset = None 
is_first_call = True
# 

###### ######  ###### OPEN FACE INTEGRATION ###### ###### ###### ###### ######
camera = None
vid_writer = None
video_thread = None
video_is_running = threading.Event()

server_directory = os.getcwd()
root_directory = os.path.dirname(server_directory)
openFace_directory = os.path.join(root_directory, 'OpenFace')

processed_videos_directory = os.path.join(root_directory, 'EyeMindApp', 'outputData', 'OpenFace')

def find_camera():
    """
    Finds and connects to the first available camera.

    Returns:
        bool: True if a camera is found and successfully connected, False otherwise.
    """
    global camera

    # Looking for camera
    for i in range(N_CONNECTION_TRIALS):
        cam = cv2.VideoCapture(0)

        if cam.isOpened():
            print("Camera found and successfully connected.")
            camera = cam
            return True
        else:
            time.sleep(2)
            cam.release()

    print(f"No cameras found after {i} attempts.")
    return False


def start_video_recording(output_path):
    """
    Starts video recording in a separate thread and saves it to the specified output file.
    To finish recording and save the video, call 'end_video_recording'.

    Args:
        output_path (str): The full path, including the filename, where the video recording will be saved.
    """

    global camera, vid_writer, video_thread

    # Video properties
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30 #TODO change later via ffmpeg  /  add camera default fps?

    # Initialize VideoWriter
    vid_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    if not vid_writer.isOpened():
        print("Failed to open VideoWriter.")
        return

    # TODO: make sure variable framerate camera is taken into consideration

    # Defining recording loop
    def recording_loop():
        print("Video recording started...")
        frame_count = 0
        while video_is_running.is_set():
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab frame.")
                break
            vid_writer.write(frame)
            frame_count += 1
        print(f"Video recording stopped. Total frames recorded: {frame_count}")

    # start video thread using the recording loop
    video_is_running.set()
    video_thread = threading.Thread(target=recording_loop, daemon=True) #TODO: unsure if we need daemon thread
    video_thread.start()


def end_video_recording():
    """
    Stops and saves video the recording, and releases allocated resources.
    """
    global camera, vid_writer, video_thread

    # Once the video thread
    if video_thread and video_is_running.is_set():
        video_is_running.clear()
        video_thread.join()  

    # release camera resource
    if camera:
        camera.release()
        camera = None

    # release video writer resource
    if vid_writer:
        vid_writer.release()
        vid_writer = None

    # close any open OpenCV windows
    cv2.destroyAllWindows()
    print("Video recording resources released.")


def perform_openFace_analysis(raw_video, output_path):
    """
    Runs OpenFace analysis on a specified video file and saves the output to a specified directory.

    Args:
        raw_video (str): The full path to the video file to be analyzed using the OpenFace software.
        output_path (str): The directory path to where the processed material should be saved.
    """
    # Feature parameters to include in OpenFace processing
    # TODO: might change these parameters depending on what we need from OpenFace
    # (see https://github.com/TadasBaltrusaitis/OpenFace/wiki/Command-line-arguments)
    features = [
    "-2Dfp",       # 2D landmarks
    "-3Dfp",       # 3D landmarks
    "-pdmparams",  # Rigid and non-rigid shape parameters
    "-pose",       # Head pose (location and rotation)
    "-aus",        # Facial Action Units
    "-gaze",       # Gaze and related features
    # "-tracked",    # video showing OpenFace analysis
    "-hogalign"    # HOG features
    ]

    # Construct the command for OpenFace feature extraction
    # TODO: changeto FaceLandmarkVidMulti to be able to process multiple faces?
    command = (
    f".\\FeatureExtraction.exe -f \"{raw_video}\" -out_dir \"{output_path}\" {' '.join(features)}"
    )

    # Change working directory to the OpenFace folder to execute the command
    os.chdir(openFace_directory)

    # Run the PowerShell command
    try:
        # Execute the OpenFace command via PowerShell
        subprocess.run(["powershell", "-Command", command], check=True)
        print("OpenFace analysis completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during OpenFace analysis: {e}")
    finally:
        # Ensure we return to the root directory
        os.chdir(server_directory)

###### ######  ###### END OF OPEN FACE INTEGRATION CODE ###### ###### ###### ###### ######


def find_eyeTracker():
    """
    Finds the first available connected eye-tracker.

    Returns:
        bool: True if the eye-tracker is found, False otherwise.
    """
    global mt

    # looking for eye-tracker
    ft = []
    for i in range (0,N_CONNECTION_TRIALS):
        ft = tr.find_all_eyetrackers()
        if len(ft) == 0:
            print("No Eye Trackers found! Trying again ...")
            time.sleep(2)
        else:
            break

    # Pick first eye-tracker
    if len(ft)>0:
        mt = ft[0]
        print("Found Tobii Tracker at '%s'" % (mt.address))
        return True
    else:
        print("No Eye Trackers found!")
        return False


def start_gaze_tracking():
    """
    Start gaze tracking. Subscribes to the tobii data stream with the dictionary setting enabled,
    using the callback function 'gaze_data_callback'
    """
    global isETstarted
    mt.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    isETstarted = True


def end_gaze_tracking():
    """
    Ends gaze tracking. Unsubscribes from the tobii data stream. 
    """
    mt.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)


def gaze_data_callback(gaze_data):
    """
    Logs selected data attributes from the tobii data stream periodically. 

    Args:
        gaze_data (object): A gaze data object with many attributes referring to gaze characteristics.
    """

    eventSource = "eye-tracker"

    try:
        # global last_report
        # global N
        global gazeData

        # sts = gaze_data['system_time_stamp'] / 1000000.


        # if sts > last_report + 5:
        #     sys.stdout.write("%14.3f: %10d packets\r" % (sts, N))
        #     last_report = sts
        # N += 1

        # if not in testmode: call unpack_gaze_data()
        # if in testmode: d = gaze_data    i.e. uses raw gaze data
        d = unpack_gaze_data(gaze_data) if not testMode else gaze_data

        #print(d)
        timestamp = d[0]

        validLeft = d[1]
        validright = d[2]

        leftXRatio = d[3]
        leftYRatio = d[4]

        rightXRatio = d[5]
        rightYRatio = d[6]

        leftPupilValidity = d[7]
        rightPupilValidity = d[8]

        leftPupilDiameter = d[9]
        rightPupilDiameter = d[10]

        leftXOrigin = d[11]
        leftYOrigin = d[12]
        leftZOrigin = d[13]

        rightXOrigin = d[14]
        rightYOrigin = d[15]
        rightZOrigin = d[16]



        entry = {
            "Timestamp": timestamp,

            "validLeft": validLeft,
            "validRight": validright,

            "leftXRatio": leftXRatio,
            "leftYRatio": leftYRatio,
            "rightXRatio": rightXRatio,
            "rightYRatio": rightYRatio,

            "leftPupilValidity": leftPupilValidity,
            "rightPupilValidity": rightPupilValidity,

            "leftPupilDiameter": leftPupilDiameter,
            "rightPupilDiameter": rightPupilDiameter,

            "leftXOrigin": leftXOrigin,
            "leftYOrigin": leftYOrigin,
            "leftZOrigin": leftZOrigin,

            "rightXOrigin": rightXOrigin,
            "rightYOrigin": rightYOrigin,
            "rightZOrigin": rightZOrigin,

            "snapshotId": currentSnapshotId,
            #"currentSnapshotTimestamp": currentSnapshotTimestamp,

            "currentQuestion": currentQuestion,

            "eventSource": eventSource,

            "systemTimestamp": time.time_ns()
            }

        gazeData.append(entry)

        storeGazeDataPeriodically()

    except:
        print("Error in callback: ")
        print(sys.exc_info())


# Helper function for gaze_data_callback()
def storeGazeDataPeriodically():
    """
    Periodically stores gaze data asynchropnously to file.

    This function handles the storage of gaze data to a file in a separate thread. The data is stored once the number of gaze data entries reaches a specified threshold.
    """
    global gazeData

    # if the length of gazeData exceeds the GAZE_BUFFER_SIZE
    if len(gazeData)>=GAZE_BUFFER_SIZE:
        print("storing gaze data ...")

        # make a deep copy of the first chunk of gazeData [:GAZE_BUFFER_SIZE]. 
        # This strategy avoid issues when gazeData is being updated externally from logQuestionData() or logClickData()
        tempData = copy.deepcopy(gazeData[:GAZE_BUFFER_SIZE])
        
        # remove the copied fragment from gazeData
        gazeData = gazeData[GAZE_BUFFER_SIZE: ]

        # start a thread responsible for appending tempData to gazeDataFilename
        thread = threading.Thread(target=appendGazesToFile, args=(tempData, ))
        thread.start()
        filewritingGazeThreads.append(thread)


# Helper function for StoreGazeDataPeriodically()
def appendGazesToFile(tempData):
    """
    Appends gaze data to a file in a separate thread, and handles file creation if necessary.

    Args:
        tempData (object): A fragment of gaze data to be appended to the file.
    """

    # filewritingGazeLock is a lock, making the load and the writing to the file thread-safe
    with filewritingGazeLock:
        print("periodic writing of gaze data to file started")

        try:
            file = open(gazeDataFilename, 'r+b')
            data = pickle.load(file)
            print("loaded data len",len(data))
            data.extend(tempData)
            print("new data len",len(data))
            file.seek(0)
            file.truncate()
            pickle.dump(data, file)
            file.close()

        except (EOFError, OSError) :
            file = open(gazeDataFilename, 'w+b')
            print("Fresh gazes file")
            print("tempData len",len(tempData))
            pickle.dump(tempData, file)
            file.close()

        print("periodic writing to file ended")



def logFullSnapshot(snapshotContent):
    """
    Logs the snapshot with all its details.

    Args:
        snapshotContent (object): The snapshot object containing all relevant details.
    """

    # start a thread responsible for appending snapshotContent to snapshotsContentDataFilename
    thread = threading.Thread(target=appendSnapshotContentToFile, args=(snapshotContent, ))
    thread.start()
    filewritingSnapshotThreads.append(thread)


# Helper function for LogFullSnapshot()
def appendSnapshotContentToFile(snapshotContent):
    """
    Appends snapshot content to a file.

    Args:
        snapshotContent (object): The snapshot object to be appended.
    """

    # filewritingSnapshotLock is a lock, makking the load and the writing to the file thread-safe
    with filewritingSnapshotLock:
        print("append snapshots content data to snapshots file started")

        try:
            file = open(snapshotsContentDataFilename, 'r+b')
            data = pickle.load(file)
            print("loaded data len",len(data))
            data[snapshotContent["id"]] = snapshotContent
            print("new data len",len(data))
            file.seek(0)
            file.truncate()
            pickle.dump(data, file)
            file.close()
        except (EOFError, OSError):
            file = open(snapshotsContentDataFilename, 'w+b')
            print("Fresh snapshot file")
            data = {}
            data[snapshotContent["id"]] = snapshotContent
            print("data len",len(data))
            pickle.dump(data, file)
            file.close()

        print("append snapshots content data to snapshots file finished")


def logQuestionData(questionTimestamp,questionEventType,questionText,questionAnswer,questionPosition,questionID):
    """
    Appends question events to gazeData.

    Args:
        questionTimestamp (str): Timestamp of the event.
        questionEventType (str): Type of question event (e.g., questionOnset, questionOffset).
        questionText (str): The text of the question.
        questionAnswer (str): The answer text.
        questionPosition (int): Position of the question (e.g., nextQuestionId).
        questionID (str): ID of the question.
    """
    # TODO: check if timestamp is 0-indexed

    global gazeData

    eventSource = "questionnaire"

    entry = { "questionTimestamp" : questionTimestamp,
                "questionEventType" : questionEventType,
                "questionText" : questionText,
                "questionAnswer" : questionAnswer,
                "questionPosition" : questionPosition,
                "questionID": questionID,
                "eventSource": eventSource,
                "systemTimestamp": time.time_ns()
                }

    gazeData.append(entry)


def logClickData(clickTimestamp,clickedElement):
    """
    Appends a click event to gazeData.

    Args:
        clickTimestamp (str): Timestamp when the click was registered.
        clickedElement (str): Identifier of the clicked element.
    """
    # TODO: check if timestamp is 0-indexed

    global gazeData

    eventSource = "clickStream"

    entry = {   "clickTimestamp" : clickTimestamp,
                "clickedElement" : clickedElement,
                "eventSource": eventSource,
                "systemTimestamp": time.time_ns()
                }

    gazeData.append(entry)


# I modified the original function, so that it now is 0-indexed instead of using the inbuilt tobii timestamp
def unpack_gaze_data(gaze_data):
    """
    Unpacks raw gaze data, adjusting the timestamp offset and flattening tuple values.

    Args:
        gaze_data (dict): the default tobii data stream.

    Returns:
        list: A flat list of processed gaze data values.
    """

    global timestamp_offset, is_first_call 

    # Mark timestamp_offset
    if is_first_call:
        timestamp_offset = gaze_data['device_time_stamp']
        is_first_call = False

    # Iterate through selected GAZE_ATTRIBUTES, and creating a flattened list
    x = []
    for attr_info in GAZE_ATTRIBUTES:
        attr = attr_info[0]
        value = gaze_data[attr]
        
        # Subtract timestamp offset
        if attr == 'device_time_stamp':
            value -= timestamp_offset

        if isinstance(value, tuple):
            x += list(value)
        else:
            x.append(value)
    return x


def getGazes():
    """
    Processes, saves, and retrieves gaze data.

    Synchronizes file-writing threads, and appends any remaining in-memory gaze data to the data file. 
    Processes and cleans the data. Then saves it as a csv file to out/logs/.

    Returns:
        object: A gaze data frame containing the gaze data.
    """

    # wait for all threads in filewritingGazeThreads to finish
    for thread in filewritingGazeThreads:
        thread.join()

    # append the data still in memory to the file
    if len(gazeData)>0:
        appendGazesToFile(gazeData)


    # open gazeDataFilename
    file = open(gazeDataFilename, 'rb')
    # load its content i.e., gazeData
    data = pickle.load(file)


    # for stress simulation:
    # data = data*100

    gazeDataFrame = pd.DataFrame(data)


    # sort gazeDataFrame by Timestamp
    gazeDataFrame.sort_values(by=['Timestamp'])

    now = int( time.time() )


    gazeDataFrame["Timestamp"] = gazeDataFrame["Timestamp"]/1000  #convert from micro to milliseconds
    # for timestamp simulation: gazeDataFrame["Timestamp"] = 325905.354 + (gazeDataFrame.index *  8.348)

    gazeDataFrame["leftX"] = gazeDataFrame["leftXRatio"]*xScreenDim
    gazeDataFrame["leftY"] = gazeDataFrame["leftYRatio"]*yScreenDim

    gazeDataFrame["rightX"] = gazeDataFrame["rightXRatio"]*xScreenDim
    gazeDataFrame["rightY"] = gazeDataFrame["rightYRatio"]*yScreenDim

    gazeDataFrame["XRatio"] = gazeDataFrame[["leftXRatio","rightXRatio"]].mean(axis=1)
    gazeDataFrame["YRatio"] = gazeDataFrame[["leftYRatio","rightYRatio"]].mean(axis=1)

    #gazeDataFrame["x"] = gazeDataFrame["XRatio"]*xScreenDim
    #gazeDataFrame["y"] = gazeDataFrame["YRatio"]*yScreenDim

    gazeDataFrame["leftDistance"] = gazeDataFrame["leftZOrigin"]
    gazeDataFrame["rightDistance"] = gazeDataFrame["rightZOrigin"]


    gazeDataFrame.to_csv("out/logs/EyeMindFinalGazeData"+str(now)+".csv")

    # version to send back to EyeMind

    # Set negative (invalid) leftX, leftY, rightX, rightY to nan
    gazeDataFrame.loc[gazeDataFrame["leftX"] < 0, "leftX"] = np.nan
    gazeDataFrame.loc[gazeDataFrame["leftY"] < 0, "leftY"] = np.nan
    gazeDataFrame.loc[gazeDataFrame["rightX"] < 0, "rightX"] = np.nan
    gazeDataFrame.loc[gazeDataFrame["rightY"] < 0, "rightY"] = np.nan


    # Set leftX, rightX to nan if value > xScreenDim
    gazeDataFrame.loc[gazeDataFrame["leftX"] > xScreenDim, "leftX"] = np.nan
    gazeDataFrame.loc[gazeDataFrame["rightX"] > xScreenDim, "rightX"] = np.nan


    # Set leftY or rightY to nan if value > yScreenDim
    gazeDataFrame.loc[gazeDataFrame["leftY"] > yScreenDim, "leftY"] = np.nan
    gazeDataFrame.loc[gazeDataFrame["rightY"] > yScreenDim, "rightY"] = np.nan


    # rounding and dropping uncessary columns for the data to be send to EyeMind (the full data was already stored) (rounding is similar to iMotions)
    # round
    gazeDataFrame = gazeDataFrame.round({
        'leftX': 0,
        'leftY': 0,
        'rightX': 0,
        'rightY': 0,
     })

    # compute x and y with rounded data
    gazeDataFrame["x"] = gazeDataFrame[["leftX","rightX"]].mean(axis=1)
    gazeDataFrame["y"] = gazeDataFrame[["leftY","rightY"]].mean(axis=1)

    # round x and y after recomputation
    gazeDataFrame = gazeDataFrame.round({
        'x': 1,
        'y': 1,
     })

    # drop uncessary columns
    gazeDataFrame = gazeDataFrame.drop(columns=[
        'leftXOrigin', 'leftYOrigin','leftZOrigin','rightXOrigin','rightYOrigin','rightZOrigin',
        'leftXRatio','leftYRatio','rightXRatio','rightYRatio','XRatio','YRatio','systemTimestamp' ])

    return gazeDataFrame


def getSnapshotsContent():
    """
    Retrieves the content of the snapshots.

    Returns:
        object: The snapshots content.
    """

    # wait for all threads in filewritingSnapshotThreads to finish
    for thread in filewritingSnapshotThreads:
        thread.join()

    # try except depending on whether snapshotsContentDataFilename was created on not yet. 
    # If the file was not created, this means there are no snapshots
    try:
        # open snapshotsContentDataFilename
        file = open(snapshotsContentDataFilename, 'rb')
        # load its content i.e., snapshotsContent
        data = pickle.load(file)
        # close file
        file.close()

    except OSError:
        data = None

    return data


######################## for testing purpose ###############################

def processMockGazeData(gazes):

    for gazePoint in gazes:
        print(gazePoint)
        gaze_data_callback(gazePoint)

########################################################################


######################## main control-flow

# find equipment if not in testmode
if testMode:
    isETready = 1
else:
    # Determine requirements based on uf OpenFace is enabled
    trackers_ready = find_eyeTracker()
    camera_ready = find_camera() if openFaceMode else True

    # Set readiness or exit if conditions are not met
    if trackers_ready and camera_ready:
        isETready = 1
    else:
        exit()




app = Flask(__name__)

@app.route('/BPMeyeMind', methods = ['POST'])
def process():
    global gazeData
    global gazeFullData
    global snapshotsFullData
    global gazeDataFilename
    global snapshotsContentDataFilename
    global filewritingGazeThreads
    global filewritingSnapshotThreads
    global currentSnapshotId
    global currentSnapshotTimestamp
    global currentQuestion
    global isETready
    global xScreenDim
    global yScreenDim
    # global last_report
    # global N
    global isETstarted

    # OpenFace Variables
    global unprocessedVideoFilename

    data = request.get_json()

    print("-----------------------new data received -----------------")

    if data['action']=='setup':
        print(data)
        print("setup received")

        # reset global variables
        gazeData = []
        gazeFullData = None
        snapshotsFullData = None
        cTimestamp = "t"+str(int( time.time() ))
        gazeDataFilename = "out/logs/EyeMindTemporalGazeData_"+cTimestamp+".bem"
        snapshotsContentDataFilename = "out/logs/EyeMindTemporalSnapshotsContentData_"+cTimestamp+".bem"
        filewritingGazeThreads = []
        filewritingSnapshotThreads = []

        # the location and name of OpenFace unprocessed recording files
        unprocessedVideoFilename = server_directory + "\\out\\logs\\" + "video" + cTimestamp + ".mp4" 

        currentSnapshotId = -1
        currentSnapshotTimestamp = -1
        currentQuestion = ""
        # last_report = 0
        # N = 0
        isETstarted = False

        # input new data
        xScreenDim = int(data['xScreenDim'])
        yScreenDim = int(data['yScreenDim'])

        # start gaze tracking if you are not in a test mode
        if not testMode:
            start_gaze_tracking()

            if openFaceMode:
                start_video_recording(unprocessedVideoFilename) 
        else:
            isETstarted = True

        # TODO: add some logging of OpenFace / recording
        
        responseMsg = {
            "gazeData": gazeData,
            "gazeFullData": gazeFullData,
            "snapshotsFullData": snapshotsFullData,
            "cTimestamp": cTimestamp,
            "gazeDataFilename": gazeDataFilename,
            "snapshotsContentDataFilename": snapshotsContentDataFilename,
            "currentSnapshotId": currentSnapshotId,
            "currentSnapshotTimestamp": currentSnapshotTimestamp,
            "filewritingGazeThreads": filewritingGazeThreads,
            "filewritingSnapshotThreads": filewritingSnapshotThreads,
            "currentQuestion": currentQuestion,
            "isETstarted": isETstarted,
            "xScreenDim": xScreenDim,
            "yScreenDim": yScreenDim,
            "isETready": isETready,
            "response": "OK"
        }

        return responseMsg

    elif data['action']=='addSnapshot' and isETstarted:
        print(data)
        print("snapshot id received")
        currentSnapshotId = data['id']
        currentSnapshotTimestamp = data['timestamp']

        responseMsg = {
            "currentSnapshotId": currentSnapshotId,
            "currentSnapshotTimestamp": currentSnapshotTimestamp,
            "response": "OK"
        }

        return responseMsg

    elif data['action']=='addQuestionEvent' and isETstarted:
        print(data)
        print("question event received")
        questionTimestamp = data['questionTimestamp']
        questionEventType = data['questionEventType']
        questionText = data['questionText']
        questionAnswer = data['questionAnswer']
        questionPosition = data['questionPosition']
        questionID = data['questionID']

        if questionEventType=="questionOnset":
            currentQuestion = data['questionID']
        elif questionEventType=="questionOffset":
            currentQuestion = ""

        logQuestionData(questionTimestamp,questionEventType,questionText,questionAnswer,questionPosition,questionID)

        responseMsg = {
            "response": "OK",
        }
        return responseMsg

    elif data['action']=='addClickEvent' and isETstarted:
        print(data)
        print("click event received")
        clickTimestamp = data['clickTimestamp']
        clickedElement = data['clickedElement']

        logClickData(clickTimestamp,clickedElement)

        responseMsg = {
            "response": "OK",
        }
        return responseMsg

    elif data['action']=='logFullSnapshot' and isETstarted:
        print("snapshot content received")
        #print(data['content']["boundingClientRect"])
        logFullSnapshot(data['content'])

        responseMsg = {
            "response": "OK",
        }
        return responseMsg


    elif data['action'] == 'PrepareGazeDataAndInitiateTransfer' and isETstarted:
        print(data)
        print("preparing data for transfer")

        if not testMode:
            # stop the data collection
            end_gaze_tracking() 

            # handle OF analysis
            if openFaceMode:
                end_video_recording() 
                perform_openFace_analysis(unprocessedVideoFilename, processed_videos_directory) # process the video recording using OpenFace
                
                if delete_raw_video:
                    os.remove(unprocessedVideoFilename)

        gazeFullData = getGazes()
        snapshotsFullData = getSnapshotsContent()
        output = {"gazeDataSize" : len(gazeFullData),
                  "snapshotsSize": len(snapshotsFullData)
                  }
        print("gaze data ready to send")
        return output

    elif data['action'] == 'getDataFragment' and isETstarted:
        print(data)
        print("getting a data fragement in range %s, %s" % (data['start'], data['end']) )

        return gazeFullData.iloc[data['start']:data['end']].to_json(orient = 'records')

    elif data['action'] == 'getSnapshotFragment' and isETstarted:
        print(data)
        print("getting a snapshot fragement in range %s, %s" % (data['start'], data['end']) )

        return {k: snapshotsFullData[k] for k in list(snapshotsFullData)[data['start']:data['end']]}


    ###########FOR TESTING PURPOSE#############################
    elif data['action'] == 'mockGazeData' and isETstarted:
        #print(data)
        processMockGazeData(data['content'])
        responseMsg = {
            "response": "OK",
        }
        return responseMsg

    elif data['action'] == 'clear' and isETstarted:
        print(data)
        gazeData = []
        responseMsg = {
            "response": "OK",
        }
        return responseMsg

    elif data['action'] == 'mockRecording' and isETstarted:
        print(data)
        gazeDataFilename = data['gazeDataFilename']
        snapshotsContentDataFilename = data['snapshotsContentDataFilename']

        responseMsg = {
            "response": "OK",
        }
        return responseMsg

    ############################################################

    return ""

if __name__ == "__main__":
    #app.run(port=5000)
    serve(app, host="0.0.0.0", port=COMMUNICATION_PORT_WITH_EYE_MIND)


############################################################


