import requests
from bs4 import BeautifulSoup
import csv

def get_journal_urls(starting_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(starting_url, headers=headers)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')

    journal_urls = []

    # Find the <a> tags with class="journal-link"
    journal_elements = soup.find_all('a', class_='journal-link')

    for element in journal_elements:
        journal_url = element['href']
        journal_urls.append(journal_url)

    return journal_urls

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

def scrape_all(urls):
    scraped_data = []
    for url in urls:
        metadata = scrape(url)
        scraped_data.append(metadata)
    save_to_csv(scraped_data)
    return scraped_data
