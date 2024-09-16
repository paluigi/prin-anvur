import os
from functools import reduce
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tinydb import TinyDB
import camelot

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
current_anvur_df = pd.DataFrame(link_list)
#current_anvur_df.to_csv("data/anvur_journals.csv", index=False)

# Create separate lists for Classe A and scientific
docs_classe_a = [
    item
    for item in
    current_anvur_df.to_dict(orient="records")
    if item.get("area").endswith("classe A")
]

docs_scientifici = [
    item for item in
    current_anvur_df.to_dict(orient="records")
    if item not in docs_classe_a
]

# Process Classe A PDFs
classe_a_list = []

for item in docs_classe_a:
    table_list = camelot.read_pdf(os.path.join("data",item.get("filename")), pages="1-end")
    # Move first line as header
    for i, _ in enumerate(table_list):
        table_list[i].df.columns = table_list[i].df.iloc[0].to_list()
        table_list[i].df = table_list[i].df[1:]
    # Concatenate all dataframes
    table_list = pd.concat([item.df for item in table_list])
    # Remove hypens from ISSN
    table_list["ISSN"] = table_list["ISSN"].str.replace("-", "")
    classe_a_list.append(table_list.copy(deep=True))

# Combine all titles and ISSN
classe_a_journals = pd.concat([df[["TITOLO", "ISSN"]].copy() for df in classe_a_list])
classe_a_journals = classe_a_journals.drop_duplicates()


# Drop Title column
classe_a_list = [df.drop(columns=["TITOLO"]) for df in classe_a_list]
# Combine classe A markings
classe_a_df = reduce(lambda  left,right: pd.merge(left,right,on=['ISSN'],how='outer'), classe_a_list)

classe_a_list = [
    {k:v for k,v in elem.items() if pd.notna(v) and v != ""} 
    for elem in classe_a_df.to_dict(orient="records")
    ]

# Process scientific PDFs
scientific_list = []

for item in docs_scientifici:
    table_list = camelot.read_pdf(os.path.join("data",item.get("filename")), pages="1-end")
    # Move first line as header
    for i, _ in enumerate(table_list):
        table_list[i].df.columns = table_list[i].df.iloc[0].to_list()
        table_list[i].df = table_list[i].df[1:]
    # Concatenate all dataframes
    table_list = pd.concat([item.df for item in table_list])
    # Remove hypens from ISSN
    table_list["ISSN"] = table_list["ISSN"].str.replace("-", "")
    scientific_list.append(table_list.copy(deep=True))

# Combine all titles and ISSN
scientific_journals = pd.concat([df[["TITOLO", "ISSN"]].copy() for df in scientific_list])
scientific_journals = scientific_journals.drop_duplicates()

# Drop Title column
scientific_list = [df.drop(columns=["TITOLO"]) for df in scientific_list]
# Combine scientific markings
scientific_df = reduce(lambda  left,right: pd.merge(left,right,on=['ISSN'],how='outer'), scientific_list)

scientific_list = [
    {k:v for k,v in elem.items() if pd.notna(v) and v != ""} 
    for elem in scientific_df.to_dict(orient="records")
    ]

# Combine the lists of journals
anvur_journals = pd.concat([classe_a_journals,scientific_journals]).drop_duplicates(subset="ISSN").sort_values(by="TITOLO")


# Save data
db = TinyDB('db.json')
# Drop previous tables
db.drop_table('anvur')
db.drop_table('classea')
db.drop_table('scientific')


anvur = db.table('anvur')
classea = db.table('classea')
scientific = db.table('scientific')

_ = anvur.insert_multiple(anvur_journals.to_dict(orient="records"))
_ = classea.insert_multiple(classe_a_list)
_ = scientific.insert_multiple(scientific_list)