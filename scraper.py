import requests
from bs4 import BeautifulSoup
import csv

def scrape(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')

    metadata = {}

    tag_mappings = {
        'citation_title': ['og:citation_title', 'og:title', 'title'],
        'citation_author': ['og:citation_author'],
        'citation_journal_title': ['og:citation_journal_title'],
        'citation_volume': ['og:citation_volume'],
        'citation_issue': ['og:citation_issue'],
        'citation_publication_date': ['og:citation_publication_date']
    }

    for key, tag_names in tag_mappings.items():
        value = ''
        for tag_name in tag_names:
            tag = soup.find('meta', attrs={'property': tag_name}) or soup.find('meta', attrs={'name': tag_name})
            if tag:
                value = tag['content']
                break
        metadata[key] = value

    return metadata

def save_to_csv(data):
    fieldnames = ['citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_publication_date', 'date-sold']
    
    with open('scraped_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            writer.writerow(item)