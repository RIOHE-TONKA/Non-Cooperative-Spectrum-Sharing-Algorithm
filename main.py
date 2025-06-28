import random
import matplotlib.pyplot as plt
from collections import deque
import time

# Define initial parameters
channels = [None] * 5  # 5 channels, initially empty
user_counter = {"PU": 0, "SU": 0}  # To track user identifiers
pu_queue = deque()  # Queue for PUs
su_queue = deque()  # Queue for SUs
occupancy_times = {}  # {user_id: total_time} to track occupancy time in seconds
fairness_history = []  # Track fairness index over time

# Function to calculate Jain's Fairness Index
def jains_fairness_index(resource_allocations):
    n = len(resource_allocations)
    if n == 0:
        return 0.0  # Fairness should be 0 when there are no users
    total_alloc = sum(resource_allocations)
    square_of_sum = total_alloc ** 2
    sum_of_squares = sum([x ** 2 for x in resource_allocations])
    return square_of_sum / (n * sum_of_squares) if sum_of_squares > 0 else 0

# Function to update the occupancy times of users
def update_occupancy_times():
    for user_id in occupancy_times:
        if user_id in channels:
            occupancy_times[user_id] += 1  # Increment the occupancy time by 1 second

# Function to calculate fairness based on occupancy times
def calculate_fairness():
    resource_allocations = [time for time in occupancy_times.values()]
    return jains_fairness_index(resource_allocations)

# Function to randomly shuffle SU channel checks
def random_su_channel_check():
    return random.sample(range(5), 5)  # Randomly shuffle the indices of the 5 channels

# Function to check if a channel is occupied by a PU or SU
def check_channel_availability():
    return [channel for channel in channels if channel is None]

# Function to assign a user to a channel with an identifier
def assign_channel(user_type, user_id=None):
    if user_type == "SU":
        available_channel_indices = random_su_channel_check()  # Shuffle for SUs
    else:
        available_channel_indices = range(5)  # PUs check channels sequentially

    for channel_index in available_channel_indices:
        if channels[channel_index] is None:
            if user_id is None:  # If user_id not provided, create one
                user_counter[user_type] += 1  # Increment user ID counter
                user_id = f"{user_type}{user_counter[user_type]}"
            
            # Start tracking the user's occupancy time
            occupancy_times[user_id] = 0  # Set initial total time to 0
            channels[channel_index] = user_id
            update_occupancy_times()  #Update times before calculating fairness
            
            # Calculate fairness after assignment
            fairness = calculate_fairness()
            fairness_history.append(fairness)  # Track fairness over time
            
            # Print fairness info after assignment
            print(f"Fairness after assignment: {fairness:.2f}")
            
            # Display occupancy per user
            display_occupancy_per_user()
            
            return True, channel_index, user_id
    
    return False, None, None

# Function to reassign a channel occupied by SU to PU
def reassign_su_for_pu():
    for i, user in enumerate(channels):
        if user and user.startswith("SU"):  # Find a channel occupied by SU
            print(f"Secondary User {user} on channel {i + 1} was removed to accommodate Primary User.")
            su_queue.append(user)  # Add SU back to the queue when removed
            channels[i] = None  # Remove the SU
            return True, i
    return False, None

# Function to add users to the appropriate queue
def queue_user(user_type):
    user_counter[user_type] += 1
    user_id = f"{user_type}{user_counter[user_type]}"
    if user_type == "PU":
        pu_queue.append(user_id)
        print(f"Primary User {user_id} added to queue.")
    else:
        su_queue.append(user_id)
        print(f"Secondary User {user_id} added to queue.")

# Function to display occupancy per user
def display_occupancy_per_user():
    print("Current Occupancy Per User (in seconds):")
    print("-----------------------------------------")
    for user_id, time in occupancy_times.items():
        print(f"{user_id}: {time} seconds")
    print("-----------------------------------------")

# Function to simulate users arriving
def simulate_user_arrival(user_type):
    if user_type == "PU":  # Check if PU needs priority
        assigned, channel_index, user_id = assign_channel(user_type)
        if assigned:
            print(f"Primary User {user_id} assigned to channel {channel_index + 1}.")
        else:
            # Try to free a channel occupied by SU if no empty channels are available
            reassigned, channel_index = reassign_su_for_pu()
            if reassigned:
                user_counter["PU"] += 1
                channels[channel_index] = f"PU{user_counter['PU']}"  # Assign the new PU to that channel
                print(f"Primary User {channels[channel_index]} assigned to channel {channel_index + 1}. (Priority Access)")
            else:
                queue_user(user_type)  # Queue PU if no available channels and no SUs to remove
    else:
        assigned, channel_index, user_id = assign_channel(user_type)
        if assigned:
            print(f"Secondary User {user_id} assigned to channel {channel_index + 1}.")
        else:
            queue_user(user_type)  # Queue SU if no available channels

