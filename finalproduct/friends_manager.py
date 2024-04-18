# friends_manager.py

import json

# Assuming ACCOUNT_FILE stores all the account info
ACCOUNT_FILE = 'accounts.txt'
FRIENDS_FILE = 'friends.json'
FRIEND_REQUESTS_FILE = 'friend_requests.json'

# Function to send a friend request
def send_friend_request(from_username, to_username):
    friend_requests = load_friend_requests()
    if from_username != to_username and from_username not in friend_requests.get(to_username, []):
        friend_requests.setdefault(to_username, []).append(from_username)
        save_friend_requests(friend_requests)

def accept_friend_request(username, friend_username):
    friends = load_friends()
    friend_requests = load_friend_requests()

    # Add each other to their friends' lists
    if friend_username in friend_requests.get(username, []):
        friends[username] = friends.get(username, []) + [friend_username]
        friends[friend_username] = friends.get(friend_username, []) + [username]

        # Remove the accepted friend request from both sides
        friend_requests[username].remove(friend_username)
        # It's possible that both users sent a request to each other, so check for that too
        if username in friend_requests.get(friend_username, []):
            friend_requests[friend_username].remove(username)

        save_friends(friends)
        save_friend_requests(friend_requests)


def reject_friend_request(username, friend_username):
    friend_requests = load_friend_requests()
    
    if friend_username in friend_requests.get(username, []):
        friend_requests[username].remove(friend_username)
        save_friend_requests(friend_requests)

# Function to list friends
def list_friends(username):
    # Load friends
    friends = load_friends()

    # Return the list of friends for the username
    return friends.get(username, [])

# Function to list pending friend requests
def list_pending_requests(username):
    # Load friend requests
    friend_requests = load_friend_requests()

    # Return the list of pending friend requests for the username
    return friend_requests.get(username, [])

def load_friends():
    try:
        with open(FRIENDS_FILE, 'r') as file:
            data = file.read()
            # If the file is not empty, return the JSON data
            if data:
                return json.loads(data)
            else:
                # Return an empty dictionary if the file is empty
                return {}
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        return {}
    except json.JSONDecodeError:
        # Return an empty dictionary if there is a JSON decode error
        return {}

# Helper function to save friends to file
def save_friends(friends):
    with open(FRIENDS_FILE, 'w') as file:
        json.dump(friends, file)

def load_friend_requests():
    try:
        with open(FRIEND_REQUESTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Helper function to save friend requests to file
def save_friend_requests(friend_requests):
    with open(FRIEND_REQUESTS_FILE, 'w') as file:
        json.dump(friend_requests, file)



