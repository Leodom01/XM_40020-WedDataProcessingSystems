#partially AI generated do not submit as it is

import requests
from bs4 import BeautifulSoup

def download_wiki_page(url):
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)

    main_content = soup.find('div', {'id': 'mw-content-text'})
    #print(main_content)
    
    if main_content:

        nested_div = main_content.find('div')

        if nested_div:
            # Extract the text within the p tags
            paragraphs = [p.text for p in nested_div.find_all('p')]
            return "\n".join(paragraphs)
        else:
            return "Nested div not found"
    else:
        return "Main content not found"
