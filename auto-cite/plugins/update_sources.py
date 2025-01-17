#!/usr/bin/env python3

import requests
import yaml
from datetime import datetime
import sys
import time
from urllib.parse import quote

def fetch_from_crossref(orcid, from_date='2020-01-01', max_results=1000):
    """Fetch DOIs from Crossref"""
    base_url = "https://api.crossref.org/works"
    params = {
        'filter': f'orcid:{orcid},from-pub-date:{from_date}',
        'select': 'DOI,type,title,published,container-title',
        'sort': 'published',
        'order': 'desc',
        'rows': max_results,
        'mailto': 'faruk.dube@imbim.uu.se'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()['message']['items']
    except Exception as e:
        print(f"Crossref error: {e}")
        return []

def fetch_from_orcid_api(orcid):
    """Fetch DOIs directly from ORCID API"""
    base_url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        works = response.json()['group']
        dois = []
        for work in works:
            for external_id in work.get('external-ids', {}).get('external-id', []):
                if external_id.get('external-id-type') == 'doi':
                    dois.append({
                        'DOI': external_id.get('external-id-value'),
                        'type': work.get('type', 'unknown'),
                        'title': [work.get('title', {}).get('title', {}).get('value', '')],
                    })
        return dois
    except Exception as e:
        print(f"ORCID API error: {e}")
        return []

def fetch_from_europe_pmc(orcid):
    """Fetch DOIs from Europe PMC"""
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        'query': f'AUTHORID:"{orcid}"',
        'format': 'json',
        'resultType': 'core',
        'pageSize': 1000
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()['resultList']['result']
        return [{
            'DOI': result.get('doi'),
            'type': 'journal-article',
            'title': [result.get('title')],
            'container-title': [result.get('journalTitle')]
        } for result in results if result.get('doi')]
    except Exception as e:
        print(f"Europe PMC error: {e}")
        return []

def is_valid_publication(pub):
    """Check if publication is valid (not preprint/thesis)"""
    # Valid publication types
    valid_types = {
        'journal-article',
        'proceedings-article',
        'book-chapter',
        'book',
        'peer-review',
        'article',
        'journal'
    }
    
    # Terms that indicate preprints or theses
    invalid_terms = {
        'preprint', 
        'thesis', 
        'dissertation',
        'working paper',
        'arxiv',
        'biorxiv',
        'medrxiv',
        'researchsquare',
        'zenodo'
    }
    
    # Convert type and title to lowercase for comparison
    pub_type = str(pub.get('type', '')).lower()
    title = str(pub.get('title', [''])[0]).lower()
    container = str(pub.get('container-title', [''])[0]).lower() if pub.get('container-title') else ''
    
    # Check if it's a valid type
    is_valid = (pub_type in valid_types)
    
    # Check for invalid terms in type, title, and container
    has_invalid_terms = any(term in pub_type or term in title or term in container 
                          for term in invalid_terms)
    
    return is_valid and not has_invalid_terms

def update_sources_yaml(orcids, output_file='_data/sources.yaml'):
    all_dois = set()
    
    for orcid in orcids:
        print(f"\nFetching publications for ORCID {orcid}...")
        
        # Fetch from multiple sources
        crossref_pubs = fetch_from_crossref(orcid)
        print(f"Found {len(crossref_pubs)} publications from Crossref")
        
        orcid_pubs = fetch_from_orcid_api(orcid)
        print(f"Found {len(orcid_pubs)} publications from ORCID")
        
        europe_pmc_pubs = fetch_from_europe_pmc(orcid)
        print(f"Found {len(europe_pmc_pubs)} publications from Europe PMC")
        
        # Combine all publications
        all_pubs = crossref_pubs + orcid_pubs + europe_pmc_pubs
        
        # Filter and add DOIs
        for pub in all_pubs:
            if pub.get('DOI') and is_valid_publication(pub):
                doi = pub['DOI'].lower()
                title = pub.get('title', [''])[0]
                pub_type = pub.get('type', 'unknown')
                container = pub.get('container-title', [''])[0] if pub.get('container-title') else 'N/A'
                
                print(f"Adding: {title}")
                print(f"Type: {pub_type}")
                print(f"Journal: {container}")
                print("---")
                
                all_dois.add(f"doi:{doi}")
    
    # Read existing DOIs
    try:
        with open(output_file, 'r') as file:
            existing_data = yaml.safe_load(file) or []
    except FileNotFoundError:
        existing_data = []
    
    existing_dois = set(item['id'].lower() for item in existing_data if 'id' in item)
    
    # Add new DOIs
    new_dois = all_dois - existing_dois
    for doi in new_dois:
        existing_data.append({'id': doi})
    
    # Sort by DOI
    existing_data.sort(key=lambda x: x['id'])
    
    # Write updated data back to file
    with open(output_file, 'w') as file:
        yaml.dump(existing_data, file, default_flow_style=False)
    
    print(f"\nAdded {len(new_dois)} new DOIs to {output_file}")
    if new_dois:
        print("\nNew DOIs added:")
        for doi in sorted(new_dois):
            print(f"  {doi}")

# List of ORCIDs to search for
orcids = [
    "0000-0001-5432-1764",  # Luisa W. Hugerth's ORCID
    "0000-0003-1340-9123",  # Faruk Dube's ORCID
]

if __name__ == "__main__":
    update_sources_yaml(orcids)