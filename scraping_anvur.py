import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Setup variables
webpage = "https://www.anvur.it/attivita/classificazione-delle-riviste/classificazione-delle-riviste-ai-fini-dellabilitazione-scientifica-nazionale/elenchi-di-riviste-scientifiche-e-di-classe-a/"

headers = {
    'User-Agent': 'Anvur Journal Acquisition',
    "Mail": "luigi.palumbo@unitus.it"
}

# Get list of links from Anvur webpage
with requests.get(webpage, headers=headers) as res:
    response = BeautifulSoup(res.text, "html.parser")

link_list = [
    {
        "area": item.get_text(strip=True),
        "filename": item.get("href").split("/")[-1],
        "link": item.get("href")
    }
    for item in
    response.find_all("a", {"href": re.compile("pdf$")})
]

# Download files
for item in link_list:
    time.sleep(2)
    with requests.get(item.get("link"), headers=headers) as res:
        with open("data/{}".format(item.get("filename")), "wb") as f:
            f.write(res.content)

# Save list of most recent downloaded files
link_df = pd.DataFrame(link_list)
link_df.to_csv("data/anvur_journals.csv", index=False)