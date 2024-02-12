import getpass

class InCollegeApplication:
    MAX_ACCOUNTS = 5
    accounts = {}  # Dictionary to store user information
    job_posts = []  # List to store job posts (up to 5)
    login_attempts = 0  # Counter to track unsuccessful login attempts

    @classmethod
    def create_account(cls):
        if len(cls.accounts) >= cls.MAX_ACCOUNTS:
            print("All permitted accounts have been created, please come back later.")
            return

        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        # Ensure unique first and last name combination
        if any(u['first_name'] == first_name and u['last_name'] == last_name for u in cls.accounts.values()):
            print("An account with this first and last name already exists.")
            return

        username = input("Enter a unique username: ")
        while username in cls.accounts:
            print("Username already exists. Choose a different username.")
            username = input("Enter a unique username: ")

        password = getpass.getpass("Enter a secure password: ")
        # Add your password validation logic here...

        cls.accounts[username] = {'password': password, 'first_name': first_name, 'last_name': last_name}
        print("Account created successfully.")

        current_user = None

    @classmethod
    def login(cls):
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        if username in cls.accounts and cls.accounts[username]['password'] == password:
            print("You have successfully logged in.")
            cls.current_user = username  # Set the current_user to the logged-in username
            cls.show_options_after_login()
        else:
            print("Incorrect username/password. Please try again.")
            cls.login_attempts += 1

    @classmethod
    def show_options_after_login(cls):
        print("1. Job Search/Internship")
        print("2. Find someone you know")
        print("3. Learn a new skill")
        print("4. Post a job")
        print("5. Return to previous level")

        choice = input("Enter your choice: ")
        if choice == "1":
            print("Under construction")
        elif choice == "2":
            cls.find_person()
        elif choice == "3":
            cls.learn_new_skill()
        elif choice == "4":
            cls.post_job()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please enter a valid option.")

    @classmethod
    def find_person(cls):
        print("Find someone you know.")
        first_name = input("Enter the first name of the person: ")
        last_name = input("Enter the last name of the person: ")

        # Search for a person by their first and last name.
        for account_info in cls.accounts.values():
            if account_info['first_name'].lower() == first_name.lower() and account_info['last_name'].lower() == last_name.lower():
                print(f"{first_name} {last_name} is a part of the InCollege system.")
                # Here you could add additional functionality, such as asking if the user wants to connect with this person.
                return
        print(f"{first_name} {last_name} is not yet a part of the InCollege system yet.")


    @classmethod
    def learn_new_skill(cls):
        skills = [
            "1. Time management",
            "2. Teamwork and collaboration",
            "3. Emotional intelligence",
            "4. Digital literacy",
            "5. Critical thinking"
        ]
        print("Select a skill to learn:")
        for skill in skills:
            print(skill)

        choice = input("Enter the number of the skill you want to learn (or 'exit' to go back): ")
        if choice.lower() == 'exit':
            return
        if choice.isdigit() and 1 <= int(choice) <= len(skills):
            print(f"{skills[int(choice) - 1]} is an important skill. This feature is under construction.")
        else:
            print("Invalid choice. Please enter a number from the list or 'exit' to go back.")


    @classmethod
    def post_job(cls):
        if len(cls.job_posts) >= 5:
            print("The maximum number of job posts has been reached. Please try again later.")
            return

        if cls.current_user is None:  # Check if a user is logged in
            print("You must be logged in to post a job.")
            return

        title = input("Enter the job title: ")
        description = input("Enter the job description: ")
        employer = input("Enter the employer's name: ")
        location = input("Enter the location: ")
        salary = input("Enter the salary: ")
        
        job_post = {
            'title': title,
            'description': description,
            'employer': employer,
            'location': location,
            'salary': salary,
            'posted_by': cls.current_user  # Use the class attribute for the username
        }
        cls.job_posts.append(job_post)
        print("Job posted successfully.")





def main():
    app = InCollegeApplication()

    while True:
        print("\nWelcome to InCollege!")
        print("1. Log In")
        print("2. Create New Account")
        print("3. Find Someone You Know")
        print("4. Learn a New Skill")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            app.login()
        elif choice == "2":
            app.create_account()
        elif choice == "3":
            app.find_person()
        elif choice == "4":
            app.learn_new_skill()
        elif choice == "5":
            print("Thank you for using InCollege. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

