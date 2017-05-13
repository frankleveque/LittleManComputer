import sys
import re

opCodes = {
    'add': 100,
    'sub': 200,
    'sta': 300,
    'store': 300,
    'load': 500,
    'lda': 500,
    'branch': 600,
    'bra': 600,
    'branchzero': 700,
    'brz': 700,
    'branchpositive': 800,
    'brp': 800,
    'input': 901,
    'inp': 901,
    'output': 902,
    'out': 902,
    'halt': 000,
    'hlt': 000,
    'hcf': 000,
    'coffee': 000,
    'coffeebreak': 000,
    'data': None,
    'dat': None
}
memory = ["000"] * 100
labels = {}


def convert_to_lowercase(instructions):
    """
    converts elements in instructions to lowercase if possible
    :param instructions: list of instruction lists
    :return: list of lowercase instruction lists
    """
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


def fix_instructions(instructions):
    """
    converts instructions to proper format:
        [ None/label | instruction | label/box# ]

    :param instructions: list of instruction lists
    :return: list of fixed instruction lists
    """
    orig_len = len(instructions[:])

    instructions = convert_to_lowercase(instructions)

    # massage inputs
    for i in range(len(instructions)):
        if len(instructions[i]) == 1:
            instructions[i] = [None] + instructions[i] + ["0"]

        elif len(instructions[i]) == 2 and instructions[i][0] in opCodes:
            instructions[i] = [None] + instructions[i]

        elif len(instructions[i]) == 2 and not (instructions[i][0] in opCodes):
            instructions[i] += ["0"] 
        
    # postcondition checks
    for i in range(len(instructions)):
        assert len(instructions[i]) == 3
        assert instructions[i][0] not in opCodes
        assert instructions[i][1] in opCodes
    assert len(instructions[:]) == orig_len

    return instructions[:]


def process_labels(instructions):
    """
    goes through instructions and adds label definitions to label dictionary for later

    :param instructions: list of instruction lists
    :return: None
    """
    for i in range(len(instructions)):
        assert len(instructions[i]) == 3
        if instructions[i][0]:
            print("Label added: ", repr(instructions[i][0]), i)
            labels[instructions[i][0]] = i


def compile_instruction(instruction):
    """
        Takes an instruction list and returns its compiled value
        Should take the form of:
            [ None/label | instruction | label/box# ]
        but tries to handle special values
        
        :param instruction: list of instructions
        :return: compiled value 
    """
    if len(instruction) == 1:
        try:
            return opCodes[list(instruction)[0]]
        except KeyError:
            print(list(instruction)[0] + " is not a valid op code")
            return None

    elif len(instruction) == 2:
        instruction = [None] + instruction

    assert len(instruction) == 3

    op = instruction[1]
    opcode = opCodes[op]
    box = instruction[2]

    try:
        assert op.isalpha()
    except AssertionError:
        print(op + " is not a valid op code")

    try:
        if isinstance(box, int):
            box = int(box)
        elif box.isalpha():
            box = labels[box]

        if op == 'hlt' or op == 'halt' or op == 'inp' or op == 'input':
            return opcode
        elif op == 'dat' or op == 'data':
            return int(box)
        else:
            return opcode + int(box)

    except KeyError:
        print("Warning: Opcode " + repr(op) + " or label " + repr(box) + " not defined - returning HLT")
        return 0


def remove_comments(instructions):
    """
    removes comments from string
    :param instructions: string of chars that will be split later into instructions
    :return: fixed string without comments
    """
    temp = ""
    row = instructions.rstrip().lstrip()
    row = re.sub(r'\s', " ", row)
    row = re.sub(r'#.*$', " ", row)
    row = row.rstrip().lstrip()

    r = row.find("#")
    s = row.find("//")

    lowest = r if r < s and r > -1 and r else s
    if lowest != -1:
        temp += row[:lowest]
    else:
        temp += row

    return temp





if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Needs input file(s)")
        sys.exit(0)

    for file in sys.argv[1:]:
        instructions = [] 
        with open(file) as f:
            data = f.readline()
            while data != "":
                if data == '\n' or data.startswith('#') or data.startswith("//"):
                    data = f.readline()
                    continue
                data = remove_comments(data)
                data = data.split() 
                instructions += [data]
                data = f.readline()


        instructions = fix_instructions(instructions)

        process_labels(instructions)

        for i in range(len(instructions)):
            memory[i] = "%.03i" % compile_instruction(instructions[i])

        assert len(memory) == 100
  
        with open(file + '.lmc', 'w+') as out:
            for line in memory:
                out.write(str(line) + '\n')

        print("")
        print("Instructions: ")
        for row in list(instructions):
            for item in row:
                print(str(item), end="|")
                pass
            print("")
        print("")

else:
    pass
