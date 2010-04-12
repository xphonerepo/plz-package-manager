#!/usr/bin/env python
import unittest, string

# hack to import plz (without .py)
_current_name, __name__ = __name__, ''
execfile('plz')
__name__ = _current_name

class RangeExpansionCheck(unittest.TestCase):
    def testExpandIntegerRanges(self):
        s = 's[1-3].example.com'
        expected = set('s%d.example.com' % i for i in range(1,4))
        self.assertEquals(expected, range_expansion(s))

    def testExpandElements(self):
        s = '[one,two,three].example.com'
        expected = set("%s.example.com" % i for i in ["one", "two", "three"])
        self.assertEquals(expected, range_expansion(s))

    def testCombinedRanges(self):
        s = 's[1-3].[one,two].example.com'
        expected = ['s1.one.example.com',
                    's2.one.example.com',
                    's3.one.example.com',
                    's1.two.example.com',
                    's2.two.example.com',
                    's3.two.example.com']
        self.assertEquals(set(expected), range_expansion(s))

    def testNestedRanges(self):
        s = 'www.[s[1-3], p[1-3], one].example.com'
        expected = ['www.s1.example.com',
                    'www.s2.example.com',
                    'www.s3.example.com',
                    'www.p1.example.com',
                    'www.p2.example.com',
                    'www.p3.example.com',
                    'www.one.example.com']
        self.assertEquals(set(expected), range_expansion(s))

    def testNestedElements(self):
        s = 'www.[[one,two],[x,y,z],[1-3]].example.com'
        expected = ['www.one.example.com',
                    'www.two.example.com',
                    'www.x.example.com',
                    'www.y.example.com',
                    'www.z.example.com',
                    'www.1.example.com',
                    'www.2.example.com',
                    'www.3.example.com']
        self.assertEquals(set(expected), range_expansion(s))

# --- test config parser ---

# Test: Assignments, bool, dict list, string, float, bool, and,
# or, xor,arithmetics, string expressions and if..then..else.
#
# The test code is mostly ripped from 'test_grammar.py', available
# from the Python source tree. 

test_backslash_1 = r"""
x = 1 \
+ 1
"""

test_backslash_2 = r"""
# Backslash does not means continuation in comments :\
x = 0
"""

test_integers_1 = r"""
a = 0xff
b = 0377
c = 2147483647
"""

test_long_ints_1 = r"""
x = 0L
x = 0l
x = 0xffffffffffffffffL
x = 0xffffffffffffffffl
x = 077777777777777777L
x = 077777777777777777l
x = 123456789012345678901234567890L
x = 123456789012345678901234567890l
"""

test_string_literals_1 = r"""
x = ''; y = ""
"""

test_string_literals_2 = r"""
x = '\''; y = "'"
"""

test_string_literals_3 = r"""
x = '"'; y = "\""
"""

test_string_literals_4 = r"""
x = "doesn't \"shrink\" does it"
y = 'doesn\'t "shrink" does it'
"""

test_string_literals_5 = r"""
x = "does \"shrink\" doesn't it"
y = 'does "shrink" doesn\'t it'
"""

test_string_literals_6 = r'''
x = r"""
The "quick"
brown fox
jumps over
the 'lazy' dog.
"""
y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
'''

test_string_literals_7 = r"""
y = '''
The "quick"
brown fox
jumps over
the 'lazy' dog.
'''
"""

test_string_literals_8 = r'''
y = "\n\
The \"quick\"\n\
brown fox\n\
jumps over\n\
the 'lazy' dog.\n\
"
'''

test_string_literals_9 = r"""
y = '\n\
The \"quick\"\n\
brown fox\n\
jumps over\n\
the \'lazy\' dog.\n\
'
"""

test_if_stmt_1 = r"""
if 1: pass
if 1: pass
else: pass
if 0: pass
elif 0: pass
if 0: pass
elif 0: pass
elif 0: pass
elif 0: pass
else: pass
"""

test_and_or_not_1 = r"""
if not 1: pass
if 1 and 1: pass
if 1 or 1: pass
if not not not 1: pass
if not 1 and 1 and 1: pass
if 1 and 1 or 1 and 1 and 1 or not 1 and 1: pass
"""

test_comparison_1 = r"""
if 1: pass
x = (1 == 1)
if 1 == 1: pass
if 1 != 1: pass
if 1 <> 1: pass
if 1 < 1: pass
if 1 > 1: pass
if 1 <= 1: pass
if 1 >= 1: pass
if 1 is 1: pass
if 1 is not 1: pass
if 1 in (): pass
if 1 not in (): pass
if 1 < 1 > 1 == 1 >= 1 <= 1 <> 1 != 1 in 1 not in 1 is 1 is not 1: pass
"""

