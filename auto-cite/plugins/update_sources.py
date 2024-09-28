#!/usr/bin/env python3

import requests
import yaml
from datetime import datetime
import sys

def fetch_dois_by_orcid(orcid, from_date='2020-01-01', max_results=50):
    base_url = f"https://api.crossref.org/works"
    
    params = {
        'filter': f'orcid:{orcid},from-pub-date:{from_date}',
        'sort': 'published',
        'order': 'desc',
        'rows': max_results,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()['message']['items']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ORCID {orcid}: {e}")
        print(f"URL: {response.url}")
        print(f"Response content: {response.text}")
        return []

def update_sources_yaml(orcids, output_file='_data/sources.yaml'):
    all_dois = set()
    
    for orcid in orcids:
        print(f"Fetching DOIs for ORCID {orcid}...")
        publications = fetch_dois_by_orcid(orcid)
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

# List of ORCIDs to search for
orcids = [
    "0000-0001-5432-1764",  # Luisa W. Hugerth's ORCID
    # Add more ORCIDs here
]

if __name__ == "__main__":
    update_sources_yaml(orcids)