import re
import json
import time
import random
from bs4 import BeautifulSoup
import requests

# Add your links here
urls = ['https://www.dialog.lk/', 'https://www.dialog.lk/support/contact-us']

# Rotate multiple user-agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1'
]

# Randomized headers
def get_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Referer': 'https://www.google.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

# Regex patterns
email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
phone_pattern = r'\+?\d{1,4}?[\s-]?\(?\d{1,3}?\)?[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,9}'

all_emails = []
all_phones = []
all_links = []

# Use a session to maintain cookies and improve stealth
session = requests.Session()

for url in urls:
    try:
        # Random delay to avoid hitting too quickly
        time.sleep(random.uniform(2, 5))  # Random delay between 2 to 5 seconds

        # Make the request with randomized headers
        response = session.get(url, headers=get_headers())

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract emails, phones, and links
            emails = re.findall(email_pattern, soup.text)
            phones = re.findall(phone_pattern, soup.text)
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # Add unique values to the lists
            all_emails.extend(emails)
            all_phones.extend(phones)
            all_links.extend(links)
        else:
            print(f"Failed to retrieve the page at {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")

# Remove duplicates
all_emails = list(set(all_emails))
all_phones = list(set(all_phones))
all_links = list(set(all_links))

# Save data to JSON file
data = {
    "emails": all_emails,
    "phones": all_phones,
    "links": all_links
}

with open('contacts_and_links.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data Extraction Complete")
