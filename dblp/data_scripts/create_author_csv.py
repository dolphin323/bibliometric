import pandas as pd
import json
from tqdm import tqdm
from itertools import islice
import multiprocessing as mp
import csv


def divide_dict(d, n):
    it = iter(d)
    for i in range(0, len(d), n):
        yield {k: d[k] for k in islice(it, n)}


def get_processed_first_year_pub(filenames):
    first_year_pubs_with_author_name = dict()

    for filename in filenames:
        with open(filename, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                first_year_pubs_with_author_name[row["dblp_author_name"]] = row[
                    "first_publication_year"
                ]

    return first_year_pubs_with_author_name


# df_articles = df_articles.reset_index()  # make sure indexes pair with number of rows
def proccess_features(info):
    values = info["values"].values()
    # df_authors = pd.DataFrame()
    df_authors_dblp = pd.DataFrame()
    df_universities = pd.DataFrame()

    first_year_pubs = pd.read_csv("../data/research_age/dblp_all.csv")

    for row in tqdm(values):
        point_per_author = 1 / len(row["author"].split("|"))
        # institutions = dict()
        if int(row["publication_year"]) < 2024 and int(
            row["type"]
            not in [
                "editorial",
                "position paper",
                "keynote",
                "opinion",
                "tutorial",
                "poster",
                "panel",
            ]
        ):
            for author_name_dblp in row["author"].split("|"):
                author_row = dict()

                author_row["dblp_author_name"] = author_name_dblp
                author_row["title"] = row["title"]
                author_row["id"] = row["id"]
                author_row["booktitle"] = row["booktitle"]
                author_row["journal"] = row.get("journal", "")
                author_row["publication_date"] = row["publication_date"]
                author_row["publication_year"] = row["publication_year"]
                author_row["cited_by_count"] = row["cited_by_count"]
                # author_row["research_age"] = (
                #     first_year_pubs[
                #         first_year_pubs["dblp_author_name"] == author_name_dblp
                #     ]
                # )["research_age"]

                df_authors_dblp = pd.concat(
                    [df_authors_dblp, pd.DataFrame([author_row])], ignore_index=True
                )
            for author in row["authorships"]:
                # author_row = dict()

                # display_name = author["author"]["display_name"]

                # author_row["raw_author_name"] = author["raw_author_name"]
                # author_row["display_name"] = display_name
                # author_row["title"] = row["title"]
                # author_row["id"] = row["id"]
                # institution_row["booktitle"] = row.get("booktitle", "")
                # institution_row["journal"] = row.get("journal", "")
                # author_row["publication_date"] = row["publication_date"]
                # author_row["publication_year"] = row["publication_year"]
                # author_row["cited_by_count"] = row["cited_by_count"]
                # df_authors = pd.concat(
                #     [df_authors, pd.DataFrame([author_row])], ignore_index=True
                # )

                author_institutions = author["institutions"]
                for institution in author_institutions:
                    institution_row = dict()
                    institution_row["display_name"] = institution["display_name"]
                    institution_row["country_code"] = institution["country_code"]
                    institution_row["type"] = row["type"]
                    institution_row["title"] = row["title"]
                    institution_row["id"] = row["id"]
                    institution_row["booktitle"] = row.get("booktitle", "")
                    institution_row["score"] = point_per_author
                    institution_row["journal"] = row.get("journal", "")
                    df_universities = pd.concat(
                        [df_universities, pd.DataFrame([institution_row])]
                    )

    df_universities.to_csv(
        f"../data/analysis/filtered_types/institutions/institutions_{info['num_of_file']}.csv",
        index=False,
    )

    df_authors_dblp.to_csv(
        f"../data/analysis/filtered_types/authors/authors_{info['num_of_file']}.csv",
        index=False,
    )


def main():
    with open(
        "../data/output_filter_venue_2016_added_data/with_type/output_article.json",
        "r",
    ) as file:
        article_json_str = file.read()

    article_json = json.loads(article_json_str)

    list_for_proccess = []
    for index, value in enumerate(divide_dict(article_json, 3700)):
        list_for_proccess.append(
            {
                "num_of_file": index,
                "values": value,
            }
        )

    pool = mp.Pool(2)
    result = pool.map(proccess_features, list_for_proccess)


if __name__ == "__main__":
    main()
