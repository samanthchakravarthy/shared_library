import sys,os

print(os.path.abspath('..'))
import calculator
import stringReverse
import unittest


class calculatorTests(unittest.TestCase):

    def setUp(self):
        self.cal_obj = calculator.calculator()

    def test_add_method(self):
        result = self.cal_obj.add(4, 2)
        self.assertEqual(6, result)

    def test_add_method_invalid_value(self):
        self.assertRaises(ValueError, self.cal_obj.add, "four", "five")

    def test_multiply_method(self):
        result = self.cal_obj.mul(5, 3)
        self.assertEqual(15, result)

    def test_multiply_method_invalid_value(self):
        self.assertRaises(ValueError, self.cal_obj.mul, "four", "five")

    def test_sub_method(self):
        result = self.cal_obj.sub(6, 4)
        self.assertEqual(2, result)

    def test_sub_method_invalid_value(self):
        self.assertRaises(ValueError, self.cal_obj.sub, "four", "five")

    def test_div_method(self):
        result = self.cal_obj.div(5, 1)
        self.assertEqual(5, result)

    def test_div_method_invalid_value(self):
        self.assertRaises(ValueError, self.cal_obj.div, "five", "four")

    def test_div_method_zero(self):
        self.assertRaises(ZeroDivisionError, self.cal_obj.div, 5, 0)

    def tearDown(self):
        del self.cal_obj

class stringReverseTests(unittest.TestCase):

   def setUp(self):
        self.rstr_obj = stringReverse.stringReverse()

   def test_string_reverse_normal(self):
        value = self.rstr_obj.sreverse('hello')
        self.assertEqual(value, 'olleh')

   def test_string_reverse_error(self):
       list_of_bad_value = [ 123, None, ]
       for bad_value in list_of_bad_value:
           self.assertRaises(TypeError, self.rstr_obj.sreverse, bad_value)

   def tearDown(self):
        del self.rstr_obj

if __name__ == '__main__':
    unittest.main()