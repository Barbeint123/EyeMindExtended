import json
import random
import os
import copy
import numpy as np


def isDirectoryEmpty(path):
	if len(os.listdir(path) ) == 1 and os.path.isfile(f'{path}/README.md'):
		return True
	return False


def write_json(data,path):
	with open(path, "w") as outFile:
		json.dump(data, outFile)

def read_json(path):
	with open(path) as inFile:
		return json.load(inFile)

def suffleTasksStartingFromIndex(data,taskStartIndex,questionsPerTask):

	# convert data to np.array
	data = np.array(data)
	# organize questions per task 
	data = np.split(data,len(data)/questionsPerTask) 
	#start by copying the data that should not be shuffled
	new_data = copy.deepcopy(data[0:taskStartIndex])
	#copy the remaining data
	remaining_data = copy.deepcopy(data[taskStartIndex:])
	#suffle remaining data
	random.shuffle(remaining_data) 
	#extend new_data with suffled remaining_data
	new_data.extend(remaining_data)	

	return list(np.concatenate(new_data).flat)


def createSessions(experimentConfig):

	# read template
	template = read_json(experimentConfig["template"])

	# iterate over rooms
	for room in experimentConfig["rooms"]:
		# create room directory 
		roomPath = f'{experimentConfig["outDirectory"]}/{room}/'
		os.makedirs(roomPath,mode=0o777)
		# iterate over participants
		for participant in range(0,experimentConfig["participantsPerRoom"]):
			#make new session from template
			newSession = copy.deepcopy(template)
			#shuffle newSession["questions"] list starting from a given index 
			newSession["questions"] = suffleTasksStartingFromIndex(newSession["questions"],taskStartIndex=experimentConfig["shuffleStartTaskIndex"], questionsPerTask=experimentConfig['questionsPerTask'])	
			#Assign linkingSubProcessMode
			newSession["linkingSubProcessesMode"] = experimentConfig["linkingSubProcessesModes"][participant % len(experimentConfig["linkingSubProcessesModes"])]
			# export
			exportName = f'{experimentConfig["ParticipantsIdPrefix"]}{experimentConfig["participantsIdSeed"]+participant}-{newSession["linkingSubProcessesMode"]}'
			os.makedirs(roomPath+room+exportName,mode=0o777)
			outFile = f'{roomPath}{room}{exportName}/{exportName}.json'
			print(f'outFile: {outFile}')
			#save file
			write_json(newSession,outFile)