# Expert System
# Monica Kuo (mdk6jd); Ouyang De (do5xb)

import textwrap

# create data structures
# in the form {"variable" : ["value", "-R/-L"]}
variableDefinitions = {}
# in the form {"variable" : "true/false"}
facts = {}
rules = []

def expertSystem():

	while(True):

		# get input 
		commandString = input()
		# parse input
		commandList = commandString.split(' ')
		# call correct function
		if(commandList[0] == "Teach"):
			if((commandList[1] == "-R") or (commandList[1] == "-L")):
				teachVariableDefinition(commandList)
			if(commandList[1] in variableDefinitions.keys() and (commandList[3] == "true" or commandList[3] == "false")):
				teachTruth(commandList)

		if(commandList[0] == "List"):
			listCommand()
		if(commandList[0] == "Learn"):
			learnCommand()
		if(commandList[0] == "Query"):
			queryCommand()
		if(commandList[0] == "Why"):
			whyCommand()

		# print(commandList)
		

def teachVariableDefinition(commandList):
	# get information
	argument = commandList[1]
	variable = commandList[2]
	value = ' '.join(commandList[4::])
	# add information to variableDefinitions
	variableDefinitions[variable] = [value, argument]

def teachTruth(commandList):
	# get information
	variable = commandList[1]
	truth = commandList[3]
	typeOfVariable = variableDefinitions[variable][1]
	# this command can only be used with root variables
	if(typeOfVariable == "-R"):
		facts[variable] = truth
	else:
		print("Error: Cannot set a learned variable directly")



def listCommand():

	print("Root Variables:")
	for variable, definition in variableDefinitions.items():
		if(definition[1] == "-R"):
			print(' '*5 + variable + ' = ' + definition[0])
	print()

	print("Learned Variables:")
	for variable, definition in variableDefinitions.items():
		if(definition[1] == "-L"):
			print(' '*5 + variable + ' = ' + definition[0])
	print()

	print("Facts:")
	for variable, fact in facts.items():
		if(fact == "true"):
			print(' '*5 + variable)
	print()

	print("Rules:")
	for rule in rules:
		print(" "*5 + rule)
	print()


def learnCommand():
	print("in learnCommand")

def queryCommand():
	print("in queryCommand")

def whyCommand():
	print("in whyCommand")

if __name__ == "__main__":
	expertSystem()