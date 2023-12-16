import csv
import json
import requests
from tqdm import tqdm


def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in tqdm(csvReader):
            try:
                doi_link = [
                    string
                    for string in rows["ee"].split("|")
                    if string.startswith("https://doi.org/")
                ][0]

                response = requests.get(f"https://api.openalex.org/works/{doi_link}")
                # print(response.json())

                response_data = response.json()

                rows["concepts"] = response_data.get("concepts", [])
                rows["authorships"] = response_data.get("authorships", [])
                rows["type"] = response_data.get("type", "")
                rows["keywords"] = response_data.get("keywords", [])

                key = rows["id"]
                # id,author,booktitle,ee,journal,key,title,year,cited_by_count,publication_date,publication_year

                data[key] = rows
            except:
                print("__________________")
                print(response.text)
                print(rows["ee"])

    with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


csvFilePath = r"../data/output_filter_venue_2016_added_data/output_article.csv"
jsonFilePath = (
    r"../data/output_filter_venue_2016_added_data/with_type/output_article.json"
)

make_json(csvFilePath, jsonFilePath)
