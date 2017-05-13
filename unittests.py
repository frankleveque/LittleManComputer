

import unittest
import LMC_Compiler as lc

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
opCodes['coffee'] = 000
opCodes['coffeebreak'] = 000
opCodes['data'] = None
opCodes['dat'] = None

memory = ["0"] * 100
labels = {}


class Test(unittest.TestCase):
    def test_lowercase(self):
        ins = ["HLT", 132123, "324234", "ASDF", "423423BRZ", ["hLt", 99, "TEST"]]
        ins_lower = ["hlt", "132123", "324234", "asdf", "423423brz", ["hlt", "99", "test"]]
        self.assertEqual(lc.convert_to_lowercase("ABCD"), "abcd")
        self.assertEqual(lc.convert_to_lowercase(ins), ins_lower)
        self.assertEqual(lc.convert_to_lowercase([1234]), ["1234"])
        self.assertEqual(lc.convert_to_lowercase(["12ASDF34"]), ["12asdf34"])
        self.assertEqual(lc.convert_to_lowercase([]), [])
        self.assertEqual(lc.convert_to_lowercase([[],[],['HLT']]), [[],[],['hlt']])
        self.assertEqual(lc.convert_to_lowercase(999),"999")
        self.assertEqual(lc.convert_to_lowercase("999"),"999")

    def test_fix(self):
        self.assertEqual(lc.fixInstructions([["HLT"]]), [[None,"hlt","0"]])
        self.assertEqual(lc.fixInstructions([["DAT"]]), [[None,"dat","0"]])
        self.assertEqual(lc.fixInstructions([["DAT","10"]]), [[None,"dat","10"]])
        self.assertEqual(lc.fixInstructions([["Lab","DAT","10"]]), [["lab","dat","10"]])
        self.assertEqual(lc.fixInstructions([["wat","DAT"]]), [["wat","dat","0"]])
        self.assertEqual(lc.fixInstructions([["wat","INP"]]), [["wat","inp","0"]])
        a = [["DAT"],["DAT","0"],["ASDF","DAT"],["ASDF","DAT","0"],["wat","INP"]]
        b = [[None,"dat","0"],[None,"dat","0"],["asdf","dat","0"],["asdf","dat","0"],["wat","inp","0"]]
        self.assertEqual(lc.fixInstructions(a), b)
    def test_mem(self):
        assert(len(memory) == 100)
    def test_strip(self):
        self.assertEqual(lc.stripLabels([[None,"inp", "10"]]), [["inp","10"]])
        self.assertEqual(lc.stripLabels([[None,"hlt", "10"]]), [["hlt","10"]])
        self.assertEqual(lc.stripLabels([[None,"halt", "10"]]), [["halt","10"]])
        self.assertEqual(lc.stripLabels([["label","dat","20"]]), [["dat","20"]])
        self.assertEqual(lc.stripLabels([[None,"inp","0"],["wat","dat","20"],[None,"add","wat"]]), [["inp","0"],["dat","20"],["add","1"]])
        self.assertEqual(lc.stripLabels([["what","inp","0"],[None,"add","what"]]),[["inp","0"],["add","0"]])
        self.assertEqual(lc.stripLabels([[None,"sub","asdf"]]),[["sub","99"]])
        self.assertEqual(lc.stripLabels([["label","dat","10"]]), [["dat","10"]])
        self.assertEqual(lc.stripLabels([[None,"add","80"],["test","dat","10"],[None,"store","test"]]), [["add","80"],["dat","10"],["store","1"]])
    def test_compile(self):
        self.assertEqual(lc.compileInstruction(["hlt","32"]), 0)
        self.assertEqual(lc.compileInstruction(["store","44"]), 344)
        self.assertEqual(lc.compileInstruction(["sta","77"]), 377)
     


if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)



