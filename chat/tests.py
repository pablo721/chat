from django.test import TestCase
from .utils import format_timer
# Create your tests here.




class TimeFormatterTest(TestCase):

    def test_format_time(self):
        secs = 5000  #
        expected =  '1h, 23m, 20s'
        formatted_time = format_timer(secs)
        assert formatted_time == '1h 23m 20s', f'format_timer error: expected {expected}, got {formatted_time}'



