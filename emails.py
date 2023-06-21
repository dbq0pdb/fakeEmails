import random
import csv
import string
import time
import datetime


def load_usernames():
    with open('usernames.txt', 'r', errors='ignore') as usernames_file:
        usernames = [line.strip().lower() for line in usernames_file]
    return usernames


def generate_random_email(usernames):
    common_names = ["james", "john", "robert", "michael", "william", "david", "richard", "charles", "joseph", "thomas"]
    
    # Choose a username or a common name
    base = random.choice(usernames + common_names)

    # Occasionally add another username or common name
    if random.random() < 0.3:
        second_base = random.choice(usernames + common_names)
        separator = random.choice(['.', '_'])
        base = f"{base}{separator}{second_base}"

    # Limit the base to 20 characters
    base = base[:20].lower()

    # Occasionally append a number at the end
    if random.random() < 0.6:
        base += str(random.randint(1, 99))

    # Choose a domain
    domain_choices = [
        "@gmail.com",
        "@yahoo.com",
        "@outlook.com",
        "@hotmail.com",
        "@icloud.com",
        "@protonmail.com",
        "@live.com",
        "@mail.com",
        "@me.com",
        "@mac.com"
    ]
    domain = random.choice(domain_choices)

    return f"{base}{domain}"


# Load usernames into memory
usernames = load_usernames()

# Generate 10,000 random emails
emails = []
start_time = time.time()
for _ in range(5000):
    email = generate_random_email(usernames)
    emails.append([email])
end_time = time.time()
elapsed_time = end_time - start_time

# Export emails to CSV file
with open('emails.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(emails)

# Display statistics
print("------------------------")
print("CSV file 'emails.csv' created.")
print(f"Number of generated emails: {len(emails)}")
print(f"Elapsed time: {datetime.timedelta(seconds=elapsed_time)}")
print("------------------------")
