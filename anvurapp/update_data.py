import json
import requests
import pandas as pd
from tinydb import TinyDB


def get_anvur_data() -> str:
    """Function to get updated ANVUR data from server
    Return string with operation status
    """
    try:
        with requests.get("https://anvur.by.gg8.eu/v1/anvur/") as res:
            response = json.loads(res.text)
        with open("db.json", "w") as f:
            json.dump(response, f)
        return "ANVUR data downloaded."
    except Exception:
        return "Error. ANVUR data not downloaded."


def get_scimago_data() -> str:
    """Function to get journal data from Scimago.
    Return string with operation status
    """
    try:
        # Get scimago file from their website
        scimago_df = pd.read_csv(
            "https://www.scimagojr.com/journalrank.php?out=xls", sep=";"
        )
        # Get dummies for scientific areas and merge the table on index
        areas_df = scimago_df["Areas"].str.get_dummies(sep="; ")
        scimago_df = scimago_df.join(areas_df)
        # Rename ISSN in uppercase
        scimago_df = scimago_df.rename(columns={"Issn": "ISSN"})
        # Drop type column
        scimago_df = scimago_df.drop(columns="Type")
        # Add link to Scimago website
        scimago_df["Link"] = scimago_df.apply(
            lambda row: "https://www.scimagojr.com/journalsearch.php?q={}&tip=sid".format(
                row["Sourceid"]
            ),
            axis=1,
        )
        # Explode to one line for each ISSN
        scimago_df["ISSN"] = scimago_df["ISSN"].str.split(", ")
        scimago_df = scimago_df.explode("ISSN")

        # Save data
        db = TinyDB("scimago.json")
        # Drop previous table
        db.drop_table("scimago")

        scimago = db.table("scimago")

        _ = scimago.insert_multiple(scimago_df.to_dict(orient="records"))

        return "Scimago data downloaded."
    except Exception:
        return "Error. Scimago data not downloaded."
