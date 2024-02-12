import getpass
import random
import string

class InCollegeApplication:
    MAX_ACCOUNTS = 5
    accounts = {}  # Dictionary to store username-password pairs
    login_attempts = 0  # Counter to track unsuccessful login attempts

    @classmethod
    def create_account(cls):
        if len(cls.accounts) >= cls.MAX_ACCOUNTS:
            print("All permitted accounts have been created, please come back later.")
            return

        # New - ask for first name and last name
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")

        # Check if the combination of first name and last name is unique
        for account_info in cls.accounts.values():
            if account_info['first_name'] == first_name and account_info['last_name'] == last_name:
                print("An account with this first name and last name already exists.")
                return

        username = input("Enter a unique username: ")
        while username in cls.accounts:
            print("Username already exists. Choose a different username.")
            username = input("Enter a unique username: ")

        password = getpass.getpass("Enter a secure password: ")
        # Existing password validation logic here...

        # New - store first name and last name along with the password
        cls.accounts[username] = {'password': password, 'first_name': first_name, 'last_name': last_name}
        print("Account created successfully.")


    @classmethod
    def login(cls):
        # Method to handle user login
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        if username in cls.accounts and cls.accounts[username] == password:
            print("You have successfully logged in.")
        else:
            print("Incorrect username/password. Please try again.")
            cls.login_attempts += 1  # Increment login attempts counter

    @classmethod
    def show_options_after_login(cls):
        # Method to display options after successful login
        print("Options after login:")
        print("1. Job Search/Internship (Under construction)")
        print("2. Find someone you know (Under construction)")
        print("3. Learn a new skill (Under construction)")
        print("4. Return to previous level")


    @classmethod
    def find_person(cls):
        first_name = input("Enter the first name of the person you're looking for: ")
        last_name = input("Enter the last name of the person you're looking for: ")

        # New - search for the person by first and last name
        found = any(account_info['first_name'] == first_name and account_info['last_name'] == last_name for account_info in cls.accounts.values())

        if found:
            print(f"{first_name} {last_name} is a part of the InCollege system.")
            # Additional logic for connecting with the person
        else:
            print(f"{first_name} {last_name} is not yet a part of the InCollege system yet.")



         

# Example usage:
app = InCollegeApplication()

while True:
    print("1. Log In")
    print("2. Create New Account")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        app.login()
        if app.login_attempts >= 3:  # Example: Allow unlimited login attempts, or set a limit
            print("Too many login attempts. Exiting.")
            break
        else:
            app.show_options_after_login()
    elif choice == "2":
        app.create_account()
    elif choice == "3":
        print("Exiting InCollege application. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
