# Expert System
# Monica Kuo (mdk6jd); Ouyang De (do5xb)

import textwrap

# create data structures
# in the form {"variable" : ["value", "-R/-L", "true/false"]}
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
			if((commandList[2]) == "->"):
				teachNewRule(commandList)

		if(commandList[0] == "List"):
			listCommand()

		if(commandList[0] == "Learn"):
			learnCommand()

		if(commandList[0] == "Query"):
			queryCommand()

		if(commandList[0] == "Why"):
			whyCommand()

		# print(commandList)
		
# Teach <ARG> <VAR> = <STRING>
def teachVariableDefinition(commandList):
	# get information
	argument = commandList[1]
	variable = commandList[2]
	value = ' '.join(commandList[4::])
	# add information to variableDefinitions
	variableDefinitions[variable] = [value, argument, "false"]

# Teach <ROOT VAR> = <BOOL>
def teachTruth(commandList):
	# get information
	variable = commandList[1]
	truth = commandList[3]
	typeOfVariable = variableDefinitions[variable][1]
	# this command can only be used with root variables
	if(typeOfVariable == "-R"):
		facts[variable] = truth
		variableDefinitions[variable][2] = truth
		# reset all learned variables to the value of false
		for variable, information in variableDefinitions.items():
			if(information[1] == "-L"):
				information[2] = 'false'
				facts[variable] = 'false'

	else:
		print("Error: Cannot set a learned variable directly")

# Teach <EXP> -> <VAR>
def teachNewRule(commandList):
	# check to make sure that all variables here have already been defined via previous Teach commands
	for letter in commandList[1]:
		# ignore command if variables in <EXP> are not defined 
		if( (letter not in "!&|()") and letter not in variableDefinitions.keys() ):
			return
	# ignore command if variable <VAR> is not defined
	if( commandList[3] not in variableDefinitions.keys() ):
		return 

	# add to rules 
	rules.append(' '.join(commandList[1:]))

def listCommand():

	print("Root Variables:")
	for variable, information in variableDefinitions.items():
		if(information[1] == "-R"):
			print(' '*5 + variable + ' = ' + information[0])
	print()

	print("Learned Variables:")
	for variable, information in variableDefinitions.items():
		if(information[1] == "-L"):
			print(' '*5 + variable + ' = ' + information[0])
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

# Query <EXP>
def queryCommand():
	print("in queryCommand")

# Why <EXP>
def whyCommand():
	print("in whyCommand")

if __name__ == "__main__":
	expertSystem()