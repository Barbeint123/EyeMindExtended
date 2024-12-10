import unittest
from utils import write_json, read_json, suffleTasksStartingFromIndex
import os
import pandas as pd
import re
import numpy as np

# experimentConfig = {

# 	"rooms": ["A","M"], #eye-tracking rooms where parrallel sessions will occur (e.g., Amine room A, Maike room M)
# 	"participantsPerRoom": 50, #number of participant sessions to be created in each room folder
# 	"ParticipantsIdPrefix": "P", #prefix used in participant id
# 	"participantsIdSeed":1, #seed from which to start when assigning ids to participants
# 	"shuffleStartIndex":2, #shuffle questions list starting from startIndex=2 (to keep the amazon smart process questions first)


# 	"template" :  '../../Experiment-data/template.json', #template file path
# 	"outDirectory": "../../Experiment-data/Participant-data/", #output directory
# 	"linkingSubProcessesModes": ["no","newTab","withinTab"] #linking modes accronyms for no-support, symoblic links, breadcrumb respectively
# }

experimentConfig = {

	"rooms": ["S","K"], #eye-tracking rooms where parrallel sessions will occur
	"participantsPerRoom": 50, #number of participant sessions to be created in each room folder
	"ParticipantsIdPrefix": "P", #prefix used in participant id
	"participantsIdSeed":1, #seed from which to start when assigning ids to participants
	"shuffleStartTaskIndex":2, #shuffle tasks list starting from startIndex=2
	"questionsPerTask": 3, #number of questions per task. Note that the questions within the tasks are not randomized. Only the tasks are randomized

	"template" :  '../../Experiments-data/bpmn-fba-2023/template.json', #template file path
	"outDirectory": "../../Experiments-data/bpmn-fba-2023/Participant-data/", #output directory
	"linkingSubProcessesModes": ["no"] # ["no","newTab","withinTab"], linking modes accronyms for no-support, symoblic links, breadcrumb respectively
}

###
 # Title: Tests
 #
 # Description: test class
 #
 # Additional notes: none
 #
class Tests(unittest.TestCase):

	###
	# Title: test shuflling
	#
	# Description: test the suffling
	#
	def test_shuflling(self):

		print("test_shuflling")

		inFilePath =  'test-data/test-session2.json'

		# read json
		session = read_json(inFilePath)

		#number of loaded questions
		nLoadedQuestions = len(session["questions"])

		# randomization start index
		randStartIndex = (experimentConfig['shuffleStartTaskIndex']*experimentConfig['questionsPerTask'])

		#non randomized questions and tasks to questions
		nonRandomizedQuestions = session["questions"][0:randStartIndex]
		questionsToRandomize = session["questions"][randStartIndex:]

		#list with question ids in their original order
		questionIdsInOriginalOrder = [question["id"] for question in session["questions"]] 

		#shuffle questions starting from taskStartIndex 
		session["questions"] = suffleTasksStartingFromIndex(session["questions"],taskStartIndex=experimentConfig['shuffleStartTaskIndex'],questionsPerTask=experimentConfig['questionsPerTask'])

		#list with question ids in new order
		questionIdsInNewOrder = [question["id"] for question in session["questions"]]

		#devide questions into tasks
		taskSets = np.split(np.array(session["questions"]),len(np.array(session["questions"]))/experimentConfig['questionsPerTask']) 

		#asserts
		#number of questions did not change
		self.assertEqual(len(session["questions"]), nLoadedQuestions)
		#first (experimentConfig['shuffleStartTaskIndex']*experimentConfig['questionsPerTask'])) questions did remain at the same order
		self.assertEqual(session["questions"][0:randStartIndex], nonRandomizedQuestions)
		#remaining questions come at different order
		self.assertNotEqual(questionIdsInNewOrder[randStartIndex:], questionIdsInOriginalOrder[randStartIndex:])
		#the questions within the tasks are not randomized
		for task in taskSets:
			for idx, question in enumerate(task):
				if idx<len(task)-1:
					self.assertEqual(int(task[idx]["id"])+1, int(task[idx+1]["id"]))


###
	# Title: test generated sessions
	#
	# Description: test generated sessions
	#
	def test_generated_sessions(self):

		print("test_generated_sessions")


		# get questions of the template
		template = read_json(experimentConfig["template"])

		#list with question ids in their original template order
		questionIdsInOriginalOrder = [question["id"] for question in template["questions"]]

		# randomization start index
		randStartIndex = (experimentConfig['shuffleStartTaskIndex']*experimentConfig['questionsPerTask'])-1

		# iterate the session files in outDirectory
		for room in experimentConfig['rooms']:
			for subdir, dirs, files in os.walk(f'{experimentConfig["outDirectory"]}/{room}/'):
				for file in files:
					fileName = os.path.join(subdir, file)
					print(f'reading {fileName}')
					if fileName != "out/README.md":
						session = read_json(fileName)
						#list with question ids in new session order
						questionIdsInNewOrder = [question["id"] for question in session["questions"]]

						#devide questions into tasks
						taskSets = np.split(np.array(session["questions"]),len(np.array(session["questions"]))/experimentConfig['questionsPerTask']) 

						#asserts
						#number of questions is the same as the one in the template
						self.assertEqual(len(session["questions"]), len(template["questions"]))
						#first (experimentConfig['shuffleStartTaskIndex']*experimentConfig['questionsPerTask'])) questions did remain the same
						for index, question in enumerate(session["questions"][0:randStartIndex]):
							self.assertEqual(question["id"], template["questions"][index]["id"])
							self.assertEqual(question["question"], template["questions"][index]["question"])
							self.assertEqual(question["type"], template["questions"][index]["type"])
							self.assertEqual(question["options"], template["questions"][index]["options"])
							self.assertEqual(question["model-group"], template["questions"][index]["model-group"])
						#remaning questions come at different order
						self.assertNotEqual(questionIdsInNewOrder[randStartIndex:], questionIdsInOriginalOrder[randStartIndex:])
						#linkingSubProcessesMode in file name matches linkingSubProcessesModes in the session config
						linkingSubProcessesModeFromFileName = re.search('-(.+?).json',file).group(1)
						self.assertEqual(linkingSubProcessesModeFromFileName, session["linkingSubProcessesMode"])
						#the questions within the tasks are not randomized
						for task in taskSets:
							for idx, qs in enumerate(task):
								if idx<len(task)-1:
									self.assertEqual(int(task[idx]["id"])+1, int(task[idx+1]["id"]))


# for now, tests should be executed in independent runs
def suite():
    suite = unittest.TestSuite()
    suite.addTest(Tests('test_shuflling'))
    suite.addTest(Tests('test_generated_sessions'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

