#%%
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from data_util import load_pnas
import re
import codecs
import time

# Script to scrape abstracts of PNAS for the abstract text
# and associated key words. YOU MUST HAVE ACCESS TO PNAS
# (I'M ASSUMING THROUGH NU VPN). No pirates here. Totally legal
# yup
dat_file = 'test.csv'
journal = 'PNAS'
url_list = ['http://www.pnas.org/content/115/33/8278', 'http://www.pnas.org/content/115/33/8290']
# url_list = ['http://www.pnas.org/content/115/33/8278']
# url_base = 'http://www.pnas.org/content/115/33/8290'

#%%
base_url = 'http://www.pnas.org/content/'
url_list = []
vol_start = 115
vol_end = 100 
issue_start = 52
issue_end = 0

for v in range(vol_start, vol_end, -1):
    if v == 115:
        i_start = 33
    else:
        i_start = issue_start
    for i in range(i_start, issue_end, -1):
        url = base_url + str(v) + '/' + str(i)
        print(url)
        url_list += find_chem_urls(url, base_url)
        time.sleep(4)
#%%
# for u in url_list:
    # print(u)
grab_articles(url_list)
#%%
def find_chem_urls(content_url, base_url):
    url_list = []
    r = requests.get(content_url)
    soup = bs(r.text, "lxml")
    lidex = -1
    lis = soup.find_all('li')
    for i, li in enumerate(lis):
        li_class = li.get('class')
        if li_class == None:
            continue
        li_c = ' '.join(li_class)
        if 'section-chemistry' in li_c:
            lidex = i
    
    idx = lidex
    while(True):
        if lis[lidex].find_all('h2') is not None and idx != lidex:
            break
        for h in lis[idx].find_all('a'):
            if h.get('class') == ['highwire-cite-linked-title']:
                print(h.get('href'))
                url_list.append(base_url + h.get('href')[9:])
        idx += 1
    return url_list

#%%
def grab_articles(url_list):
    with codecs.open(dat_file, 'w', encoding='utf8') as f:
        f.write('Title|Authors|Abstract|Keywords|Pub Date|DOI|Journal Name\n')
        for url in url_list:
            keywords = []
            authors = []
        
            r = requests.get(url)
            soup = bs(r.text, "lxml")
        
            for link in soup.find_all('a'):
                if 'keyword' in str(link.get('href')):
                    # print(link.text)
                    keywords.append(link.text)
                
            found_abstract = False
            for meta_tag in soup.find_all('meta'):
        
                # Multiple matches for abstract, but the first match is what we need
                if 'citation_abstract' == meta_tag.get('name') and not found_abstract:
                    # print(meta_tag.get('content'))
        
                    # There's like extra html tags and I don't know how to remove them
                    abstract = meta_tag.get('content')[3:-4]
                    found_abstract = True
        
        
                if 'citation_title' == meta_tag.get('name'):
                    title = meta_tag.get('content')
    
                if 'citation_publication_date' == meta_tag.get('name'):
                    # TODO We need to figure out a date format
                    # print(meta_tag.get('content'))
                    pub_date = meta_tag.get('content')
        
                if 'citation_doi' == meta_tag.get('name'):
                    # print(meta_tag.get('content'))
                    doi = meta_tag.get('content')
        
                if 'citation_author' == meta_tag.get('name'):
                    # print(meta_tag.get('content'))
                    authors.append(meta_tag.get('content'))
            
            var_list = [title, ','.join(authors), abstract, ','.join(keywords), 
                            pub_date, doi, journal]
            # encode_vars = []
            # for var in var_list:
            #     var = re.sub(r"<sub>(?P<digit>\d+)</sub>",r"\1", var)
            #     var = var.encode('utf-8').strip()
            #     print(var)
            #     print(re.sub('[ -~]', '', var))
            #     encode_vars.append(var)
    
            # stripping weird tags around subscript numbers
            strip_tags = [re.sub(r"<sub>(?P<digit>\d+)</sub>",r"\1", var) for var in var_list]
            # line = '%s | %s | %s | %s | %s | %s | %s\n' % tuple(var_list)
            line = '%s|%s|%s|%s|%s|%s|%s\n' % tuple(strip_tags)
            print(title)
            f.write(line)
            time.sleep(4)

#%%
df = load_pnas(dat_file)
print(pd.api.types.infer_dtype(df.columns))