import unittest
from unittest.mock import patch
import tkinter as tk
from project import InCollegeGUI

class TestInCollegeGUI(unittest.TestCase):

    def setUp(self):
        self.app = InCollegeGUI(tk.Tk())
        
    def test_show_copyright_notice(self):
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.show_copyright_notice()
        mock_showerror.assert_called_once_with("Copyright Notice", "This application is presented by the USF’s Software Engineering Green Team and is protected by copyright laws. Distribution of this resource without written permission of the sponsor is prohibited.\n© 2024 Hetvi Shah, Austin Molketin, Silvana Chain Marulanda, Dat Nguyen, Boburjon Usmonov")

    def test_show_help_center(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_help_center()
        mock_showinfo.assert_called_once_with("Help Center", "We're here to help.")

    def test_show_about(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_about()

        # Add assertions for each call
        mock_showinfo.assert_any_call("About", "Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.")
        mock_showinfo.assert_any_call("Our Vision: Empowering Students to Shape Their Future", "We envision a world where every college student has direct access to the tools and connections necessary to forge a successful career path. InCollege is more than just a software package; it's the commencement of potential, a network of opportunity, and a community of like-minded individuals committed to professional growth.")
        mock_showinfo.assert_any_call("Contact Us", "To learn more about InCollege or to provide support for our venture, please reach out to one of our team members.\nHetvi Shah: hetvi@usf.edu\nAustin Molketin: amolketin@usf.edu\nSilvana Chain Marulanda: smchain@usf.edu\nDat Nguyen: dnguyen182@usf.edu\nBoburjon Usmonov: boburjon@usf.edu\nLet's build the future of student professional development together.")

    def test_show_accessibility(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_accessibility()
        mock_showinfo.assert_called_once_with("Accessibility","At inCollege, we prioritize accessibility to ensure an inclusive job search experience for all college students. Our app features accessibility options, including screen reader compatibility, customizable text settings, and simplified navigation, making it user-friendly for individuals with diverse needs. Alt text for images and color contrast options are incorporated to enhance accessibility further. We are dedicated to creating an environment where every college student, regardless of abilities, can effortlessly utilize our platform to explore and pursue career opportunities.")

    def test_show_user_agreement(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_user_agreement()
        mock_showinfo.assert_called_once_with("User Agreement", "By using the InCollege platform, users agree to abide by the following terms and conditions: 1.Users must provide accurate and truthful information when creating an account and using the platform. 2.Users are responsible for maintaining the confidentiality of their account credentials and for all activities that occur under their account. 3.Users must respect the rights of other users and refrain from engaging in any form of harassment, bullying, or discrimination. 4.Users must not use the platform for any illegal or unauthorized purposes, including but not limited to spamming, phishing, or distributing malware. 5.Users retain ownership of the content they share on InCollege but grant the platform a non-exclusive,royalty-free license to use, reproduce, and distribute their content for the purpose of operating and promoting the platform. 6.InCollege reserves the right to remove any content or suspend/terminate any account that violates these terms or is deemed inappropriate or harmful to the community. 7.By using InCollege, users acknowledge and agree to these terms and conditions. Violation of the User Agreement may result in the suspension or termination of the users account without prior notice.")

    def test_show_cookie_policy(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_cookie_policy()
        mock_showinfo.assert_called_once_with("cookie","At InCollege, we value your privacy and strive to be transparent about our use of cookies. Cookies are small data files stored on your device to enhance your experience on our platform by remembering your preferences and visits. We use them to ensure our website functions correctly, to analyze our traffic, and to personalize content and ads. By using the InCollege platform, you consent to the use of cookies in accordance with our Privacy Policy. For more information on how we use cookies and how you can manage them, please visit our full Cookie Policy page.")

    def test_show_copyright_policy(self):
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_copyright_policy()
        mock_showinfo.assert_called_once_with("copyright policy",'The Copyright Policy of InCollege states that all content shared on the platform, including but not limited to text, images, videos, and documents, is subject to copyright protection. Users must ensure they have the necessary rights or permissions to share any content on InCollege. Infringement of copyright will result in the removal of the infringing content and may lead to the suspension or termination of the users account')

if __name__ == '__main__':
    unittest.main()
