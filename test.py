"""
Simple program for parsing command line arguments. 
This module contains unit tests for args_java_style and args_exception.

Original Java written by Bob Martin, published in his book "clean code". 

Translated into Python by Emily Bache
"""

import unittest

from args import *
from exception import *


class ArgsTest(unittest.TestCase):
    def testCreateWithNoSchemaOrArguments(self):
        args = Args([], [])
        self.assertEquals(0, args.nextArgument())

    def testWithNoSchemaButWithOneArgument(self):
        self.assertRaises(ArgsException, lambda: Args([], ["-x"]))

    def testWithNoSchemaButWithMultipleArguments(self):
        self.assertRaises(ArgsException, lambda: Args([], ["-x", "-y"]))

    def testNonLetterSchema(self):
        self.assertRaises(ArgsException, lambda: Args([7], []))

    def testInvalidArgumentFormat(self):
        self.assertRaises(ArgsException, lambda: Args([('no type')], []))


    def testSimpleBooleanPresent(self):
        args = Args([('x',bool)], ["-x"])
        self.assertEquals(True, args.getBoolean('x'))
        self.assertEquals(1, args.nextArgument())


    def testSimpleStringPresent(self):
        args = Args(['x', str], ["-x", "param"])
        self.assertTrue(args.has('x'))
        self.assertEquals("param", args.getString('x'))
        self.assertEquals(2, args.nextArgument())

    def testMissingStringArgument(self):
        self.assertRaises(ArgsException, lambda: Args([('x',str)], ["-x"]))


    def testSpacesInFormat(self):
        args = Args([('x',bool),('y',bool)], ["-xy"])
        self.assertTrue(args.has('x'))
        self.assertTrue(args.has('y'))
        self.assertEquals(1, args.nextArgument())

    def testSimpleIntPresent(self):
        args = Args([('x',int)], ["-x", "42"])
        self.assertTrue(args.has('x'))
        self.assertEquals(42, args.getInt('x'))
        self.assertEquals(2, args.nextArgument())

    def testInvalidInteger(self):
        self.assertRaises(ArgsException, lambda: Args([('x',int)], ["-x", "Forty two"]))


    def testMissingInteger(self):
        self.assertRaises(ArgsException, lambda: Args([('x',int)], ["-x"]))

    def testSimpleDoublePresent(self):
        args = Args([('x',float)], ["-x", "42.3"])
        self.assertTrue(args.has('x'))
        self.assertEquals(42.3, args.getDouble('x'), .001)

    def testInvalidDouble(self):
        self.assertRaises(ArgsException, lambda: Args([('x',float)], ["-x", "Forty two"]))

    def testMissingDouble(self):
        self.assertRaises(ArgsException, lambda: Args([('x',float)], ["-x"]))

    def testStringArray(self):
        args = Args([('x',list)], ["-x", "alpha"])
        self.assertTrue(args.has('x'))
        result = args.getStringArray('x')
        self.assertEquals(1, len(result))
        self.assertEquals("alpha", result[0])

    def testMissingStringArrayElement(self):
        self.assertRaises(ArgsException, lambda: Args([('x',list)], ["-x"]))

    def testExtraArguments(self):
        args = Args([('x',bool),('y',str)], ["-x", "-y", "alpha", "beta"])
        self.assertTrue(args.getBoolean('x'))
        self.assertEquals("alpha", args.getString('y'))
        self.assertEquals(3, args.nextArgument())

    def testExtraArgumentsThatLookLikeFlags(self):
        args = Args([('x',bool),('y',bool)], ["-x", "alpha", "-y", "beta"])
        self.assertTrue(args.has('x'))
        self.assertFalse(args.has('y'))
        self.assertTrue(args.getBoolean('x'))
        self.assertFalse(args.getBoolean('y'))
        self.assertEquals(1, args.nextArgument())



if __name__ == "__main__":
    unittest.main()
