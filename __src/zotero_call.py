"""
GRAVITYchat - Zotero API Calls for Paper Organization and Preprocessing
--------------------------------
This script serves as the data processing script for GRAVITYchat. Its primary task is
1. Call paper PDFs and Zotero metadata
2. Preprocess and the PDF and metadata

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

# Standard Libraries
import requests
import json
import os

# Third-party Libraries
import dotenv
#from pyzotero import zotero

_ = dotenv.load_dotenv(dotenv.find_dotenv())
API_KEY = os.environ.get("API_KEY")
GROUP_ID = os.environ.get("GROUP_ID")
BASE_URL = f"https://api.zotero.org/groups/{GROUP_ID}/items"


# Fetch all items in the LIGO group library
headers = {"Authorization": f"Bearer {API_KEY}"}
params = {"format": "json", "limit": 100}
response = requests.get(BASE_URL, headers=headers, params=params)
items = response.json()
print(items)
