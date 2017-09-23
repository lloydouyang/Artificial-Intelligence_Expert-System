# Expert System
# Monica Kuo (mdk6jd); De Ouyang (do5xb)

import textwrap

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
            whyCommand(commandList[1])

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
                if facts[subs]=="true":
                    a=True
                else:
                    a=False
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                if facts[subs2]=="true":
                    b=True
                else:
                    b=False

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
                if facts[subs]=="true":
                    a=True
                else:
                    a=False
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                if facts[subs2]=="true":
                    b=True
                else:
                    b=False

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
            if facts[s]=="true":
                return True
            else:
                return False

def learnCommand():

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
                        if variableDefinitions[subs][1]=="-R":
                            if f:
                                print("I KNOW IT IS NOT TRUE THAT "+translate(subs))
                        else:
                            potentialChange=backwardc(subs,workingmemory,f)
                            if potentialChange:
                                workingmemory[subs]="true"
                                s=s.replace(s[p:i+1],"#")
                            else:
                                s=s.replace(s[p:i+1],"@")
                    else:
                        if f:
                            print("I KNOW THAT "+translate(subs))
                        s=s.replace(s[p:i+1],"#")

                else:
                    potentialChange=backwardc(subs,workingmemory,f)
                    if potentialChange:
                        workingmemory[subs]="true"
                    else:
                        workingmemory[subs]="false"
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
                    if workingmemory[subs]=="true":
                        a=True
                        if f:
                            print("I KNOW THAT "+translate(subs))
                    else:
                        if variableDefinitions[subs][1]=="-R":
                            if f:
                                print("I KNOW IT IS NOT TRUE THAT "+translate(subs))
                            a=False
                        else:
                            a=backwardc(subs,workingmemory,f)
                else:
                    a=backwardc(subs,workingmemory,f)
                    if a:
                        workingmemory[subs]="true"
                    else:
                        workingmemory[subs]="false"
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                if subs2 in workingmemory:
                    if workingmemory[subs2]=="true":
                        b=workingmemory[subs2]
                        if f:
                            print("I KNOW THAT "+translate(subs2))
                    else:
                        if variableDefinitions[subs2][1]=="-R":
                            if f:
                                print("I KNOW IT IS NOT TRUE THAT "+translate(subs2))
                            b=False
                        else:
                            b=backwardc(subs2,workingmemory,f)
                else:
                    b=backwardc(subs2,workingmemory,f)
                    if b:
                        workingmemory[subs2]="true"
                    else:
                        workingmemory[subs2]="false"

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
                    if workingmemory[subs]=="true":
                        a=True
                        if f:
                            print("I KNOW THAT "+translate(subs))
                    else:
                        if variableDefinitions[subs][1]=="-R":
                            if f:
                                print("I KNOW IT IS NOT TRUE THAT "+translate(subs))
                            a=False
                        else:
                            a=backwardc(subs,workingmemory,f)
                else:
                    a=backwardc(subs,workingmemory,f)
                    if a:
                        workingmemory[subs]="true"
                    else:
                        workingmemory[subs]="false"
        if subs2=="@":
            b=True
        else:
            if subs2=="#":
                b=False
            else:
                if subs2 in workingmemory:
                    if workingmemory[subs2]=="true":
                        b=True
                        if f:
                            print("I KNOW THAT "+translate(subs2))
                    else:
                        if variableDefinitions[subs2][1]=="-R":
                            if f:
                                print("I KNOW IT IS NOT TRUE THAT "+translate(subs2))
                            b=False
                        else:
                            b=backwardc(subs2,workingmemory,f)
                else:
                    b=backwardc(subs2,workingmemory,f)
                    if b:
                        workingmemory[subs2]="true"
                    else:
                        workingmemory[subs2]="false"

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
                    if f:
                        print("I KNOW THAT "+translate(s))
                    return True
                else:
                    return backwardc(s,workingmemory,f)
            else:

                return backwardc(s,workingmemory,f)


def backwardc(v,workingmemory,f):
    temp=""
    for rule in rules:
        p=rule.find(">")
        if rule[p+2:]==v:
            if backevaluate(rule[:p-2],workingmemory,f):
                if f:
                    print("BECAUSE IT IS TRUE THAT "+translate(rule[:p-2]), "I KNOW THAT "+translate(rule[p+2:]))
                return True
            else:
                temp=rule[:p-2]
    if f:
        print("BECAUSE IT IS NOT TRUE THAT "+temp+" I CANNOT PROVE THAT "+translate(v))
    return False

def translate(s):

    s=s.replace("!"," NOT ")
    s=s.replace("&"," AND ")
    s=s.replace("|"," OR ")
    for variable, fact in facts.items():
        s=s.replace(variable,variableDefinitions[variable][0])
    return s
# Query <EXP>
def queryCommand(s):
#    print(workingmemory)

    workingmemory=facts.copy()

    print(backevaluate(s,workingmemory,False))


# Why <EXP>
def whyCommand(s):
    workingmemory=facts.copy()
    flg=backevaluate(s,workingmemory,False)
    print(flg)
    str=""
    pp=""
    for i in range(len(s)):
        if s[i] not in "!&|()":
            pp=pp+s[i]
        else:
            if pp!="":
                if pp in workingmemory:
                    if workingmemory[pp]=="true":
                        print("I KNOW THAT "+translate(pp))
                    else:
                        if variableDefinitions[pp][1]=="-R":
                            print("I KNOW IT IS NOT TRUE THAT "+translate(pp))
                        else:
                            backwardc(pp,workingmemory,True)
                else:
                    backwardc(pp,workingmemory,True)
                pp=""
    if pp!="":
                if pp in workingmemory:
                    if workingmemory[pp]=="true":
                        print("I KNOW THAT "+translate(pp))
                    else:
                        if variableDefinitions[pp][1]=="-R":
                            print("I KNOW IT IS NOT TRUE THAT "+translate(pp))
                        else:
                            backwardc(pp,workingmemory,True)
                else:
                    backwardc(pp,workingmemory,True)
                pp=""
    if flg:
        print("THUS I KNOW THAT "+translate(s))
    else:
        print("THUS I CANNOT PROVE THAT "+translate(s))



if __name__ == "__main__":
    expertSystem()
