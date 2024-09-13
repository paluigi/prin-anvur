import requests

# Setup variables
scimago_link = "https://www.scimagojr.com/journalrank.php?out=xls"

headers = {
    'User-Agent': 'Anvur Journal Acquisition',
    "Mail": "luigi.palumbo@unitus.it"
}

# Download file
with requests.get(scimago_link, headers=headers) as res:
    with open("data/scimago.csv", "wb") as f:
        f.write(res.content)