# Function to handle user queues automatically when a channel becomes available
def process_user_queue():
    available_channels = check_channel_availability()
    if not (pu_queue or su_queue):  # Only process if there are users in the queues
        print("No users in the queue to process.")
        return
    
    while available_channels:
        if pu_queue:  # Process PU queue first
            user_id = pu_queue.popleft()
            assigned, channel_index, user_id = assign_channel("PU", user_id)
            if assigned:
                print(f"Primary User {user_id} from queue assigned to channel {channel_index + 1}.")
        elif su_queue:  # Then process SU queue
            user_id = su_queue.popleft()
            assigned, channel_index, user_id = assign_channel("SU", user_id)
            if assigned:
                print(f"Secondary User {user_id} from queue assigned to channel {channel_index + 1}.")
        available_channels = check_channel_availability()  # Check again if there are any more available channels

# Function to remove a user from the spectrum
def remove_user(user_id):
    if user_id in occupancy_times:
        channel_index = None
        # Search for the user in the channels list
        for i, user in enumerate(channels):
            if user == user_id:
                channel_index = i
                break

        if channel_index is not None:
            print(f"User {user_id} removed from channel {channel_index + 1}.")
            channels[channel_index] = None
            occupancy_times.pop(user_id, None)  # Remove from occupancy times
            
            process_user_queue()  # Automatically process the queue when a user is removed
            
            update_occupancy_times()  # Update times after user removal
            
            # Calculate fairness after removal
            fairness = calculate_fairness()
            fairness_history.append(fairness)  # Track fairness over time
            print(f"Fairness after removal: {fairness:.2f}")
            print("---------------------------------------")
        else:
            print(f"User {user_id} not found in any channel.")
    else:
        print(f"User {user_id} not found.")

# Plot the current spectrum usage with user IDs in the middle of the bars
def plot_spectrum_usage():
    plt.figure(figsize=(10, 5))
    labels = ['Channel ' + str(i) for i in range(1, 6)]
    
    # Define the heights of the bars: 1 for PU, 0.5 for SU, 0 for empty channels
    bar_heights = [1 if ch and ch.startswith("PU") else (1 if ch and ch.startswith("SU") else 0) for ch in channels]
    
    # Define the colors for the bars: blue for PU, green for SU, red for empty channels
    bar_colors = ['Blue' if ch and ch.startswith("PU") else ('Green' if ch and ch.startswith("SU") else 'Purple') for ch in channels]
    
    # Plot the bar chart
    plt.bar(labels, bar_heights, color=bar_colors)
    plt.ylim(0, 1.5)
    plt.xlabel("Channels")
    plt.ylabel("Occupancy (PU=1, SU=1, Empty=0)")
    plt.title("Spectrum Channel Occupancy")
    
    # Add user IDs at the center of the bars
    for i, user in enumerate(channels):
        if user:  # Only add text for occupied channels
            bar_height = 1 if user.startswith("PU") else 1
            plt.text(i, bar_height / 2, user, ha='center', va='center', color='white', fontsize=12)
    
    plt.show()

# Plot the fairness history
def plot_fairness_history():
    plt.figure(figsize=(8, 5))
    plt.plot(fairness_history, marker='o', color='blue')
    plt.xlabel("Time Steps")
    plt.ylabel("Jain's Fairness Index")
    plt.title("Fairness Index Over Time")
    plt.ylim(0, 1.0)
    plt.grid(True)
    plt.show()

# Function to print current users and queue
def print_current_users():
    print("Current Channel Occupancy:")
    print("--------------------------")
    for i, user in enumerate(channels):
        if user is not None:
            print(f"Channel {i + 1}: {user}")
        else:
            print(f"Channel {i + 1}: Empty")

def print_queue():
    print("Primary User Queue:", list(pu_queue))
    print("Secondary User Queue:", list(su_queue))

# Function to simulate the real-time interaction loop
def add_or_remove_users():
    start_time = time.time()  # Track the start time
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # Update occupancy times every second
        if elapsed_time >= 1:
            update_occupancy_times()
            start_time = current_time  # Reset start time
        
        action = input("Enter 'add' to add a user, 'remove' to remove a user, 'queue' to check the queue, 'plot' to plot fairness index, or 'exit' to stop: ").strip().lower()
        
        if action == 'exit':
            print("Simulation ended.")
            break
        
        if action == 'add':
            user_type = input("Enter user type (PU for Primary User, SU for Secondary User): ").strip().upper()
            if user_type in ["PU", "SU"]:
                try:
                    simulate_user_arrival(user_type)
                    plot_spectrum_usage()
                    print_current_users()
                    print_queue()  # Print queue status after adding a user
                except Exception as e:
                    print(f"Error while adding user: {e}")
            else:
                print("Invalid input, please enter 'PU' for Primary User or 'SU' for Secondary User.")
        
        elif action == 'remove':
            user_id = input("Enter the user ID to remove (e.g., PU1, SU1): ").strip().upper()
            try:
                remove_user(user_id)
                plot_spectrum_usage()
                print_current_users()
                print_queue()  # Print queue status after removing a user
            except Exception as e:
                print(f"Error while removing user: {e}")
        
        elif action == 'queue':
            print_queue()  # Just print the current queue
        
        elif action == 'plot':
            plot_fairness_history()  # Plot the fairness index history
        
        # Display the updated fairness
        fairness = calculate_fairness()
        print(f"\nUpdated Jain's Fairness Index: {fairness:.2f}\n")

# Run the simulation
add_or_remove_users()


#------------FINAL-------------
