import requests
from bs4 import BeautifulSoup

webpage = "https://www.anvur.it/attivita/classificazione-delle-riviste/classificazione-delle-riviste-ai-fini-dellabilitazione-scientifica-nazionale/elenchi-di-riviste-scientifiche-e-di-classe-a/"

with requests.get(webpage) as res:
    response = BeautifulSoup(res.text, "html.parser")