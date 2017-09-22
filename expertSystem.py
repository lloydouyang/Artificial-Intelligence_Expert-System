# Expert System
# Monica Kuo (mdk6jd); De Ouyang (do5xb)

import textwrap
import pdb

# create data structures
# in the form {"variable" : ["value", "-R/-L", "true/false"]}
variableDefinitions = {}
# in the form {"variable" : "true/false"}
facts = {}
rules = []
workingmemory={}

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

            queryCommand(commandList[1])

        if(commandList[0] == "Why"):
            whyCommand(commandList)

        # print(commandList)

# Teach <ARG> <VAR> = <STRING>
def teachVariableDefinition(commandList):
    # get information
    argument = commandList[1]
    variable = commandList[2]
    value = ' '.join(commandList[4::])
    # add information to variableDefinitions
    variableDefinitions[variable] = [value, argument, "false"]
    facts[variable]="false"

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
                information[2] = "false"
                facts[variable] = "false"

    else:
        print("Error: Cannot set a learned variable directly")

# Teach <EXP> -> <VAR>
def teachNewRule(commandList):
    # check to make sure that all variables here have already been defined via previous Teach commands
    for i in range(len(commandList[1])):
        # ignore command if variables in <EXP> are not defined
        if(commandList[1][i] not in "!&|()"):
            for j in range(i,len(commandList[1]),1):
                if(commandList[1][j] in "!&|()"):
                    j=j-1
                    break
            letter=commandList[1][i:j+1]
            #print(letter)
            if letter not in variableDefinitions.keys():
                #print("ignore")
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
# find the index of corresponding ")"
def findclose(q,s):
    d=1
    for i in range(q+1,len(s),1):
        if s[i]=="(":
            d+=1
        else:
            if s[i]==")":
                d-=1
        if d==0: return i
    return -1
# To evaluate expression to give true or false, @ means true, # means false
def evaluate(s):

    # get rid of ()
    q=s.find("(")
    qq=findclose(q,s)
    while (q!=-1):
        flag2= evaluate(s[q+1:qq])
        if flag2:
            s=s.replace(s[q:qq+1],"@")
        else:
            s=s.replace(s[q:qq+1],"#")
        q=s.find("(")
        qq=findclose(q,s)


    p=s.find("!")
    while p!=-1:
        for i in range(p+1,len(s),1):
            if (s[i] in "!&|()"):
                i=i-1
                break
        subs=s[p+1:i+1]
        if subs=="#":
            s=s.replace(s[p:i+1],"@")
        else:
            if subs=="@":
                s=s.replace(s[p:i+1],"#")
            else:
                if facts[subs]=="false":
                    s=s.replace(s[p:i+1],"@")
                else:
                    s=s.replace(s[p:i+1],"#")
        p=s.find("!")
    #print(s)
    # get rid of &
    p=s.find("&")
    while (p!=-1):

        for i in range(p+1,len(s),1):
            if (s[i] in "!&|()"):
                i=i-1
                break
        for j in range(p-1,-1,-1):
            if (s[j] in "!&|()"):
                j=j+1
                break
        subs=s[p+1:i+1]
        subs2=s[j:p]
        if subs=="@":
            a=True
        else:
            if subs=="#":
                a=False
            else:
                a=facts[subs]
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                b=facts[subs2]

        if (a and b):
            s=s.replace(s[j:i+1],"@")
        else:
            s=s.replace(s[j:i+1],"#")
        p=s.find("&")
    # get rid of |
    p=s.find("|")
    while (p!=-1):
        i=p+1
        for i in range(p+1,len(s),1):

            if (s[i] in "!&|()"):
                i=i-1
                break
        for j in range(p-1,-1,-1):
            if (s[j] in "!&|()"):
                j=j+1
                break
        subs=s[p+1:i+1]
        subs2=s[j:p]
        if subs=="@":
            a=True
        else:
            if subs=="#":
                a=False
            else:
                a=facts[subs]
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                b=facts[subs2]

        if (a or b):
            s=s.replace(s[j:i+1],"@")
        else:
            s=s.replace(s[j:i+1],"#")
        p=s.find("|")
        #print(s)
    if s=="@":
        return True
    else:
        return False

