'''
simple test
'''
from django.test import SimpleTestCase
from app import calc


class CalcTest(SimpleTestCase):
    '''Test calc module'''

    def test_add_numbers(self):
        '''測試加法功能'''
        var = {
            "x":1,
            "y":2,
        }
        x,y = var.values()
        res = calc.add(x,y)
        self.assertEqual(res,3)
