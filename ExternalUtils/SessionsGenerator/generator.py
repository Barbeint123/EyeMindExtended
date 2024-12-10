from utils import  isDirectoryEmpty, createSessions

experimentConfig = {

	"rooms": ["A","M"], #eye-tracking rooms where parrallel sessions will occur
	"participantsPerRoom": 50, #number of participant sessions to be created in each room folder
	"ParticipantsIdPrefix": "P", #prefix used in participant id
	"participantsIdSeed":1, #seed from which to start when assigning ids to participants
	"shuffleStartTaskIndex":2, #shuffle tasks list starting from startIndex=2 
	"questionsPerTask": 1, #number of questions per task. Note that the questions within the tasks are not randomized. Only the tasks are randomized

	"template" :  '../../Experiment-data/template.json', #template file path
	"outDirectory": "../../Experiment-data/Participant-data/", #output directory
	"linkingSubProcessesModes": ["no","newTab","withinTab"] # ["no","newTab","withinTab"], linking modes accronyms for no-support, symoblic links, breadcrumb respectively
}

# check that experimentConfig["outDirectory"] is empty
if not isDirectoryEmpty(experimentConfig["outDirectory"]):
	print(f'Error: "directory {experimentConfig["outDirectory"]}"" is not empty or does not contain an empty README.md file')
	exit();

# create sessions
createSessions(experimentConfig)
