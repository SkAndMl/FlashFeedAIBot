import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict
from collections import defaultdict



def get_links(query: str,
              num_links: int=4) -> List[str]:
    
    query = query.replace(" ", "+")
    link = f"https://www.google.com/search?q={query}&tbm=nws"
    ua = UserAgent()
    response = requests.get(
        url=link,
        headers={"User-Agent" : ua.random}
    )
    soup = BeautifulSoup(response.text, "lxml")
    links = []
    for li in soup.find_all("a", class_="WlydOe", href=True)[:num_links]:
        links.append(li["href"])
    return links

def get_text_content(links: str) -> Dict[str, str]:
    texts = defaultdict(str)
    ua = UserAgent()
    for link in links:
        response = requests.get(
            url=link,
            headers={"User-Agent" : ua.random}
        )
        link_text = ""
        link_soup = BeautifulSoup(response.text, "html.parser")
        for p in link_soup.find_all("p"):
            link_text += p.text + "\n"
        texts[link] = link_text
    return texts





