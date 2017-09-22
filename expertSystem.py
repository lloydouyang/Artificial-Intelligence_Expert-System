# Expert System
# Monica Kuo (mdk6jd); De Ouyang (do5xb)

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
                if(commandList[1][i] in "!&|()"):
                    j=j-1
                    break
            letter=commandList[1][i:j+1]
            if letter not in variableDefinitions.keys():
                print("ignore")
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



# Query <EXP>
def queryCommand():
    print("in queryCommand")

# Why <EXP>
def whyCommand():
    print("in whyCommand")

if __name__ == "__main__":
    expertSystem()
