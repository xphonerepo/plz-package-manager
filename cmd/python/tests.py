#!/usr/bin/env python
import unittest

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

if __name__ == "__main__":
    unittest.main()
