import unittest
from unittest.mock import patch
import tkinter as tk
from project import InCollegeGUI

class TestInCollegeGUI(unittest.TestCase):
    def setUp(self):
        self.app = InCollegeGUI(tk.Tk())

    def test_search_student_by_first_name(self):
        search_result = self.app.search_student(first_name)
        self.assertNotEqual(len(search_result), 0)

    def test_search_student_by_last_name(self):
        search_result = self.app.search_student(last_name)
        self.assertNotEqual(len(search_result), 0)
    
    def test_search_student_by_university(self):
        search_result = self.app.search_student(university)
        self.assertNotEqual(len(search_result), 0)

    def test_search_student_by_major(self):
        search_result = self.app.search_student(university)
        self.assertNotEqual(len(search_result), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_send_friend_request(self):
        self.assertIn(sender, self.app.get_pending_friend_requests(recipient))
        mock_showinfo.assert_called_with("Friend request sent")

    @patch("tkinter.messagebox.showinfo")
    def test_accept_friend_request(self):
        self.app.accept_friend_request(recipient, sender)
        self.assertIn(sender, self.app.get_friends_list(recipient))
        self.assertIn(recipient, self.app.get_friends_list(sender))
        mock_showinfo.assert_called_with("Accepted friend request")

    @patch("tkinter.messagebox.showinfo")
    def test_reject_friend_request(self):
        self.app.reject_friend_request(recipient, sender)
        self.assertNotIn(sender, self.app.get_pending_friend_requests(recipient))
        mock_showinfo.assert_called_with("Rejected friend request")

    @patch("tkinter.messagebox.showinfo")
    def test_disconnect_from_friend(self):
        self.app.disconnect_from_friend(user, friend)
        self.assertNotIn(friend, self.app.get_friends_list(user))
        self.assertNotIn(user, self.app.get_friends_list(friend))
        mock_showinfo.assert_called_with("Disconected")


if __name__ == '__main__':
    unittest.main()