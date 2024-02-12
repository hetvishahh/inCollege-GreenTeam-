import unittest
from unittest.mock import patch
from main import InCollegeApplication

class TestInCollegeApplication(unittest.TestCase):

    # Previous test_create_account method...

    @patch('builtins.input', side_effect=['2', 'new_user2', 'Password!23', '3'])
    @patch('getpass.getpass', return_value='Password!23')
    def test_account_creation_max_accounts(self, mock_input, mock_getpass):
        """
        Test account creation fails when max accounts limit is reached.
        """
        InCollegeApplication.MAX_ACCOUNTS = 1  # Temporarily set for test
        InCollegeApplication.accounts = {'max_user': 'MaxPass!23'}  # Simulate max accounts reached
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            app.create_account()
            mock_print.assert_called_with("All permitted accounts have been created, please come back later.")
            self.assertEqual(len(InCollegeApplication.accounts), 1)  # No new accounts should be added

    @patch('builtins.input', side_effect=['1', 'new_user', '3'])
    @patch('getpass.getpass', return_value='Password!23')
    def test_login_success(self, mock_input, mock_getpass):
        """
        Test logging in with correct credentials.
        """
        InCollegeApplication.accounts = {'new_user': 'Password!23'}
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            app.login()
            mock_print.assert_called_with("You have successfully logged in.")

    @patch('builtins.input', side_effect=['1', 'wrong_user', '3'])
    @patch('getpass.getpass', return_value='WrongPass!23')
    def test_login_failure(self, mock_input, mock_getpass):
        """
        Test logging in with incorrect credentials.
        """
        InCollegeApplication.accounts = {'new_user': 'Password!23'}
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            app.login()
            mock_print.assert_called_with("Incorrect username/password. Please try again.")

    @patch('builtins.input', side_effect=['1', 'new_user', '1', 'new_user', '1', 'new_user', '3'])
    @patch('getpass.getpass', side_effect=['Wrong!23', 'Wrong!23', 'Password!23'])
    def test_exceed_max_login_attempts(self, mock_input, mock_getpass):
        """
        Test exceeding maximum login attempts.
        """
        InCollegeApplication.accounts = {'new_user': 'Password!23'}
        InCollegeApplication.login_attempts = 0  # Reset for test
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            for _ in range(3):  # Simulate login attempts
                app.login()
            mock_print.assert_called_with("Too many login attempts. Exiting.")
            self.assertEqual(InCollegeApplication.login_attempts, 3)
    @patch('builtins.input', side_effect=['2', 'user1', 'short'])
    @patch('getpass.getpass', return_value='short')
    def test_create_account_with_invalid_password(self, mock_input, mock_getpass):
        """
        Test account creation with a password that doesn't meet the criteria.
        """
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            app.create_account()
            mock_print.assert_called_with("Invalid password. Please follow the password requirements.")
            self.assertNotIn('user1', InCollegeApplication.accounts)

    @patch('builtins.input', side_effect=['2', 'existing_user', 'existing_user', 'ValidPass!23', '3'])
    @patch('getpass.getpass', return_value='ValidPass!23')
    def test_create_account_with_existing_username(self, mock_input, mock_getpass):
        """
        Test creating an account with a username that already exists.
        """
        InCollegeApplication.accounts = {'existing_user': 'SomePass!23'}
        with patch('builtins.print') as mock_print:
            app = InCollegeApplication()
            app.create_account()
            calls = [
                unittest.mock.call("Username already exists. Choose a different username."),
                unittest.mock.call("Account created successfully.")
            ]
            mock_print.assert_has_calls(calls)
            self.assertIn('existing_user', InCollegeApplication.accounts)
            self.assertEqual(InCollegeApplication.accounts['existing_user'], 'SomePass!23')  # The password remains unchanged


    def setUp(self):
        # Reset application state before each test
        InCollegeApplication.accounts = {}
        InCollegeApplication.login_attempts = 0

if __name__ == '__main__':
    unittest.main()