def learnCommand():
    print("in learnCommand")
    #Testing Evaluate
    # #print(evaluate("S&V"))
    #print(evaluate("!V&S"))
    #print(evaluate("!V&(S|V)"))
    #print(evaluate("S|!(V|S)"))
    #print(evaluate("(S|V)|!(V|S)"))
    #print(evaluate("((S|V))"))
    #print(evaluate("((S|V)|!(V|S))"))
    flag=True
    while flag:
        flag=False
        for rule in rules:
            p=rule.find(" ")
            s=rule[:p]
            var=rule[p+4:]
            if facts[var]=="false":
                if evaluate(s):
                    facts[var]="true"
                    flag=True


def backevaluate(s,workingmemory,f):

    # get rid of ()
    q=s.find("(")
    qq=findclose(q,s)
    while (q!=-1):
        flag2= backevaluate(s[q+1:qq],workingmemory,f)
        if flag2:
            s=s.replace(s[q:qq+1],"@")


        else:
            s=s.replace(s[q:qq+1],"#")
        q=s.find("(")
        qq=findclose(q,s)


    p=s.find("!")
    while p!=-1:
        for i in range(p+1,len(s),1):
            if (s[i] in "!&|()"):
                i=i-1
                break
        subs=s[p+1:i+1]
        if subs=="#":
            s=s.replace(s[p:i+1],"@")
        else:
            if subs=="@":
                s=s.replace(s[p:i+1],"#")
            else:
                if subs in workingmemory:
                    if workingmemory[subs]=="false":
                        potentialChange=backwardc(subs,workingmemory,f)
                        if potentialChange:
                            workingmemory[subs]=True
                            s=s.replace(s[p:i+1],"#")
                        else:
                            s=s.replace(s[p:i+1],"@")
                    else:
                        s=s.replace(s[p:i+1],"#")

                else:
                    workingmemory[subs]=backwardc(subs,workingmemory,f)
                    if workingmemory[subs]=="false":
                        s=s.replace(s[p:i+1],"@")
                    else:
                        s=s.replace(s[p:i+1],"#")


        p=s.find("!")
    #print(s)
    # get rid of &
    p=s.find("&")
    while (p!=-1):

        for i in range(p+1,len(s),1):
            if (s[i] in "!&|()"):
                i=i-1
                break
        for j in range(p-1,-1,-1):
            if (s[j] in "!&|()"):
                j=j+1
                break
        subs=s[p+1:i+1]
        subs2=s[j:p]
        if subs=="@":
            a=True
        else:
            if subs=="#":
                a=False
            else:
                if subs in workingmemory:
                    if workingmemory[subs]:
                        a=workingmemory[subs]
                    else:
                        a=backwardc(subs,workingmemory,f)
                else:
                    a=backwardc(subs,workingmemory,f)
                    workingmemory[subs]=a
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                if subs2 in workingmemory:
                    if workingmemory[subs2]:
                        b=workingmemory[subs2]
                    else:
                        b=backwardc(subs2,workingmemory,f)
                else:
                    b=backwardc(subs2,workingmemory,f)
                    workingmemory[subs]=b
        if (a and b):
            s=s.replace(s[j:i+1],"@")
        else:
            s=s.replace(s[j:i+1],"#")
        p=s.find("&")
    # get rid of |
    p=s.find("|")
    while (p!=-1):
        i=p+1
        for i in range(p+1,len(s),1):

            if (s[i] in "!&|()"):
                i=i-1
                break
        for j in range(p-1,-1,-1):
            if (s[j] in "!&|()"):
                j=j+1
                break
        subs=s[p+1:i+1]
        subs2=s[j:p]
        if subs=="@":
            a=True
        else:
            if subs=="#":
                a=False
            else:
                if subs in workingmemory:
                    if workingmemory[subs]:
                        a=workingmemory[subs]
                    else:
                        a=backwardc(subs,workingmemory,f)
                else:
                    a=backwardc(subs,workingmemory,f)
                    workingmemory[subs]=a
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                b=workingmemory[subs2]
                if subs2 in workingmemory:
                    if workingmemory[subs2]:
                        b=workingmemory[subs2]
                    else:
                        b=backwardc(subs2,workingmemory,f)
                else:
                    b=backwardc(subs2,workingmemory,f)
                    workingmemory[subs]=b

        if (a or b):
            s=s.replace(s[j:i+1],"@")
        else:
            s=s.replace(s[j:i+1],"#")
        p=s.find("|")
        #print(s)
    if s=="@":
        return True
    else:
        if s=="#":
            return False
        else:
            if s in workingmemory:

                if workingmemory[s]=="true":
                    return True
                else:
                    return backwardc(s,workingmemory,f)
            else:

                return backwardc(s,workingmemory,f)


