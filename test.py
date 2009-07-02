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
        args = Args("", [])
        self.assertEquals(0, args.nextArgument())

    def testWithNoSchemaButWithOneArgument(self):
        self.assertRaises(ArgsException, lambda: Args("", ["-x"]))

    def testWithNoSchemaButWithMultipleArguments(self):
        self.assertRaises(ArgsException, lambda: Args("", ["-x", "-y"]))

    def testNonLetterSchema(self):
        self.assertRaises(ArgsException, lambda: Args("*", []))

    def testInvalidArgumentFormat(self):
        self.assertRaises(ArgsException, lambda: Args("f~", []))


    def testSimpleBooleanPresent(self):
        args = Args("x", ["-x"])
        self.assertEquals(True, args.getBoolean('x'))
        self.assertEquals(1, args.nextArgument())


    def testSimpleStringPresent(self):
        args = Args("x*", ["-x", "param"])
        self.assertTrue(args.has('x'))
        self.assertEquals("param", args.getString('x'))
        self.assertEquals(2, args.nextArgument())

    def testMissingStringArgument(self):
        self.assertRaises(ArgsException, lambda: Args("x*", ["-x"]))


    def testSpacesInFormat(self):
        args = Args("x, y", ["-xy"])
        self.assertTrue(args.has('x'))
        self.assertTrue(args.has('y'))
        self.assertEquals(1, args.nextArgument())

    def testSimpleIntPresent(self):
        args = Args("x#", ["-x", "42"])
        self.assertTrue(args.has('x'))
        self.assertEquals(42, args.getInt('x'))
        self.assertEquals(2, args.nextArgument())

    def testInvalidInteger(self):
        self.assertRaises(ArgsException, lambda: Args("x#", ["-x", "Forty two"]))


    def testMissingInteger(self):
        self.assertRaises(ArgsException, lambda: Args("x#", ["-x"]))

    def testSimpleDoublePresent(self):
        args = Args("x##", ["-x", "42.3"])
        self.assertTrue(args.has('x'))
        self.assertEquals(42.3, args.getDouble('x'), .001)

    def testInvalidDouble(self):
        self.assertRaises(ArgsException, lambda: Args("x##", ["-x", "Forty two"]))

    def testMissingDouble(self):
        self.assertRaises(ArgsException, lambda: Args("x##", ["-x"]))

    def testStringArray(self):
        args = Args("x[*]", ["-x", "alpha"])
        self.assertTrue(args.has('x'))
        result = args.getStringArray('x')
        self.assertEquals(1, len(result))
        self.assertEquals("alpha", result[0])

    def testMissingStringArrayElement(self):
        self.assertRaises(ArgsException, lambda: Args("x[*]", ["-x"]))

    def testExtraArguments(self):
        args = Args("x,y*", ["-x", "-y", "alpha", "beta"])
        self.assertTrue(args.getBoolean('x'))
        self.assertEquals("alpha", args.getString('y'))
        self.assertEquals(3, args.nextArgument())

    def testExtraArgumentsThatLookLikeFlags(self):
        args = Args("x,y", ["-x", "alpha", "-y", "beta"])
        self.assertTrue(args.has('x'))
        self.assertFalse(args.has('y'))
        self.assertTrue(args.getBoolean('x'))
        self.assertFalse(args.getBoolean('y'))
        self.assertEquals(1, args.nextArgument())

class ArgsExceptionTest(unittest.TestCase):
  def testUnexpectedMessage(self):
    e = ArgsException(ErrorCode.UNEXPECTED_ARGUMENT, 'x', None);
    self.assertEquals("Argument -x unexpected.", e.errorMessage());

  def testMissingStringMessage(self):
    e = ArgsException(ErrorCode.MISSING_STRING, 'x', None);
    self.assertEquals("Could not find string parameter for -x.", e.errorMessage());

  def testInvalidIntegerMessage(self):
    e = ArgsException(ErrorCode.INVALID_INTEGER, 'x', "Forty two");
    self.assertEquals("Argument -x expects an integer but was 'Forty two'.", e.errorMessage());

  def testMissingIntegerMessage(self):
    e = ArgsException(ErrorCode.MISSING_INTEGER, 'x', None);
    self.assertEquals("Could not find integer parameter for -x.", e.errorMessage());

  def testInvalidDoubleMessage(self):
    e = ArgsException(ErrorCode.INVALID_DOUBLE, 'x', "Forty two");
    self.assertEquals("Argument -x expects a double but was 'Forty two'.", e.errorMessage());

  def testMissingDoubleMessage(self):
    e = ArgsException(ErrorCode.MISSING_DOUBLE, 'x', None);
    self.assertEquals("Could not find double parameter for -x.", e.errorMessage());

  def testInvalidArgumentName(self):
    e = ArgsException(ErrorCode.INVALID_ARGUMENT_NAME, '#', None);
    self.assertEquals("'#' is not a valid argument name.", e.errorMessage());

  def testInvalidFormat(self):
    e = ArgsException(ErrorCode.INVALID_ARGUMENT_FORMAT, 'x', "$");
    self.assertEquals("'$' is not a valid argument format.", e.errorMessage());




if __name__ == "__main__":
    unittest.main()
