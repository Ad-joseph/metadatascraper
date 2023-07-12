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
    meta_tags = soup.find_all('meta')
    
    meta_mapping = {
        'citation_title': ['citation_title', 'title'],
        'citation_author': ['citation_author', 'author'],
        'citation_journal_title': ['citation_journal_title', 'journal'],
        'citation_volume': ['citation_volume', 'volume'],
        'citation_issue': ['citation_issue', 'issue'],
        'citation_publication_date': ['citation_publication_date', 'publication_date'],
        'date-sold': ['date-sold']
    }
    
    for key, tag_names in meta_mapping.items():
        values = []
        for tag in meta_tags:
            if 'name' in tag.attrs and tag.attrs['name'] in tag_names:
                values.append(tag.attrs['content'])
            elif 'property' in tag.attrs and tag.attrs['property'] in tag_names:
                values.append(tag.attrs['content'])
        
        if key == 'citation_author':
            # Format author names with a comma between last name and first name
            formatted_authors = []
            for value in values:
                authors = value.split(', ')
                formatted_authors.append(' '.join(authors[::-1]))
            metadata[key] = ', '.join(formatted_authors)
        else:
            metadata[key] = ', '.join(values)
    
    return metadata

def save_to_csv(data):
    fieldnames = ['citation_title', 'citation_author', 'citation_journal_title', 'citation_volume', 'citation_issue', 'citation_publication_date', 'date-sold']
    
    with open('scraped_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            writer.writerow(item)