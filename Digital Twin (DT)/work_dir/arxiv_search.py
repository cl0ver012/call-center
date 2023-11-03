# filename: arxiv_search.py

import requests
import xml.etree.ElementTree as ET

# Define the base url and the search query
base_url = 'http://export.arxiv.org/api/query?'
search_query = 'all:trust calibration in AI based systems'

# Send a GET request to the arXiv API
response = requests.get(base_url, params={'search_query': search_query})

# Parse the response using ElementTree
root = ET.fromstring(response.content)

# Define the arXiv namespace
namespace = {'arxiv': 'http://arxiv.org/schemas/atom'}

# Print the title, authors, and summary of each paper
for entry in root.findall('arxiv:entry', namespace):
    print('Title: ', entry.find('arxiv:title', namespace).text)
    print('Authors: ', ', '.join(author.find('arxiv:name', namespace).text for author in entry.findall('arxiv:author', namespace)))
    print('Summary: ', entry.find('arxiv:summary', namespace).text)
    print('\n')