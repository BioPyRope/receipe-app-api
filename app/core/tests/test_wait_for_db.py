"""Test the commands of wait_for_db at /core"""

from unittest.mock import patch
from psycopg2 import OperationalError as psycopg2Error

from django.core.management import call_command
from django.test import SimpleTestCase

from django.db.utils import OperationalError

@patch("core.management.commands.wait_for_db.Command.check") # patched_check
class CommandTest(SimpleTestCase):
    
    def test_wait_for_db_ready(self,patched_check):
        
        patched_check.return_values=True
        call_command("wait_for_db")# 此時我會期待
        patched_check.assert_called_once_with(databases=["default"])
    
    @patch("time.sleep") # patched_sleep
    def test_wait_for_db_delay(self,patched_sleep,patched_check):
        
        patched_check.side_effect=[psycopg2Error]*2+[OperationalError]*3+[True]
        
        call_command("wait_for_db")
        
        self.assertEqual(patched_check.call_count,6)
        patched_check.assert_called_with(databases=["default"])