import random
import csv
import string
import time
import datetime
import os
import threading
import multiprocessing as mp

def load_usernames():
    with open('usernames.txt', 'r', errors='ignore') as usernames_file:
        usernames = [line.strip().lower() for line in usernames_file]
    return usernames

def get_domain_choices():
    top_domains = [
        "@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@icloud.com",
        "@protonmail.com", "@live.com", "@mail.com", "@me.com", "@mac.com"
    ]
    other_domains = [
        "@aol.com", "@msn.com", "@comcast.net", "@verizon.net", "@att.net",
        "@charter.net", "@cox.net", "@sbcglobal.net", "@netzero.net", "@earthlink.net",
        "@optonline.net", "@frontiernet.net", "@centurylink.net", "@windstream.net",
        "@bellsouth.net", "@embarqmail.com", "@rr.com", "@twc.com", "@cogeco.ca",
        "@rogers.com", "@shaw.ca", "@telus.net", "@mymts.net"
    ]

    while True:
        user_choice = input("Do you want to use the top 10 domains (1) or all domains (2)? ").strip()
        if user_choice == "1":
            return top_domains
        elif user_choice == "2":
            return top_domains + other_domains
        else:
            print("Invalid choice. Please try again.")

def generate_random_email(usernames, domain_choices):
    # Choose a username
    base = random.choice(usernames)

    # Occasionally add another username
    if random.random() < 0.3:
        second_base = random.choice(usernames)
        separator = random.choice(['.', '_'])
        base = f"{base}{separator}{second_base}"

    # Limit the base to 20 characters
    base = base[:20].lower()

    # Occasionally append a number at the end
    if random.random() < 0.6:
        base += str(random.randint(1, 99))

    # Choose a domain
    domain = random.choice(domain_choices)

    return f"{base}{domain}"

def generate_and_write_emails(usernames, domain_choices, output_file, start, end, email_set):
    for _ in range(start, end):
        email = generate_random_email(usernames, domain_choices)
        if email not in email_set:
            email_set.add(email)
            try:
                with open(output_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([email])
            except Exception as e:
                print(f"Error writing emails to CSV file: {e}")

def main():
    while True:
        try:
            amount = int(input("How many emails do you want to generate? "))
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    # Get the user's domain choice
    domain_choices = get_domain_choices()

    # Set the output file name
    output_file = "emails.csv"
    output_file = os.path.join(os.getcwd(), output_file)

    # Generate emails using multithreading or multiprocessing
    start_time = time.time()
    num_threads = min(mp.cpu_count(), amount)
    chunk_size = amount // num_threads

    email_set = set()
    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else amount
        t = threading.Thread(target=generate_and_write_emails, args=(load_usernames(), domain_choices, output_file, start, end, email_set))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate additional statistics
    unique_emails = len(email_set)
    email_rate = unique_emails / elapsed_time

    print("------------------------")
    print(f"CSV file '{output_file}' created.")
    print(f"Number of generated emails: {unique_emails}")
    print(f"Elapsed time: {datetime.timedelta(seconds=elapsed_time)}")
    print(f"Email generation rate: {email_rate:.2f} emails/second")
    print("------------------------")

if __name__ == "__main__":
    main()