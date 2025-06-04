from unittest.mock import patch
import unittest
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from email_config import send_email

class TestEmail(unittest.TestCase):
    @patch("google.oauth2.service_account.Credentials.from_service_account_file")  # ✅ Patch here
    def test_send_email(self, mock_oauth):
        mock_oauth.return_value = "False Credentials"
        try:
            send_email()  # Call your email function
        except RuntimeError:
            assert False, "❌ Email function should not fail on success!"

    @patch("google.oauth2.service_account.Credentials.from_service_account_file")  # ✅ Patch here
    def test_oauth_failure(self, mock_oauth):
        mock_oauth.side_effect = Exception("OAuth failed")  # Simulate login failure

        with self.assertRaises(Exception):  # ✅ Ensure the failure is correctly handled
            send_email()

if __name__ == '__main__':
    unittest.main()