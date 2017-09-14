# Expert System
# Monica Kuo (mdk6jd); Ouyang De (do5xb)

import textwrap

# create data structures
# in the form {"key" : ["value", "R/L"]}
variableDefinitions = {"key" : ["value", "R"], "key2": ["value2", "L"]}
trueVariables = ["E", "D"]
rules = []

def expertSystem():

	while(True):

		# get input 
		commandString = input()
		# parse input
		commandList = commandString.split(' ')
		# call correct function
		if(commandList[0] == "Teach"):
			teachCommand()
		if(commandList[0] == "List"):
			listCommand()
		if(commandList[0] == "Learn"):
			learnCommand()
		if(commandList[0] == "Query"):
			queryCommand()
		if(commandList[0] == "Why"):
			whyCommand()

		# print(commandList)
		

def teachCommand():
	print("in teachCommand")

def listCommand():

	print("Root Variables:")
	for variable, definition in variableDefinitions.items():
		if(definition[1] == "R"):
			print(' '*5 + variable + ' = "' + definition[0] + '"')
	print()

	print("Learned Variables:")
	for variable, definition in variableDefinitions.items():
		if(definition[1] == "L"):
			print(' '*5 + variable + ' = "' + definition[0] + '"')
	print()

	print("Facts:")
	for fact in trueVariables:
		print(' '*5 + fact)
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