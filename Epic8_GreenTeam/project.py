import tkinter as tk
import os
import webbrowser
import subprocess
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, Checkbutton, BooleanVar, Text
from friends_manager import send_friend_request, accept_friend_request, reject_friend_request, list_friends, list_pending_requests
import re 
import json
from messaging import MessagingSystem
from datetime import datetime, timezone, timedelta



ACCOUNT_FILE = "accounts.txt"
JOB_FILE = "jobs.txt"
APPLIED_JOBS_FILE = "applied_jobs.txt"
SAVED_JOBS_FILE = "saved_jobs.txt"

def load_accounts():
    try:
        with open(ACCOUNT_FILE, "r") as file:
            return [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_account(username, password, first_name, last_name, university, major, plus_account):
    #creation_time = datetime.datetime.now().isoformat()
    with open(ACCOUNT_FILE, "a") as file:
        account_type = "Plus" if plus_account else "Standard"
        file.write(f"{username},{password},{first_name},{last_name},{university},{major},{account_type}\n")
    # Append new student name to new_students.json
    try:
        with open("new_students.json", "r+") as file:
            new_students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        new_students = []

    new_students.append(f"{first_name} {last_name}")
    with open("new_students.json", "w") as file:
        json.dump(new_students, file)






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
    MAX_ACCOUNTS = 10

    def __init__(self, root):
        self.root = root
        self.root.title("InCollege")
        root.geometry("1000x600")
       # root.configure(background='light blue')
        self.messaging_system = MessagingSystem()

        
        # Initialize the 'current_user' attribute for demonstration purposes
        self.current_user = None  # This should be set appropriately during login/logout
        
        # Create the main menu frame
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack()

         # Make sure this is before login attempts
        self.user_display_label = tk.Label(self.main_menu_frame, text="Not logged in",font=('Helvetica', 15, 'bold'),
                        foreground='black',  # Text color
                        background='light blue')  
        self.user_display_label.pack()

        # Initialize this label in your __init__ method
        self.account_type_label = tk.Label(self.main_menu_frame, text="Account type unknown")
        self.account_type_label.pack()

        # Success Story Display
        self.success_story_label = tk.Label(self.main_menu_frame, text="Success Story: Bob used InCollege to land his dream job within a month of graduating. Join InCollege today and start your success story!")
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

        self.create_account_button = tk.Button(self.main_menu_frame, text="Sign Up", command=self.create_account_window,
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

        self.logout_button = tk.Button(self.main_menu_frame, text="Logout",
                                   command=self.logout)
        self.logout_button.pack()

        # Create a menubar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create "Useful Links" menu
        self.useful_links_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Useful Links", menu=self.useful_links_menu)

        # Add items to "Useful Links" menu
        self.useful_links_menu.add_command(label="General", command=self.show_under_construction)
        self.useful_links_menu.add_command(label="Browse InCollege", command=self.show_under_construction)
        self.useful_links_menu.add_command(label="Business Solutions", command=self.show_under_construction)
        self.useful_links_menu.add_command(label="Directories", command=self.show_under_construction)

        # Create "InCollege Important Links" menu
        self.important_links_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="InCollege Important Links", menu=self.important_links_menu)

        # Add items to "InCollege Important Links" menu
        self.important_links_menu.add_command(label="Sign Up", command=self.create_account_window)
        self.important_links_menu.add_command(label="Help Center", command=self.show_help_center)
        self.important_links_menu.add_command(label="About", command=self.show_about)
        self.important_links_menu.add_command(label="Press", command=self.show_press)
        self.important_links_menu.add_command(label="Blog", command=self.show_under_construction)
        self.important_links_menu.add_command(label="Careers", command=self.show_under_construction)
        self.important_links_menu.add_command(label="Developers", command=self.show_under_construction)

        # Create other items for "InCollege Important Links"
        self.important_links_menu.add_command(label="A Copyright Notice", command=self.show_copyright_notice)
        self.important_links_menu.add_command(label="Accessibility", command=self.show_accessibility)
        self.important_links_menu.add_command(label="User Agreement", command=self.show_user_agreement)
        self.important_links_menu.add_command(label="Privacy Policy", command=self.privacy_policy)
        self.important_links_menu.add_command(label="Cookie Policy", command=self.show_cookie_policy)
        self.important_links_menu.add_command(label="Copyright Policy", command=self.show_copyright_policy)
        self.important_links_menu.add_command(label="Brand Policy", command=self.show_brand_policy)
        self.important_links_menu.add_command(label="Languages", command=self.change_language)


        # Create a Job Search/Internship menu item
        self.job_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Job Search/Internship", menu=self.job_menu)
        
        # Add "Post a Job" option to the Job Search/Internship menu
        self.job_menu.add_command(label="Post a Job", command=self.post_job_window)
        # Initially disable "Post a Job". It will be enabled upon user login.
        self.job_menu.entryconfig("Post a Job", state="disabled")

        self.job_menu.add_command(label="See Jobs", command=self.show_jobs_window)
        self.job_menu.add_command(label="Saved jobs", command=self.show_saved_jobs)
        self.job_menu.add_command(label="Applied jobs", command=self.show_applied_jobs)


       
        self.user_settings = {
            'email': True,
            'sms': True,
            'advertising': True,
            # Add other default settings if necessary
        }

        # Load user settings from file or other persistent storage
        self.load_user_settings()



        # friends management GUI
        self.manage_friends_button = tk.Button(self.root, text="Manage Friends", command=self.manage_friends)
        self.manage_friends_button.pack()

        # Button to view profile
        self.view_profile_button = tk.Button(self.root, text="View Profile", command=self.display_user_profile)
        self.view_profile_button.pack()

        # Button to edit profile
        self.edit_profile_button = tk.Button(self.root, text="Edit Profile", command=self.edit_user_profile)
        self.edit_profile_button.pack()

        self.messaging_system = MessagingSystem()

        # Create a 'Message' button in the main window
        self.message_button = tk.Button(self.main_menu_frame, text="Message", command=self.create_message_window)
        self.message_button.pack()

        self.message_button = tk.Button(self.main_menu_frame, text="Check Inbox", command=self.display_messages)
        self.message_button.pack()
    

    def check_job_application_reminder(self):
            tk.messagebox.showinfo("Reminder", "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")


    def check_profile_completion_reminder(self):
        if not self.is_profile_complete(self.current_user):
            tk.messagebox.showinfo("Profile Completion", "Don't forget to create a profile.")

    def check_new_messages(self):
        if self.messaging_system.get_messages_for_user(self.current_user):
            tk.messagebox.showinfo("New Messages", "You have messages waiting for you.")
    
    def notify_job_application_status(self):
        applied_jobs_count = self.get_applied_jobs_count(self.current_user)
        tk.messagebox.showinfo("Job Application Status", f"You have currently applied for {applied_jobs_count} jobs.")


    def notify_new_job(self, job_title):
        tk.messagebox.showinfo("New Job Posted", f"A new job '{job_title}' has been posted.")


    

    def is_profile_complete(self, username):
        profile_data = self.load_profile(username)
        required_fields = ['university', 'major', 'information', 'experience', 'education']
        
        # Check if each required field is present and non-empty
        for field in required_fields:
            if field not in profile_data or not profile_data[field].strip():
                return False
        
        return True







    def display_messages(self):
        # Retrieve messages for the current user
        user_messages = self.messaging_system.get_messages_for_user(self.current_user)
        
        # Create a new window to display messages
        message_window = tk.Toplevel(self.root)
        message_window.title("Inbox")

        # If there are no messages, display a message and return
        if not user_messages:
            tk.Label(message_window, text="No messages in your inbox.").pack()
            return
        
        # Create a listbox to display messages
        listbox = tk.Listbox(message_window, width=50, height=10)
        listbox.pack()
        for message in user_messages:
            listbox.insert(tk.END, f"From {message['from']}: {message['message']}")

        # Optionally, add a scrollbar to the listbox
        scrollbar = tk.Scrollbar(message_window, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

    
    def create_message_window(self):
        message_window = Toplevel(self.root)
        message_window.title("Send a Message")

        Label(message_window, text="To:").pack(side='left')
        to_entry = Entry(message_window)
        to_entry.pack(side='left', fill='x', expand=True)

        Label(message_window, text="Message:").pack(anchor='w')
        message_text = Text(message_window, height=5, width=40)
        message_text.pack()

        send_button = tk.Button(message_window, text="Send",
                        command=lambda: self.send_message(
                            self.current_user,
                            to_entry.get(),
                            message_text.get("1.0", tk.END).strip(), message_window))
        send_button.pack()
        
    def send_message(self, from_user, to_user, message, message_window):
        # This will call the send_message method of the messaging_system instance
        result = self.messaging_system.send_message(from_user, to_user, message)
        
        # Check if the message was sent successfully before closing the window
        if "Message sent." in result:
            message_window.destroy()
        #else:
            #tk.messagebox.showerror("Message", result)
           # message_window.destroy()
        # The window will be closed and a messagebox will show the result either way

    
    def create_send_message_to_anyone_button(self):
        # This method will be called after user login, to check their status and add button if they're a Plus member
        if self.messaging_system.is_plus_member(self.current_user):
            send_to_anyone_button = tk.Button(self.main_menu_frame, text="Send Message to Any User", command=self.show_all_users)
            send_to_anyone_button.pack()

    def show_all_users(self):
        all_users_window = tk.Toplevel(self.root)
        all_users_window.title("All Users")

        # Get all usernames from the accounts file
        all_usernames = self.messaging_system.get_all_usernames()

        # Display all usernames as buttons
        for username in all_usernames:
            if username != self.current_user:  # Don't allow users to message themselves
                user_button = tk.Button(all_users_window, text=username, command=lambda u=username: self.create_plus_message_window(u))
                user_button.pack()


    def create_plus_message_window(self, recipient=None):
        # Create a window for sending a message
        message_window = tk.Toplevel(self.root)
        message_window.title("Send a Message")

        # Entry for the recipient's username
        to_label = tk.Label(message_window, text="To:")
        to_label.pack(side='top', anchor='w')

        to_entry = tk.Entry(message_window)
        to_entry.pack(side='top', fill='x', expand=True)
        if recipient:
            to_entry.insert(0, recipient)

        # Text field for the message body
        message_label = tk.Label(message_window, text="Message:")
        message_label.pack(anchor='w')

        message_text = tk.Text(message_window, height=5, width=40)
        message_text.pack()

        # Send button to submit the message
        send_button = tk.Button(message_window, text="Send", command=lambda: self.send_plus_message(to_entry.get(), message_text.get("1.0", tk.END).strip()))
        send_button.pack()

    def send_plus_message(self, to_user, message):
        # Call the send_message method from MessagingSystem
        result = self.messaging_system.send_message_as_plus(self.current_user, to_user, message)
        tk.messagebox.showinfo("Message Status", result)
       
        


    

    def manage_friends(self):
        self.friends_window = tk.Toplevel(self.root)
        self.friends_window.title("Manage Friends")

        tk.Button(self.friends_window, text="View Friends", command=self.show_friends_list).pack()
        tk.Button(self.friends_window, text="View Friend Requests", command=self.show_friend_requests).pack()
        tk.Button(self.friends_window, text="Send Friend Request", command=self. send_friend_request_interface).pack()

    def show_friends_list(self):
    # Retrieve the list of friends for the current user
        friends = list_friends(self.current_user)  # Assuming you have a function to list friends

        friends_window = tk.Toplevel(self.root)
        friends_window.title("Friends List")

        for friend_username in friends:
            # Create a button for each friend that shows their username
            button = tk.Button(friends_window, text=friend_username, command=lambda u=friend_username: self.show_friend_profile(u))
            button.pack()

    def show_friend_profile(self, friend_username):
        # Use the load_profile function to get the friend's profile data
        profile_data = self.load_WHOLEprofile(friend_username)
        if profile_data is None:
            messagebox.showerror("Error", f"No profile data found for {friend_username}.")
            return

        # Create a new window to display the friend's profile information
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{friend_username}'s Profile")

        # Display the profile information
        for key, value in profile_data.items():
            tk.Label(profile_window, text=f"{key.capitalize()}: {value}").pack()
    
    def refresh_friends_list(self):
        # Assume self.current_user is the logged-in user's username
        friends_list = list_friends(self.current_user)


    def show_friend_requests(self):
        pending_requests = list_pending_requests(self.current_user)
        
        friend_requests_window = tk.Toplevel(self.root)
        friend_requests_window.title("Pending Friend Requests")
        
        for request_username in pending_requests:
            frame = tk.Frame(friend_requests_window)
            frame.pack()
            
            tk.Label(frame, text=request_username).pack(side=tk.LEFT)
            accept_btn = tk.Button(frame, text="Accept", command=lambda u=request_username: self.accept_fq(u))
            accept_btn.pack(side=tk.LEFT)
            reject_btn = tk.Button(frame, text="Reject", command=lambda u=request_username: self.reject_fq(u))
            reject_btn.pack(side=tk.LEFT)


    def accept_fq(self, friend_username):
        accept_friend_request(self.current_user, friend_username)
        messagebox.showinfo("Friend Request", f"You are now friends with {friend_username}.")
        self.show_friend_requests()
        self.refresh_friends_list()  # Refresh the list

    def reject_fq(self, friend_username):
        reject_friend_request(self.current_user, friend_username)
        messagebox.showinfo("Friend Request", f"Friend request from {friend_username} has been rejected.")
        self.show_friend_requests()  # Refresh the list
        self.refresh_friends_list()


    def view_friends_list(self):
        # This will open a new window with the current user's list of friends
        friends_list = list_friends(self.current_user)
        friends_window = tk.Toplevel(self.root)
        friends_window.title("My Friends")

        for friend in friends_list:
            tk.Label(friends_window, text=friend).pack()
    
    
    def send_friend_request_interface(self):
        to_username = simpledialog.askstring("Send Friend Request", "Enter the username to send a request to:")
        send_friend_request(self.current_user, to_username)
        messagebox.showinfo("Friend Request", f"Friend request sent to {to_username}.")

    

    
    def load_user_settings(self):
        # Load settings from a file or database
        # For demonstration, let's assume a simple file with comma-separated values
        try:
            with open('user_settings.txt', 'r') as file:
                settings = file.read().split(',')
                self.user_settings = {
                    'email': settings[0] == 'True',
                    'sms': settings[1] == 'True',
                    'advertising': settings[2] == 'True',
                    # Add other settings if necessary
                }
        except FileNotFoundError:
            # If the file does not exist, default settings are already set
            pass

    def save_user_settings(self):
        # Save settings to a file or database
        with open('user_settings.txt', 'w') as file:
            settings = [
                str(self.user_settings['email']),
                str(self.user_settings['sms']),
                str(self.user_settings['advertising']),
                # Add other settings if necessary
            ]
            file.write(','.join(settings))





    def privacy_policy(self):
        # Show privacy policy information
        messagebox.showinfo("Privacy Policy", "At InCollege, safeguarding your privacy is at the core of our commitment to providing a secure and enjoyable user experience. This Privacy Policy outlines the practices and principles governing the collection, utilization, and protection of your personal information. We collect data, such as your name, contact details, and user preferences, to enhance our services and personalize your inCollege experience. The information gathered is used solely for legitimate purposes, such as facilitating job searches and improving app functionality. We do not share your personal data with third parties without your explicit consent, except as required by law. Our security measures include encryption, access controls, and regular audits to protect your information from unauthorized access or disclosure. By continuing to use our app, you signify your understanding and acceptance of this Privacy Policy, as we continue to prioritize transparency and user trust in all our interactions.")
        # If user is logged in, show Guest Controls option
        if self.current_user:
            self.show_guest_controls()

    def show_guest_controls(self):
        # Create a Toplevel window for guest controls
        guest_controls_window = tk.Toplevel(self.root)
        guest_controls_window.title("Guest Controls")

        # Variables to hold the on/off state of each setting
        email_var = tk.BooleanVar(value=self.user_settings.get('email', True))
        sms_var = tk.BooleanVar(value=self.user_settings.get('sms', True))
        advertising_var = tk.BooleanVar(value=self.user_settings.get('advertising', True))

        # Checkbuttons for each setting
        email_cb = tk.Checkbutton(guest_controls_window, text="InCollege Email", variable=email_var)
        email_cb.pack()

        sms_cb = tk.Checkbutton(guest_controls_window, text="SMS", variable=sms_var)
        sms_cb.pack()

        advertising_cb = tk.Checkbutton(guest_controls_window, text="Targeted Advertising", variable=advertising_var)
        advertising_cb.pack()

        # Save button
        save_btn = tk.Button(guest_controls_window, text="Save Settings",
                            command=lambda: self.update_guest_controls(email_var, sms_var, advertising_var, guest_controls_window))
        save_btn.pack()

    def update_guest_controls(self, email_var, sms_var, advertising_var, window):
        # Update the user's settings
        self.user_settings['email'] = email_var.get()
        self.user_settings['sms'] = sms_var.get()
        self.user_settings['advertising'] = advertising_var.get()
        
        # Save the updated settings
        self.save_user_settings()

        # Close the guest controls window
        window.destroy()

        # Confirmation message
        messagebox.showinfo("Settings Updated", "Your guest control settings have been updated.")

    
    
    def show_success_story(self):
        """Show the success story and 'Watch Video' button."""
        self.success_story_label.pack()
        self.watch_video_button.pack()

    def hide_success_story(self):
        """Hide the success story and 'Watch Video' button."""
        self.success_story_label.pack_forget()
        self.watch_video_button.pack_forget()


    def play_video(self):
        # URL to the video
        video_url = "https://drive.google.com/file/d/1UztP8JWQvTD0wZZ3HkKGtPNXhLRB3Jaa/view?usp=sharing"  # Replace with your video URL
        
        # Open the video URL with the default web browser
        webbrowser.open(video_url)
        messagebox.showinfo("Play Video", "Video is now playing in your web browser.")
    
    
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
        if len(jobs) >= 10:
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

        # Pass individual components of job_post to save_job
        self.save_job(
            title=job_post['title'],
            description=job_post['description'],
            employer=job_post['employer'],
            location=job_post['location'],
            salary=job_post['salary'],
            username=job_post['username']
        )
        messagebox.showinfo("Success", "Job posted successfully.")
        window.destroy()


    def delete_job(self, job_title):
        jobs = self.load_jobs()
        job_deleted = False

        # Find the job with the given title and remove it
        new_jobs = []
        for job in jobs:
            if job[0].lower() == job_title.lower():
                job_deleted = True
            else:
                new_jobs.append(job)

        # Save the updated job list
        with open(JOB_FILE, "w") as file:
            for job in new_jobs:
                file.write(",".join(job) + "\n")

        # If a job was deleted, notify the students who had applied for it
        if job_deleted:
            self.notify_job_deleted(job_title)

    def notify_job_deleted(self, job_title):
        # Retrieve all applied jobs
        applied_jobs = self.load_applied_jobs()
        for username, jobs in applied_jobs.items():
            if job_title in jobs:
                # Create a notification for the user about the deletion of the job
                self.create_notification(username, f"A job that you applied for has been deleted: {job_title}")
                # Remove the deleted job from the user's applied jobs list
                jobs.remove(job_title)



    def show_jobs_window(self):
        # Load jobs from the file
        jobs = self.load_jobs()

        num_applied_jobs = len(self.load_applied_jobs().get(self.current_user, []))

        # Notify the user of the number of applied jobs
        messagebox.showinfo("Jobs Applied", f"You have currently applied for {num_applied_jobs} jobs.")


        jobs_window = tk.Toplevel(self.root)
        jobs_window.title("Available Jobs")

        # Display each job with 'Apply' and 'Save' buttons
        for job in jobs:
            job_frame = tk.Frame(jobs_window)
            job_frame.pack(fill='x', padx=5, pady=5)
            
            job_id = job[0] # Assuming the first element is the job ID
            tk.Label(job_frame, text=f"Title: {job[1]}, Employer: {job[3]}, Location: {job[4]}, Salary: {job[5]}").pack(side='left')

            apply_button = tk.Button(job_frame, text="Apply", command=lambda j=job_id: self.apply_for_job(j))
            apply_button.pack(side='right')

            save_button = tk.Button(job_frame, text="Save", command=lambda j=job_id: self.save_job_for_later(j))
            save_button.pack(side='right')

    def apply_for_job(self, job_id):
    # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "You need to log in to apply for a job.")
            return

        # Save the applied job
        self.save_applied_jobs(self.current_user, job_id)
        messagebox.showinfo("Success", f"You have applied for job {job_id}.")

    def save_job_for_later(self, job_id):
        # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "You need to log in to save a job.")
            return

        # Save the saved job
        self.save_saved_jobs(self.current_user, job_id)
        messagebox.showinfo("Success", f"You have saved job {job_id} for later.")

    def show_saved_jobs(self):
        # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "You need to log in to see saved jobs.")
            return

        saved_jobs = self.load_saved_jobs().get(self.current_user, [])
        saved_jobs_str = "\n".join(saved_jobs)

        saved_jobs_window = tk.Toplevel(self.root)
        saved_jobs_window.title("Saved Jobs")

        if saved_jobs_str:
            tk.Label(saved_jobs_window, text="Saved Jobs:").pack()
            tk.Label(saved_jobs_window, text=saved_jobs_str).pack()
        else:
            tk.Label(saved_jobs_window, text="You have no saved jobs.").pack()

    def show_applied_jobs(self):
        # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "You need to log in to see applied jobs.")
            return

        applied_jobs = self.load_applied_jobs().get(self.current_user, [])
        applied_jobs_str = "\n".join(applied_jobs)

        applied_jobs_window = tk.Toplevel(self.root)
        applied_jobs_window.title("Applied Jobs")

        if applied_jobs_str:
            tk.Label(applied_jobs_window, text="Applied Jobs:").pack()
            tk.Label(applied_jobs_window, text=applied_jobs_str).pack()
        else:
            tk.Label(applied_jobs_window, text="You have not applied for any jobs.").pack()


    def save_applied_jobs(self, username, job_id):
        # Load current applied jobs
        applied_jobs = self.load_applied_jobs()
        # Add the new job if not already applied
        if job_id not in applied_jobs.get(username, []):
            applied_jobs.setdefault(username, []).append(job_id)
        # Save the updated applied jobs
        with open(APPLIED_JOBS_FILE, "w") as file:
            json.dump(applied_jobs, file)

    def load_applied_jobs(self):
        try:
            with open(APPLIED_JOBS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_saved_jobs(self, username, job_id):
        # Load current saved jobs
        saved_jobs = self.load_saved_jobs()
        # Add the new job if not already saved
        if job_id not in saved_jobs.get(username, []):
            saved_jobs.setdefault(username, []).append(job_id)
        # Save the updated saved jobs
        with open(SAVED_JOBS_FILE, "w") as file:
            json.dump(saved_jobs, file)

    def load_saved_jobs(self):
        try:
            with open(SAVED_JOBS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}



    def logout(self):
        self.current_user = None  # Reset current_user on logout
        self.user_display_label.config(text="Not logged in") 
        self.show_success_story()
        self.job_menu.entryconfig("Post a Job", state="disabled")
        self.hide_user_profile()
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


    def get_account_type(self, username):
        with open(ACCOUNT_FILE, "r") as file:
            for line in file:
                account_info = line.strip().split(',')
                if account_info[0] == username:
                    # Assuming the account type is the 7th element in the line
                    return account_info[6]  # This could be "Plus" or "Standard"
        return "Unknown"

    def login(self):
        username = simpledialog.askstring("Log In", "Enter your username:", parent=self.root)
        password = simpledialog.askstring("Log In", "Enter your password:", parent=self.root, show='*')
        if self.verify_login_credentials(username, password):
            self.current_user = username  # Set current_user to the logged-in username
            #notify_new_students(username)
            #update_last_login(username)  
            account_type = self.get_account_type(username)  # Function to determine the account type
            account_type_label_text = f"{account_type} Account"
            self.account_type_label.config(text=account_type_label_text)  # Update a label on the main screen with this text
            self.check_job_application_reminder()
            self.check_new_messages()

            try:
                with open("new_students.json") as file:
                    new_students = json.load(file)
                    if new_students:  # Check if there are new students
                        new_students_str = ", ".join(new_students)
                        messagebox.showinfo("New Students", f"{new_students_str} have joined InCollege", parent=self.root)
                        # Clear the list after showing
                        with open("new_students.json", "w") as clear_file:
                            json.dump([], clear_file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            #self.notify_new_jobs()
            if self.current_user and not self.is_profile_complete(self.current_user):
                messagebox.showinfo("Incomplete Profile", "Don't forget to complete your profile.")
            if self.messaging_system.is_plus_member(username):
                self.create_send_message_to_anyone_button()
            messagebox.showinfo("Login Successful", "You have successfully logged in")
            
            # Assuming self.job_menu is your job-related menu and "Post a Job" is a direct item of this menu
            self.job_menu.entryconfig("Post a Job", state="normal")  # Enable the "Post a Job" option

            self.user_display_label.config(text=f"Logged in as: {username}")
            self.hide_success_story()
            self.display_user_profile()
            
            # Potentially update UI or show/hide certain features based on login status
        else:
            messagebox.showerror("Login Failed", "Incorrect username/password, please try again")


        
    def create_account_window(self):
        accounts = load_accounts()
        if len(accounts) >= 10:
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

        Label(window, text="University:").pack()
        uni_entry = Entry(window)
        uni_entry.pack()

        Label(window, text="Major:").pack()
        major_entry = Entry(window)
        major_entry.pack()

        plus_account_var = BooleanVar(value=False)
        plus_account_check = Checkbutton(window, text="Sign up for Plus account ($10/month)", variable=plus_account_var)
        plus_account_check.pack()

        Button(window, text="Sign Up", command=lambda: self.create_account(
            username=username_entry.get(), 
            password=password_entry.get(), 
            first_name=first_name_entry.get(), 
            last_name=last_name_entry.get(), 
            university=uni_entry.get(), 
            major=major_entry.get(), 
            plus_account=plus_account_var.get(),  # Pass the state of the checkbox
            accounts=accounts, 
            window=window
        )).pack()

    def create_account(self, username, password, first_name, last_name, university, major, plus_account, accounts, window):
        if any(acc[0] == username for acc in accounts):
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
            return
        if not is_password_valid(password):
            messagebox.showerror("Error", "Password does not meet criteria.")
            return
        if plus_account:
            messagebox.showinfo("Plus Account", "You have selected a Plus account. You will be billed $10/month.")
        else:
            messagebox.showinfo("Standard Account", "You have selected a Standard account.")
        
        save_account(username, password, first_name, last_name, university, major, plus_account)
        messagebox.showinfo("Success", "Account created successfully.")
        window.destroy()

    def find_person_window(self):
        window = Toplevel(self.root)
        window.title("Find Someone You Know")

        Label(window, text="Last Name:").pack()
        last_name_entry = Entry(window)
        last_name_entry.pack()

        Label(window, text="University:").pack()
        uni_entry = Entry(window)
        uni_entry.pack()

        Label(window, text="Major:").pack()
        major_entry = Entry(window)
        major_entry.pack()

        def search():
            last_name = last_name_entry.get().strip().lower()
            uni = uni_entry.get().strip().lower()
            maj = major_entry.get().strip().lower()
            accounts = load_accounts()
            person_found = False
            for account in accounts:
                # Ensure the fields are compared correctly after stripping and converting to lower case
                if (account[3].lower() == last_name and 
                    account[4].lower() == uni and 
                    account[5].lower() == maj):
                    person_found = True
                    found_account = account
                    break

            if person_found:
        # Ask the user if they want to send a friend request
                response = messagebox.askyesno("Search Result", f"{found_account[2]} {found_account[3]} is a part of the InCollege system. Do you want to send a friend request?")
                if response:
                    send_friend_request(self.current_user[0], found_account[0])
                    messagebox.showinfo("Friend Request", "Friend request sent!")
                else:
                    messagebox.showinfo("Friend Request", "No friend request sent.")
            else:
                messagebox.showinfo("Search Result", f"No user from {uni} studying {maj} with the last name {last_name} is found in the InCollege system.")
            
            window.destroy()
        
        Button(window, text="Search", command=search).pack()

    def invite_to_join(self, first_name, last_name):
        invite_window = Toplevel(self.root)
        invite_window.title("Invite to Join InCollege")

        Label(invite_window, text=f"Invite {first_name} {last_name} to connect with you on InCollege.").pack()
        Button(invite_window, text="Log In", command=self.login).pack()
        Button(invite_window, text="Sign Up", command=self.create_account_window).pack()

    def change_language(self):
        if not self.current_user:
            messagebox.showinfo("Not logged in", "You must be logged in to change the language.")
            return

        # Ask the user to choose a language
        language = simpledialog.askstring("Select Language", "Type 'English' or 'Spanish':")
        
        if language not in ['English', 'Spanish']:
            messagebox.showerror("Invalid Selection", "Please select either 'English' or 'Spanish'.")
            return

        self.user_settings['language'] = language
        self.save_user_settings()
        messagebox.showinfo("Language Changed", f"Language set to {language}.")





    '''Print Menu Items Information EPIC 3'''

    def show_copyright_notice(self):
        messagebox.showerror("Copyright Notice", "This application is presented by the USF’s Software Engineering Green Team and is protected by copyright laws. Distribution of this resource without written permission of the sponsor is prohibited.\n© 2024 Hetvi Shah, Austin Molketin, Silvana Chain Marulanda, Dat Nguyen, Boburjon Usmonov")

    def show_help_center(self):
        messagebox.showinfo("Help Center", "We're here to help.")

    def show_about(self):
        messagebox.showinfo("About", "Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.")
        messagebox.showinfo("Our Vision: Empowering Students to Shape Their Future", "We envision a world where every college student has direct access to the tools and connections necessary to forge a successful career path. InCollege is more than just a software package; it's the commencement of potential, a network of opportunity, and a community of like-minded individuals committed to professional growth.")
        messagebox.showinfo("Contact Us", "To learn more about InCollege or to provide support for our venture, please reach out to one of our team members.\nHetvi Shah: hetvi@usf.edu\nAustin Molketin: amolketin@usf.edu\nSilvana Chain Marulanda: smchain@usf.edu\nDat Nguyen: dnguyen182@usf.edu\nBoburjon Usmonov: boburjon@usf.edu\nLet's build the future of student professional development together.")
    

    def show_accessibility(self):
        messagebox.showinfo("Accessibility","At inCollege, we prioritize accessibility to ensure an inclusive job search experience for all college students. Our app features accessibility options, including screen reader compatibility, customizable text settings, and simplified navigation, making it user-friendly for individuals with diverse needs. Alt text for images and color contrast options are incorporated to enhance accessibility further. We are dedicated to creating an environment where every college student, regardless of abilities, can effortlessly utilize our platform to explore and pursue career opportunities.")

    def show_user_agreement(self):
        messagebox.showinfo("User Agreement", "By using the InCollege platform, users agree to abide by the following terms and conditions: 1.Users must provide accurate and truthful information when creating an account and using the platform. 2.Users are responsible for maintaining the confidentiality of their account credentials and for all activities that occur under their account. 3.Users must respect the rights of other users and refrain from engaging in any form of harassment, bullying, or discrimination. 4.Users must not use the platform for any illegal or unauthorized purposes, including but not limited to spamming, phishing, or distributing malware. 5.Users retain ownership of the content they share on InCollege but grant the platform a non-exclusive,royalty-free license to use, reproduce, and distribute their content for the purpose of operating and promoting the platform. 6.InCollege reserves the right to remove any content or suspend/terminate any account that violates these terms or is deemed inappropriate or harmful to the community. 7.By using InCollege, users acknowledge and agree to these terms and conditions. Violation of the User Agreement may result in the suspension or termination of the users account without prior notice.")
  


    def show_cookie_policy(self):
        messagebox.showinfo("cookie","At InCollege, we value your privacy and strive to be transparent about our use of cookies. Cookies are small data files stored on your device to enhance your experience on our platform by remembering your preferences and visits. We use them to ensure our website functions correctly, to analyze our traffic, and to personalize content and ads. By using the InCollege platform, you consent to the use of cookies in accordance with our Privacy Policy. For more information on how we use cookies and how you can manage them, please visit our full Cookie Policy page.")


    def show_copyright_policy(self):
        messagebox.showinfo("copyright policy",'The Copyright Policy of InCollege states that all content shared on the platform, including but not limited to text, images, videos, and documents, is subject to copyright protection. Users must ensure they have the necessary rights or permissions to share any content on InCollege. Infringement of copyright will result in the removal of the infringing content and may lead to the suspension or termination of the users account')

    def show_brand_policy(self):
        messagebox.showinfo("brand","InCollege is committed to protecting its brand integrity and the trust of its users. Our Brand Policy ensures that all representations of InCollege's name, logos, and other brand elements are used correctly and only with our prior written consent. This policy applies to all marketing, communication, and promotional materials both online and offline. Unauthorized use, imitation, or modification of our brand assets is strictly prohibited. If you wish to use our brand in any way, please contact us to obtain permission. Our team will provide the necessary guidelines to maintain the strength and consistency of our brand identity.")


    def show_press(self):
        messagebox.showinfo("Pressroom", "Stay on top of the latest news, updates, and reports")

    def show_under_construction(self):
        messagebox.showinfo("Under Construction", "This feature is under construction.")







    # epic 5
        
    def load_profile(self, username):
        with open('accounts.txt', 'r') as file:
            for line in file:
                account_info = line.strip().split(',')
                if account_info[0] == username:
                    return {
                        'university': account_info[4],
                        'major': account_info[5],
                        #'information':account_info[6],
                        #'experience':account_info[7],
                        #'education':account_info[8]
                    }
        return None
    

    def load_WHOLEprofile(self, username):
        with open('accounts.txt', 'r') as file:
            for line in file:
                account_info = line.strip().split(',')
                if account_info[0] == username:
                    return {
                        'university': account_info[4],
                        'major': account_info[5],
                        'information':account_info[6],
                        'experience':account_info[7],
                        'education':account_info[8]
                    }
        return None
    

    def display_user_profile(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to view a profile.")
            return

        profile_data = self.load_profile(self.current_user)
        if profile_data is None:
            messagebox.showerror("Error", "Profile data not found.")
            return

        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{self.current_user}'s Profile")

        # Display the profile information
        for key, value in profile_data.items():
            tk.Label(profile_window, text=f"{key.capitalize()}: {value}").pack()

    def edit_user_profile(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to edit a profile.")
            return

        profile_data = self.load_profile(self.current_user)
        if profile_data is None:
            messagebox.showerror("Error", "Profile data not found.")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit {self.current_user}'s Profile")

        # Create entry widgets for each profile field and pre-fill with current data
        entries = {}
        fields = ['university', 'major', 'information', 'experience', 'education']
        for field in fields:
            tk.Label(edit_window, text=f"{field.capitalize()}:").pack()
            entry_value = profile_data.get(field, '')  # Get the current value or an empty string if not found
            entry = tk.Entry(edit_window)
            entry.insert(0, entry_value)
            entry.pack()
            entries[field] = entry
                
        def save_edited_profile():
            # Collect the data from the entries
                for field, entry in entries.items():
                    profile_data[field] = entry.get()
                # Save the profile data
                self.save_profile(profile_data)
                edit_window.destroy()

        tk.Button(edit_window, text="Save", command=save_edited_profile).pack()


    def save_profile(self, updated_profile_data):
        updated_accounts = []
        profile_updated = False
        if not self.is_profile_complete(self.current_user):
            messagebox.showinfo("Incomplete Profile", "Please complete all the necessary profile fields.")

        with open('accounts.txt', 'r') as file:
            for line in file:
                account_info = line.strip().split(',')
                # Check if this is the account to update
                if account_info[0] == self.current_user:
                    # Update the account info with the new profile data
                    account_info = [
                        self.current_user,  # Keep the username
                        account_info[1],  # Keep the password
                        account_info[2],  # Keep the first name
                        account_info[3],  # Keep the last name
                        updated_profile_data.get('university', account_info[4]),
                        updated_profile_data.get('major', account_info[5]),
                        updated_profile_data.get('information', ''),
                        updated_profile_data.get('experience', ''),
                        updated_profile_data.get('education', '')
                    ]
                    profile_updated = True
                updated_accounts.append(','.join(account_info))

        # Check if the profile was found and updated; if not, handle appropriately
        if not profile_updated:
            messagebox.showerror("Error", "Failed to update profile. User not found.")
            return

        # Write the updated accounts back to the file
        with open('accounts.txt', 'w') as file:
            for account in updated_accounts:
                file.write(f"{account}\n")

        messagebox.showinfo("Success", "Profile updated successfully.")

        


if __name__ == "__main__":
    root = tk.Tk()
    app = InCollegeGUI(root)
    root.mainloop()
