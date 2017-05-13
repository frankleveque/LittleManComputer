"""
    Copyright (C) 2017 Frank Leveque

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
import lmc_compiler as lc


class Test(unittest.TestCase):
    def test_lowercase(self):
        ins = ["HLT", 132123, "324234", "ASDF", "423423BRZ", ["hLt", 99, "TEST"]]
        ins_lower = ["hlt", "132123", "324234", "asdf", "423423brz", ["hlt", "99", "test"]]
        self.assertEqual(lc.convert_to_lowercase("ABCD"), "abcd")
        self.assertEqual(lc.convert_to_lowercase(ins), ins_lower)
        self.assertEqual(lc.convert_to_lowercase([1234]), ["1234"])
        self.assertEqual(lc.convert_to_lowercase(["12ASDF34"]), ["12asdf34"])
        self.assertEqual(lc.convert_to_lowercase([]), [])
        self.assertEqual(lc.convert_to_lowercase([[], [], ['HLT']]), [[], [], ['hlt']])
        self.assertEqual(lc.convert_to_lowercase(999), "999")
        self.assertEqual(lc.convert_to_lowercase("999"), "999")

    def test_fix(self):
        self.assertEqual(lc.fix_instructions([["HLT"]]), [[None, "hlt", "0"]])
        self.assertEqual(lc.fix_instructions([["DAT"]]), [[None, "dat", "0"]])
        self.assertEqual(lc.fix_instructions([["DAT", "10"]]), [[None, "dat", "10"]])
        self.assertEqual(lc.fix_instructions([["Lab", "DAT", "10"]]), [["lab", "dat", "10"]])
        self.assertEqual(lc.fix_instructions([["wat", "DAT"]]), [["wat", "dat", "0"]])
        self.assertEqual(lc.fix_instructions([["wat", "INP"]]), [["wat", "inp", "0"]])
        a = [["DAT"], ["DAT", "0"], ["ASDF", "DAT"], ["ASDF", "DAT", "0"], ["wat", "INP"]]
        b = [[None, "dat", "0"], [None, "dat", "0"], ["asdf", "dat", "0"], ["asdf", "dat", "0"], ["wat", "inp", "0"]]
        self.assertEqual(lc.fix_instructions(a), b)

    def test_mem(self):
        assert(len(lc.memory) == 100)

    def test_labels(self):
        self.assertEqual(lc.process_labels([[None, "DAT", 32], ["LOOP", "BRZ", 89]]), None)
        self.assertEqual(lc.labels["LOOP"], 1)

    def test_compile(self):
        self.assertEqual(lc.compile_instruction(["hlt", "32"]), 0)
        self.assertEqual(lc.compile_instruction([None, "hlt", 999]), 0)
        self.assertEqual(lc.compile_instruction(["hlt"]), 0)
        self.assertRaises(KeyError, lc.compile_instruction(["hw223lt"]))
        self.assertEqual(lc.compile_instruction(["hw223lt"]), None)
        self.assertEqual(lc.compile_instruction(["store", "44"]), 344)
        self.assertEqual(lc.compile_instruction(["sta", "77"]), 377)

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