test_binary_ops_1 = r"""
x = 1 & 1
x = 1 ^ 1
x = 1 | 1
"""

test_shift_ops_1 = r"""
x = 1 << 1
x = 1 >> 1
x = 1 << 1 >> 1
"""

test_additive_ops_1 = r"""
x = 1
x = 1 + 1
x = 1 - 1 - 1
x = 1 - 1 + 1 - 1 + 1
"""

test_multiplicative_ops_1 = r"""
x = 1 * 1
x = 1 / 1
x = 1 % 1
x = 1 / 1 * 1 % 1
"""

test_unary_ops_1 = r"""
x = +1
x = -1
x = ~1
x = ~1 ^ 1 & 1 | 1 & 1 ^ -1
x = -1*1/1 + 1*1 - ---1*1
"""

test_stmt_suite_1 = r"""
if 1: pass
if 1:
    pass
if 1:
#
#
#
    pass
pass
#
pass
#
"""

test_atoms_1 = r"""
x = (1)
x = (1 or 2 or 3)
x = (1 or 2 or 3, 2, 3)

x = []
x = [1]
x = [1 or 2 or 3]
x = [1 or 2 or 3, 2, 3]
x = []

x = {}
x = {'one': 1}
x = {'one': 1,}
x = {'one' or 'two': 1 or 2}
x = {'one': 1, 'two': 2}
x = {'one': 1, 'two': 2,}
x = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}

x = `x`
x = `1 or 2 or 3`
x = x
x = 'x'
x = 123
"""

class ConfigParserTest(unittest.TestCase):
    """
    Verify the functionality of the configuration parser for
    a range of different data types and statements.
    """

    def test_backslash(self):
        # Backslash means line continuation:
        res = parse_config(test_backslash_1)
        self.failUnless(res['x'] == 2)

        res = parse_config(test_backslash_2)
        self.failUnless(res['x'] == 0)

    def test_integers(self):
        # hex, octal and large positive ints.
        res = parse_config(string.lstrip(test_integers_1))
        self.failUnless(res['a'] == 255 and res['b'] == 255
                   and res['c'] == 017777777777)

    def test_long_ints(self):
        # test that the longint formats parses.
        res = parse_config(test_long_ints_1)
 
    def test_string_literals(self):
        # test some string definitions.
        res = parse_config(test_string_literals_1)
        self.failUnless(len(res['x']) == 0 and res['x'] == res['y'])

        res = parse_config(test_string_literals_2)
        self.failUnless(len(res['x']) == 1
                        and res['x'] == res['y'] and ord(res['x']) == 39)

        res = parse_config(test_string_literals_3)
        self.failUnless(len(res['x']) == 1
                        and res['x'] == res['y'] and ord(res['x']) == 34)
        
        res = parse_config(test_string_literals_4)
        self.failUnless(len(res['x']) == 24 and res['x'] == res['y'])

        res = parse_config(test_string_literals_5)
        self.failUnless(len(res['x']) == 24 and res['x'] == res['y'])

        res = parse_config(test_string_literals_6)
        self.failUnless(res['x'] == res['y'])

        res = parse_config(test_string_literals_6
                                  + test_string_literals_7)
        self.failUnless(res['x'] == res['y'])

        res = parse_config(test_string_literals_6
                                  + test_string_literals_8)
        self.failUnless(res['x'] == res['y'])

        res = parse_config(test_string_literals_6
                                  + test_string_literals_9)
        self.failUnless(res['x'] == res['y'])
        
    def test_syntax_error(self):
        self.failUnlessRaises(SyntaxError,
                              parse_config("a + 1 = b + 2"))
        self.failUnlessRaises(SyntaxError,
                              parse_config("x + 1 = 1"))
    
    def test_if_stmt(self):
        res = parse_config(test_if_stmt_1)

    def test_and_or_not(self):
        res = parse_config(test_and_or_not_1)

    def test_comparison(self):
        res = parse_config(test_comparison_1)

    def test_binary_ops(self):
        res = parse_config(test_binary_ops_1)

    def test_shift_ops(self):
        res = parse_config(test_shift_ops_1)

    def test_additive_ops(self):
        res = parse_config(test_additive_ops_1)

    def test_multiplicative_ops(self):
        res = parse_config(test_multiplicative_ops_1)

    def test_unary_ops(self):
        res = parse_config(test_unary_ops_1)

    def test_stmt_suite(self):
        res = parse_config(test_stmt_suite_1)

    def test_atoms(self):
        res = parse_config(test_atoms_1)

if __name__ == "__main__":
    unittest.main()