def backwardc(v,workingmemory,f):
    for rule in rules:
        p=rule.find(">")
        if rule[p+2:]==v:
            if backevaluate(rule[:p-2],workingmemory,f):
                return True
    return False


# Query <EXP>
def queryCommand(s):
#    print(workingmemory)

    workingmemory=facts.copy()

    print(backevaluate(s,workingmemory,False))


def queryCommand(commandList):
	expression = commandList[1]
	print(evaluate(expression))

# Node class for expression tree
class Node(object):
	left = None
	right = None
	data = None
	def __init_(self):
		self.left = None
		self.right = None
		self.data = None
	def getLeft(self):
		return self.left
	def getRight(self):
		return self.right
	def getData(self):
		return self.data
	def setLeft(self, left):
		self.left = left
	def setRight(self, right):
		self.right = right
	def setData(self, data):
		self.data = data

# Why <EXP>
def whyCommand(commandList):
	expression = commandList[1]

	# print the truth of the expression
	print(evaluate(expression))
	
	# print truth
	root = Node()
	createExpressionTree(expression, root)
	# printTree(root)
	parseExpressionTree(root)

def printTree(root):
	# leaf
	if(root.getLeft() == None and root.getRight() == None):
		print(root.getData())
	# inner nodes
	else:
		if(root.getLeft() != None):
			printTree(root.getLeft())
		print(root.getData())
		if(root.getRight() != None):
			printTree(root.getRight())

def parseExpressionTree(root):
	# variable
	if(root.getLeft() == None and root.getRight() == None):
		variable = root.getData()
		variableTruth = evaluate(variable)
		variableValue = variableDefinitions[variable][0]
		pdb.set_trace()
		if(variableTruth == True):
			print ("I KNOW THAT", variableValue)
		else:
			print ("I KNOW IT IS NOT TRUE THAT", variableValue)
	# inner nodes
	else:
		if(root.getLeft() != None):
			printTree(root.getLeft())
		print(root.getData())
		if(root.getRight() != None):
			printTree(root.getRight())

def createExpressionTree(expression, root):	
	# print(expression)
	
	# recursively call createExpressionTree on inner parts of expression
	beginParenIndex = expression.find("(")
	endParenIndex = findclose(beginParenIndex, expression)

	symbolIndex = findSymbol(expression)

	# if there are () expressions
	if( (beginParenIndex != -1) and (endParenIndex != -1) ):

		# if there is a symbol separating () expressions
		symbolIndex = findSymbol(expression)
		if(symbolIndex != -1):
			leftExpression = expression[:symbolIndex]
			left = Node()
			root.setLeft(left)
			createExpressionTree(leftExpression, left)
			root.setData(expression[symbolIndex])
			rightExpression = expression[(symbolIndex+1):]
			right = Node()
			root.setRight(right)
			createExpressionTree(rightExpression, right)

		else:
			newExpression = expression[(beginParenIndex+1):endParenIndex]
			createExpressionTree(newExpression, root)

	# if there is a symbol, recurse
	elif(symbolIndex != -1):
		leftExpression = expression[:symbolIndex]
		left = Node()
		root.setLeft(left)
		createExpressionTree(leftExpression, left)
		root.setData(expression[symbolIndex])
		rightExpression = expression[(symbolIndex+1):]
		right = Node()
		root.setRight(right)
		createExpressionTree(rightExpression, right)
	else:
		# base case
		root.setData(expression)
		return root

def findSymbol(expression):
	openParen = 0
	index = 0
	for char in expression:
		if(char == ")"):
			openParen-=1
			index+=1
			continue
		if(char == "("):
			openParen+=1
			index+=1
			continue
		if(openParen > 0):
			index+=1
			continue
		if(char in "!&|"):
			return index
		index+=1
	return -1
>>>>>>> work on why command

if __name__ == "__main__":
    expertSystem()

