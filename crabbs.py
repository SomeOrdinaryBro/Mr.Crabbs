import re
import json
from bs4 import BeautifulSoup
import requests

#Add your links here
urls = ['https://www.dialog.lk/', 'https://www.dialog.lk/support/contact-us']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
phone_pattern = r'\+?\d{1,4}?[\s-]?\(?\d{1,3}?\)?[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,9}'

all_emails = []
all_phones = []
all_links = []  

for url in urls:
    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')

            emails = re.findall(email_pattern, soup.text)
            phones = re.findall(phone_pattern, soup.text)
            links = [a['href'] for a in soup.find_all('a', href=True)]

            all_emails.extend(emails)
            all_phones.extend(phones)
            all_links.extend(links)
        else:
            print(f"Failed to retrieve the page at {url}. Status code: {page.status_code}")
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")

all_emails = list(set(all_emails))
all_phones = list(set(all_phones))
all_links = list(set(all_links))

data = {
    "emails": all_emails,
    "phones": all_phones,
    "links": all_links
}

with open('contacts_and_links.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data Extraction Complete")
