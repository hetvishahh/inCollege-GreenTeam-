import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button
import re 


ACCOUNT_FILE = "accounts.txt"
JOB_FILE = "jobs.txt"

def load_accounts():
    try:
        with open(ACCOUNT_FILE, "r") as file:
            return [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_account(username, password, first_name, last_name):
    with open(ACCOUNT_FILE, "a") as file:
        file.write(f"{username},{password},{first_name},{last_name}\n")

def is_password_valid(password):
    if not 8 <= len(password) <= 12:
        print("Password length issue")
        return False
    if not re.search("[A-Z]", password):
        print("Missing uppercase letter")
        return False
    if not re.search("[0-9]", password):
        print("Missing digit")
        return False
    if not re.search("[!@#$%^&*()_+=-]", password):
        print("Missing special character")
        return False
    return True


class InCollegeGUI:
    MAX_ACCOUNTS = 5

    def __init__(self, root):
        self.root = root
        self.root.title("InCollege")
        
        # Initialize the 'current_user' attribute for demonstration purposes
        self.current_user = None  # This should be set appropriately during login/logout
        
        # Create the main menu frame
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack()

         # Make sure this is before login attempts
        self.user_display_label = tk.Label(self.main_menu_frame, text="Not logged in",font=('Helvetica', 15, 'bold'),
                        foreground='black',  # Text color
                        background='white')  
        self.user_display_label.pack()


        # Success Story Display
        self.success_story_label = tk.Label(self.main_menu_frame, text="Success Story: John Doe used InCollege to land his dream job at Tech Innovations Inc. within a month of graduating. Join InCollege today and start your success story!")
        self.success_story_label.pack()

        self.watch_video_button = tk.Button(self.main_menu_frame, text="Watch Video",
                                    command=self.play_video,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2)  # Border width
        self.watch_video_button.pack()


        
        # Add buttons for each action
        self.login_button = tk.Button(self.main_menu_frame, text="Log In", command=self.login,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2) # Border width)
        self.login_button.pack()

        self.create_account_button = tk.Button(self.main_menu_frame, text="Create New Account", command=self.create_account_window,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2)  # Border width)
        self.create_account_button.pack()

        self.find_person_button = tk.Button(self.main_menu_frame, text="Find Someone You Know", command=self.find_person_window,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2)  # Border width)
        self.find_person_button.pack()

        self.learn_skill_button = tk.Button(self.main_menu_frame, text="Learn a New Skill", command=self.learn_new_skill,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2)  # Border width)
        self.learn_skill_button.pack()
       
        self.exit_button = tk.Button(self.main_menu_frame, text="Exit", command=root.quit,
                                    foreground='black',  # Text color
                                    background='blue',  # Light blue background
                                    font=('Arial', 12, 'bold'),  # Custom font
                                    borderwidth=2)  # Border width)
        self.exit_button.pack()

        # Create a menubar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create a Job Search/Internship menu item
        self.job_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Job Search/Internship", menu=self.job_menu)
        
        # Add "Post a Job" option to the Job Search/Internship menu
        self.job_menu.add_command(label="Post a Job", command=self.post_job_window)
        # Initially disable "Post a Job". It will be enabled upon user login.
        self.job_menu.entryconfig("Post a Job", state="disabled")

    
    def show_success_story(self):
        """Show the success story and 'Watch Video' button."""
        self.success_story_label.pack()
        self.watch_video_button.pack()

    def hide_success_story(self):
        """Hide the success story and 'Watch Video' button."""
        self.success_story_label.pack_forget()
        self.watch_video_button.pack_forget()


    def play_video(self):
        # This is where you'd integrate video playing functionality.
        # For the purpose of this example, we'll just show a message.
        messagebox.showinfo("Play Video", "Video is now playing")

    def learn_new_skill(self):
        messagebox.showinfo("Under Construction", "Under construction")

    def save_job(self, title, description, employer, location, salary, username):
        with open(JOB_FILE, "a") as file:
            file.write(f"{title},{description},{employer},{location},{salary},{username}\n")

    def load_jobs(self):
        try:
            with open(JOB_FILE, "r") as file:
                return [line.strip().split(",") for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def post_job_window(self):
        jobs = self.load_jobs()
        if len(jobs) >= 5:
            messagebox.showerror("Error", "The system permits up to 5 jobs to be posted.")
            return

        window = Toplevel(self.root)
        window.title("Post a Job")

        # Job entry fields
        entries = {}
        for field in ["Title", "Description", "Employer", "Location", "Salary"]:
            Label(window, text=field+":").pack()
            entry = Entry(window)
            entry.pack()
            entries[field.lower()] = entry

        Button(window, text="Post Job", command=lambda: self.post_job(entries, window)).pack()

    def post_job(self, entries, window):
        job_post = {field: entry.get() for field, entry in entries.items()}
        job_post["username"] = self.current_user  # Assuming self.current_user stores the logged-in username
        
        # Validate job_post fields (e.g., non-empty)
        if not all(job_post.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        self.save_job(job_post)
        messagebox.showinfo("Success", "Job posted successfully.")
        window.destroy()


    def logout(self):
        self.current_user = None  # Reset current_user on logout
        self.user_display_label.config(text="Not logged in") 
        self.show_success_story()
        # Update UI as needed to reflect the logout state

    def verify_login_credentials(self, username, password):
        """Check if provided credentials match an existing account in the file."""
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    stored_username, stored_password, *_ = line.strip().split(',')
                    if stored_username == username and stored_password == password:
                        return True
        except FileNotFoundError:
            pass
        return False



    def login(self):
        username = simpledialog.askstring("Log In", "Enter your username:", parent=self.root)
        password = simpledialog.askstring("Log In", "Enter your password:", parent=self.root, show='*')
        if self.verify_login_credentials(username, password):
            self.current_user = username  # Set current_user to the logged-in username
            messagebox.showinfo("Login Successful", "You have successfully logged in")
            
            # Assuming self.job_menu is your job-related menu and "Post a Job" is a direct item of this menu
            self.job_menu.entryconfig("Post a Job", state="normal")  # Enable the "Post a Job" option

            self.user_display_label.config(text=f"Logged in as: {username}")
            self.hide_success_story()
            
            # Potentially update UI or show/hide certain features based on login status
        else:
            messagebox.showerror("Login Failed", "Incorrect username/password, please try again")


        
    def create_account_window(self):
        accounts = load_accounts()
        if len(accounts) >= 5:
            messagebox.showerror("Error", "All permitted accounts have been created, please come back later")
            return

        window = Toplevel(self.root)
        window.title("Create New Account")

        Label(window, text="First Name:").pack()
        first_name_entry = Entry(window)
        first_name_entry.pack()

        Label(window, text="Last Name:").pack()
        last_name_entry = Entry(window)
        last_name_entry.pack()

        Label(window, text="Username:").pack()
        username_entry = Entry(window)
        username_entry.pack()

        Label(window, text="Password:").pack()
        password_entry = Entry(window, show="*")
        password_entry.pack()

        Button(window, text="Create Account", command=lambda: self.create_account(
            username_entry.get(), password_entry.get(), first_name_entry.get(), last_name_entry.get(), accounts, window
        )).pack()

    def create_account(self, username, password, first_name, last_name, accounts, window):
        if any(acc[0] == username for acc in accounts):
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
            return
        if not is_password_valid(password):
            messagebox.showerror("Error", "Password does not meet criteria.")
            return
        
        save_account(username, password, first_name, last_name)
        messagebox.showinfo("Success", "Account created successfully.")
        window.destroy()

    def find_person_window(self):
        window = Toplevel(self.root)
        window.title("Find Someone You Know")

        Label(window, text="First Name:").pack()
        first_name_entry = Entry(window)
        first_name_entry.pack()

        Label(window, text="Last Name:").pack()
        last_name_entry = Entry(window)
        last_name_entry.pack()

        def search():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            accounts = load_accounts()

            person_found = False
            for account in accounts:
                if account[2].lower() == first_name.lower() and account[3].lower() == last_name.lower():
                    person_found = True
                    break

            if person_found:
                messagebox.showinfo("Search Result", f"{first_name} {last_name} is a part of the InCollege system.")
                self.invite_to_join(first_name, last_name)
            else:
                messagebox.showinfo("Search Result", f"{first_name} {last_name} is not yet a part of the InCollege system yet.")
            window.destroy()

        Button(window, text="Search", command=search).pack()

    def invite_to_join(self, first_name, last_name):
        invite_window = Toplevel(self.root)
        invite_window.title("Invite to Join InCollege")

        Label(invite_window, text=f"Invite {first_name} {last_name} to connect with you on InCollege.").pack()
        Button(invite_window, text="Log In", command=self.login).pack()
        Button(invite_window, text="Sign Up", command=self.create_account_window).pack()



if __name__ == "__main__":
    root = tk.Tk()
    app = InCollegeGUI(root)
    root.mainloop()
