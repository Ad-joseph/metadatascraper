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

    # we create a dictionary with keys as the meta data we want to collect and values as the possible tags they can have
    meta_data_tags = {
        'citation_title': ['citation_title', 'header', 'title'],
        'citation_author': ['citation_author', 'author'],
        'citation_journal_title': ['citation_journal_title', 'journal'],
        'citation_volume': ['citation_volume', 'volume'],
        'citation_issue': ['citation_issue', 'issue'],
        'citation_publication_date': ['citation_publication_date', 'publication_date', 'date', 'og:updated_time']
    }

    for key, tags in meta_data_tags.items():
        values = []
        for tag in tags:
            meta_tags = soup.find_all('meta', attrs={'name': tag})
            temp_values = [meta_tag['content'] for meta_tag in meta_tags if meta_tag.has_attr('content')]
            values.extend(temp_values)

            if values:
                break

        if key == 'citation_author':
            # Format author names with a comma between last name and first name
            formatted_authors = []
            for value in values:
                authors = value.split(', ')
                formatted_authors.append(' '.join(authors[::-1]))
            metadata[key] = ', '.join(formatted_authors)
        else:
            metadata[key] = ', '.join(values)

        # if no tag was found, set value to None
        if key not in metadata:
            metadata[key] = None

    return metadata
