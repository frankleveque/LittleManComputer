'''
1 ADD - ADD
2 SUB - SUBTRACT
3 STA - STORE 
5 LDA - LOAD
6 BRA - BRANCH/JUMP
7 BRZ - BRANCH IF ZERO
8 BRP - BRANCH IF POSITIVE

901 INP - INPUT
902 OUT - OUTPUT
000 HLT/HCF - HALT/COFFEE

DAT - DATA

'''

import sys
import re 

opCodes = {}
opCodes['add'] = 100
opCodes['sub'] = 200
opCodes['sta'] = 300
opCodes['store'] = 300
opCodes['load'] = 500
opCodes['lda'] = 500
opCodes['branch'] = 600
opCodes['bra'] = 600
opCodes['branchzero'] = 700
opCodes['brz'] = 700
opCodes['branchpositive'] = 800
opCodes['brp'] = 800
opCodes['input'] = 901
opCodes['inp'] = 901
opCodes['output'] = 902
opCodes['out'] = 902
opCodes['halt'] = 000
opCodes['hlt'] = 000
opCodes['hcf'] = 000
opCodes['coffee'] = 000
opCodes['coffeebreak'] = 000
opCodes['data'] = None
opCodes['dat'] = None

memory = ["000"] * 100
labels = {}

def convert_to_lowercase(instructions):
    if isinstance(instructions, str) or isinstance(instructions, int):
        instructions = str(instructions).lower()
    else:
        for i in range(len(instructions)):
            if isinstance(instructions[i], str) or isinstance(instructions[i], int):
                instructions[i] = str(instructions[i]).lower()
            else:
                for j in range(len(instructions[i])):
                        instructions[i][j] = str(instructions[i][j]).lower()
    return instructions


def fixInstructions(instructions):

    if not instructions:
        return
    initial = len(instructions)


    # massage inputs
    for i in range(len(instructions)):
        if len(instructions[i]) == 1:
            instructions[i] = [None] + instructions[i] + ["0"] 

        elif (len(instructions[i]) == 2 and instructions[i][0] in opCodes):
            instructions[i] = [None] + instructions[i]

        elif (len(instructions[i]) == 2 and not (instructions[i][0] in opCodes)):
            instructions[i] += ["0"] 
        
    # check
    for i in range(len(instructions)):
        assert len(instructions[i]) >= 2
        assert instructions[i][0] not in opCodes
        assert instructions[i][1] in opCodes
    
    assert len(instructions[:]) == initial
    return instructions


def stripLabels(instructions):
  
    
    for i in range(len(instructions)):
        assert len(instructions[i]) == 3

        # first is label or none
        first = instructions[i][0]
        if first and first not in labels:
            print("Label " + first + " added")
            labels[first] = str(i)
            instructions[i][1] = str(i) 
        elif first and first in labels:
            print("WARNING: " + first + " already defined - ignoring")



    # strip definitions 
    for i in range(len(instructions)):
        assert len(instructions[i]) == 3
       
    
        first = instructions[i][0]
        if first:
            #defining keyword
            if first not in labels.keys():
                labels[instructions[i][0]] = str(i)
            else:
                print("Warning: Label " + first + " already defined")
        
                    
        # remove first index
        instructions[i] = instructions[i][1:]
        assert len(instructions[i]) == 2


        second = instructions[i][1]
        if second.isalpha() and second not in labels:
            print("Warning: Label " + second + " not defined anywhere - using mailbox 99")
            labels[second] = "99"
            instructions[i][1] = "99" 
  

        for i in range(len(instructions)):
            for j in range(len(instructions[i])):

                try:
                    if (instructions[i][j] not in opCodes.keys() and not str(instructions[i][j]).isdigit()):
                        instructions[i][j] = labels[instructions[i][j]]

                except KeyError:
                    if instructions[i][j] is not None:
                        print("label " + str(instructions[i][j]) + "" + " not defined")
   
        


    # check
    for i in range(len(instructions)):
        assert len(instructions[i]) == 2

    return instructions



def compileInstruction(instruction):
    '''
    [OP] [Mailbox/Value]
    '''
    assert len(instruction) <= 3 
    try:
        assert instruction[0].isalpha() 
    except AssertionError:
        print("+++++++++++",instruction[0],"+++++++++++")

    
    op = None
    box = None
    try:
        op = instruction[0]
        opcode = opCodes[op]
        box = instruction[1]
        
        if isinstance(box,int):
            box = int(box)
        elif box.isalpha():
            box = labels[box]


        if (op == 'hlt' or op == 'halt' or op == 'inp' or op == 'input'):
            return opcode
        elif (op == 'dat' or op == 'data'):
            return int(box)
        else:
            return opcode + int(box)
           
    except KeyError:
           print("Warning: Opcode not defined " + str(op) + " - returning HLT")
           return 0
 




if __name__ == "__main__":
    

    if len(sys.argv) < 2:
        print("Needs input file(s)")
        sys.exit(0)

    for a in sys.argv[1:]:

        instructions = [] 
        with open(a) as f:
            data = f.readline()
            while data != "":
                if data == '\n' or data.startswith('#'):
                    data = f.readline()
                    continue
                data = data.split() 
                instructions += [data]
                data = f.readline()


        instructions = convert_to_lowercase(instructions)
        instructions = fixInstructions(instructions)

        print("Instructions: ")
        for a in range(len(instructions)):
            for b in range(len(instructions[a])):
                print(instructions[a][b], end="|")
            print("")
        print("")
        instructions = stripLabels(instructions)
      
        
        for i in range(len(instructions)):
            memory[i] = "%.03i" % compileInstruction(instructions[i])


        assert len(memory) == 100
  


        with open(a+'.lmc', 'w+') as out:
            for line in memory:
                out.write(str(line) + '\n')

else:
    pass



