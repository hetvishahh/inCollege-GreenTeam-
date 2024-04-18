import json
import tkinter as tk
import os 


class MessagingSystem:
    def __init__(self):
        self.messages_file = 'messages.json'
        self.user_types_file = 'user_types.json'
        self.messages = self.load_messages()
        self.user_types = self.load_user_types()

    def load_messages(self):
        try:
            with open(self.messages_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_user_types(self):
        try:
            with open(self.user_types_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'standard': [], 'plus': []}

    def save_messages(self):
        with open(self.messages_file, 'w') as file:
            json.dump(self.messages, file)

    def save_user_types(self):
        with open(self.user_types_file, 'w') as file:
            json.dump(self.user_types, file)

    def add_user(self, username, user_type='standard'):
        self.user_types[user_type].append(username)
        self.save_user_types()

    def send_message(self, from_user, to_user, message):
        # Use the messaging system to send the message
        if self.can_send_message(from_user, to_user):
            self.messages.setdefault(to_user, []).append({'from': from_user, 'message': message})
            self.save_messages()
            return "Message sent."
            self.message_window.destroy()
        else:
            return "You cannot send a message to this user."
        
    def load_friends(self):
        try:
            with open('friends.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_friends(self, friends_data):
        with open('friends.json', 'w') as file:
            json.dump(friends_data, file)


    def can_send_message(self, from_user, to_user):
        # Load the friends data
        friends = self.load_friends()
        
        # Check if to_user is in from_user's friends list or vice versa
        return to_user in friends.get(from_user, []) or from_user in friends.get(to_user, [])
    
    def get_friends(self, user):
        friends_data = self.load_friends()
        return friends_data.get(user, [])

    
    def get_messages_for_user(self, username):
        # Retrieve messages for the specified user
        return self.messages.get(username, [])
    
    def get_all_usernames(self):
        # This function assumes that the 'accounts.txt' file stores usernames as the first entry in each comma-separated line
        usernames = []
        with open('accounts.txt', 'r') as file:
            for line in file:
                usernames.append(line.split(',')[0])  # Get the username which is the first element
        return usernames



    def is_plus_member(self, user):
        # Assume the seventh field in the line indicates the account type
        with open('accounts.txt', 'r') as file:
            for line in file:
                account_info = line.strip().split(',')
                if account_info[0] == user:  # username is in the first position
                    return account_info[6].lower() == 'plus'  # Check if the type is 'Plus'
        return False  # Return False if the user is not found or is not a Plus member
    

    def send_message_as_plus(self, from_user, to_user, message):
        # Check if 'from_user' is a Plus member first
        if not self.is_plus_member(from_user):
            return f"{from_user} is not a Plus member and cannot send messages to non-friends."

        # Check if 'to_user' exists in the system (exists in accounts.txt)
        if not self.user_exists(to_user):
            return f"{to_user} does not exist in the system."

        # If 'from_user' is a Plus member and 'to_user' exists, send the message
        self.messages.setdefault(to_user, []).append({'from': from_user, 'message': message})
        self.save_messages()
        return "Message sent."

    def user_exists(self, username):
        # Check if a user exists in accounts.txt
        with open('accounts.txt', 'r') as accounts_file:
            for line in accounts_file:
                account_info = line.strip().split(',')
                if account_info[0] == username:
                    return True
        return False  # Return False if the user is not found