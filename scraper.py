import requests
from bs4 import BeautifulSoup
import csv

def scrape_journals(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')

    journal_urls = []
    article_links = soup.select('a[data-track-action="view full text"]')
    for link in article_links:
        href = link['href']
        journal_urls.append(href)

    return journal_urls

def scrape_journal_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')

    metadata = {}

    tag_mappings = {
        'citation_title': ['og:citation_title', 'title'],
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
    fieldnames = ['citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_publication_date']
    with open('scraped_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

# Example usage:
starting_url = url # Replace with your starting URL
journal_urls = scrape_journals(starting_url)

scraped_data = []
for journal_url in journal_urls:
    data = scrape_journal_data(journal_url)
    scraped_data.append(data)

save_to_csv(scraped_data)