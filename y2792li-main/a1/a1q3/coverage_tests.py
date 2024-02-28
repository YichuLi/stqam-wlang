import unittest

from . import token_with_escape 


class CoverageTests(unittest.TestCase):
    def test_1(self):
        """Node Coverage but not Edge Coverage is infeasible
            Because covering all nodes would naturally lead to covering all edges as well,
            making it infeasible to have full node coverage without full edge coverage."""
        """TR: {8,11,12,13,14,20,21,23}"""
        inpt1 = '^a'
        result1 = token_with_escape(inpt1)
        self.assertEqual(result1, ['a'])
        """TR: {8,11,12,13,15,16,23}"""
        inpt2 = '|'
        result2 = token_with_escape(inpt2)
        self.assertEqual(result2, ['', ''])
        """TR: {8,11,12,13,15,18,19,23}"""
        inpt3 = 'a'
        result3 = token_with_escape(inpt3)
        self.assertEqual(result3, ['a'])

    def test_2(self):
        """Edge Coverage but not Edge-pair Coverage"""
        """TR: {[8,11], [11,12], [11,23], [12,13], [12,20], 
        [13,14], [13,15], [14,11], [15,16], [15,19], [16,11], [19,11], [20,21], [21,11]}"""
        inpt4 = 'a^a|'
        result4 = token_with_escape(inpt4)
        self.assertEqual(result4, ['aa', ''])

    def test_3(self):
        """Edge Pair Coverage but not Prime Path Coverage"""
        """TR: {[8,11,12], [11,12,13], [11,12,20], [12,13,14], [12,13,15], [12,20,21], [13,14,11], 
        [13,15,16], [13,15,19], [14,11,12], [15,16,11], [15,19,11], [16,11,23], [19,11,12], [20,21,11], [21,11,12]}"""
        inpt5 = 'a^a|'
        result5 = token_with_escape(inpt5)
        self.assertEqual(result5, ['aa', ''])
        """TR: {[8,11,23]}"""
        inpt6 = ''
        result6 = token_with_escape(inpt6)
        self.assertEqual(result6, [''])
        """TR: {[8,11,12], [11,12,13], [12,13,14], [13,14,11], [14,11,23]}"""
        inpt7 = '^'
        result7 = token_with_escape(inpt7)
        self.assertEqual(result7, [''])
        """TR: {[8,11,12], [11,12,13], [12,13,15], [13,15,16], [15,16,11], 
                [16,11,12], [13,15,19], [15,19,11], [19,11,23]}"""
        inpt8 = '|a'
        result8 = token_with_escape(inpt8)
        self.assertEqual(result8, ['', 'a'])
        """TR: {[8,11,12], [11,12,13], [12,13,14], [13,14,11], [14,11,12], 
                [12,20,21], [20,21,11], [21,11,23]}"""
        inpt9 = '^a'
        result9 = token_with_escape(inpt9)
        self.assertEqual(result9, ['a'])
