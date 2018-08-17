#%%
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

# Script to scrape abstracts of PNAS for the abstract text
# and associated key words. YOU MUST HAVE ACCESS TO PNAS
# (I'M ASSUMING THROUGH NU VPN). No pirates here. Totally legal
# yup

# url_base = 'http://www.pnas.org/keyword/artificial-photosynthesis'
url_base = 'http://www.pnas.org/content/115/33/8290'
r = requests.get(url_base)
# seems like pnas doesn't support json

soup = bs(r.text, "lxml")

for link in soup.find_all('a'):
    if 'keyword' in str(link.get('href')):
        print(link.get('href'))
all_text = soup.get_text()
for meta_tag in soup.find_all('meta'):
    # if 'abstract' in str(meta_tag.get('name')):
    if 'citation_abstract' == meta_tag.get('name'):
        print(meta_tag.get('content'))
