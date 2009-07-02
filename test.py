"""
Simple program for parsing command line arguments. 
This module contains unit tests for args_java_style and args_exception.

Original Java written by Bob Martin, published in his book "clean code". 

Translated into Python by Emily Bache
"""

import unittest

from args import *


class ArgsTest(unittest.TestCase):
    def testCreateWithNoSchemaOrArguments(self):
        args = Args("", [])
        self.assertEquals(0, args.nextArgument())

    def testWithNoSchemaButWithOneArgument(self):
        try:
            Args("", ["-x"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.UNEXPECTED_ARGUMENT, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())

    def testWithNoSchemaButWithMultipleArguments(self):
        try:
            Args("", ["-x", "-y"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.UNEXPECTED_ARGUMENT, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())

    def testNonLetterSchema(self):
        try:
            Args("*", [])
            self.fail("Args constructor should have thrown exception")
        except ArgsException, e:
            self.assertEquals(ErrorCode.INVALID_ARGUMENT_NAME, e.getErrorCode())
            self.assertEquals('*', e.getErrorArgumentId())

    def testInvalidArgumentFormat(self):
        try:
            Args("f~", [])
            self.fail("Args constructor should have throws exception")
        except ArgsException, e:
            self.assertEquals(ErrorCode.INVALID_ARGUMENT_FORMAT, e.getErrorCode())
            self.assertEquals('f', e.getErrorArgumentId())


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
        try:
            Args("x*", ["-x"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.MISSING_STRING, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())


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
        try:
            Args("x#", ["-x", "Forty two"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.INVALID_INTEGER, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())
            self.assertEquals("Forty two", e.getErrorParameter())


    def testMissingInteger(self):
        try:
            Args("x#", ["-x"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.MISSING_INTEGER, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())

    def testSimpleDoublePresent(self):
        args = Args("x##", ["-x", "42.3"])
        self.assertTrue(args.has('x'))
        self.assertEquals(42.3, args.getDouble('x'), .001)

    def testInvalidDouble(self):
        try:
            Args("x##", ["-x", "Forty two"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.INVALID_DOUBLE, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())
            self.assertEquals("Forty two", e.getErrorParameter())

    def testMissingDouble(self):
        try:
            Args("x##", ["-x"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.MISSING_DOUBLE, e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())

    def testStringArray(self):
        args = Args("x[*]", ["-x", "alpha"])
        self.assertTrue(args.has('x'))
        result = args.getStringArray('x')
        self.assertEquals(1, len(result))
        self.assertEquals("alpha", result[0])

    def testMissingStringArrayElement(self):
        try:
            Args("x[*]", ["-x"])
            self.fail()
        except ArgsException, e:
            self.assertEquals(ErrorCode.MISSING_STRING,e.getErrorCode())
            self.assertEquals('x', e.getErrorArgumentId())

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
