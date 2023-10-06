import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODEL_NAME = "facebook/bart-large-cnn"
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
SUMMARIZER = pipeline(task="summarization",
                      model=MODEL,
                      tokenizer=TOKENIZER)

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

def get_text_content(links: str) -> List[str]:
    texts = []
    ua = UserAgent()
    for link in links:
        response = requests.get(
            url=link,
            headers={"User-Agent" : ua.random}
        )
        texts.append(BeautifulSoup(response.text, "lxml").text)
    return texts


def get_summary(texts: List[str]) -> List[str]:

    summarized_texts = []
    for text in texts:
        summarized_texts.append(SUMMARIZER(text[:1024])[0]["summary_text"])
    return summarized_texts


