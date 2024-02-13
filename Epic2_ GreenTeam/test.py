import unittest
from tkinter import Tk
from unittest.mock import patch
import os

from in_college_gui import InCollegeGUI, load_accounts, save_account, is_password_valid


class TestInCollegeGUI(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = InCollegeGUI(self.root)
        if os.path.exists("accounts.txt"):
            os.remove("accounts.txt")
        if os.path.exists("jobs.txt"):
            os.remove("jobs.txt")

    def tearDown(self):
        self.root.destroy()
        if os.path.exists("accounts.txt"):
            os.remove("accounts.txt")
        if os.path.exists("jobs.txt"):
            os.remove("jobs.txt")

    def test_load_accounts_file_not_found(self):
        accounts = load_accounts()
        self.assertEqual(accounts, [])

    def test_save_account_creates_file(self):
        save_account("username", "Password1!", "First", "Last")
        self.assertTrue(os.path.exists("accounts.txt"))
        with open("accounts.txt", "r") as file:
            content = file.read()
        self.assertIn("username,Password1!,First,Last\n", content)

    def test_is_password_valid(self):
        self.assertTrue(is_password_valid("Valid1!"))
        self.assertFalse(is_password_valid("short"))
        self.assertFalse(is_password_valid("nouppercase1!"))
        self.assertFalse(is_password_valid("NOLOWER1!"))
        self.assertFalse(is_password_valid("NoSpecial1"))

    @patch("builtins.input", side_effect=["username", "Password1!"])
    @patch("builtins.print")
    def test_verify_login_credentials(self, mock_print, mock_input):
        save_account("username", "Password1!", "First", "Last")
        self.assertTrue(self.app.verify_login_credentials("username", "Password1!"))
        self.assertFalse(self.app.verify_login_credentials("wrong", "Password1!"))

    @patch("tkinter.simpledialog.askstring")
    def test_create_account_limit(self, mock_askstring):
        for i in range(5):
            save_account(f"user{i}", "Password1!", f"First{i}", f"Last{i}")
        mock_askstring.side_effect = ["user5", "Password1!", "First5", "Last5"]
        with patch("tkinter.messagebox.showerror") as mock_showerror:
            self.app.create_account_window()
            mock_showerror.assert_called_once_with(
                "Error",
                "All permitted accounts have been created, please come back later",
            )


if __name__ == "__main__":
    unittest.main()
