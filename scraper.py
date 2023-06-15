import requests
from bs4 import BeautifulSoup
import csv

def scrape(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    content = response.content

    # parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Collect metadata
    metadata = {}

    for key in ['citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_publication_date']:
        meta_tags = soup.find_all('meta', attrs={'name': key})
        values = [tag['content'] for tag in meta_tags]
        if key == 'citation_author':
            # Format author names with a comma between last name and first name
            formatted_authors = []
            for value in values:
                authors = value.split(', ')
                formatted_authors.append(' '.join(authors[::-1]))
            metadata[key] = ', '.join(formatted_authors)
        else:
            metadata[key] = ', '.join(values)

    if len(metadata['citation_publication_date']) == 0:
        meta_tags = soup.find_all('meta', attrs={'property': 'og:updated_time'})
        values = [tag['content'] for tag in meta_tags]
        metadata['citation_publication_date'] = ', '.join(values)

    return metadata

def save_to_csv(data):
    fieldnames = ['citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_publication_date']

    with open('scraped_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            writer.writerow(item)
