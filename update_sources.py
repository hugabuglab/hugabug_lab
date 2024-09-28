#!/usr/bin/env python3

import requests
import yaml
from datetime import datetime
import sys
import urllib.parse

def fetch_dois_by_author(author_name, from_date='2020-01-01', max_results=50):
    base_url = "https://api.crossref.org/works"
    
    # Encode the author name properly
    encoded_author = urllib.parse.quote(author_name)
    
    # Construct the query string
    query = f'query.author="{encoded_author}"'
    
    params = {
        'query': query,
        'filter': f'from-pub-date:{from_date}',
        'sort': 'published',
        'order': 'desc',
        'rows': max_results,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()['message']['items']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {author_name}: {e}")
        print(f"URL: {response.url}")
        print(f"Response content: {response.text}")
        return []

def update_sources_yaml(authors, output_file='_data/sources.yaml'):
    all_dois = set()
    
    for author in authors:
        print(f"Fetching DOIs for {author}...")
        publications = fetch_dois_by_author(author)
        for pub in publications:
            if 'DOI' in pub:
                all_dois.add(f"doi:{pub['DOI']}")
    
    # Read existing DOIs
    try:
        with open(output_file, 'r') as file:
            existing_data = yaml.safe_load(file) or []
    except FileNotFoundError:
        existing_data = []
    
    existing_dois = set(item['id'] for item in existing_data if 'id' in item)
    
    # Add new DOIs
    new_dois = all_dois - existing_dois
    for doi in new_dois:
        existing_data.append({'id': doi})
    
    # Write updated data back to file
    with open(output_file, 'w') as file:
        yaml.dump(existing_data, file, default_flow_style=False)
    
    print(f"Added {len(new_dois)} new DOIs to {output_file}")

# List of authors to search for
authors = [
    "Luisa W. Hugerth",
    # Add more authors here
]

if __name__ == "__main__":
    update_sources_yaml(authors)