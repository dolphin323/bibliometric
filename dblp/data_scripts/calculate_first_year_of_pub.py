import pandas as pd
import json
from tqdm import tqdm
from itertools import islice
import multiprocessing as mp
import csv


def calculate_first_year_of_pub():
    df_articles_all = pd.read_csv(
        "../data/output_csv/output_article.csv", sep=";", low_memory=False
    )
    df_inproceedings_all = pd.read_csv(
        "../data/output_csv/output_inproceedings.csv", sep=";", low_memory=False
    )

    df_articles_all = df_articles_all[
        df_articles_all["author"].apply(lambda x: isinstance(x, str))
    ]
    df_inproceedings_all = df_inproceedings_all[
        df_inproceedings_all["author"].apply(lambda x: isinstance(x, str))
    ]

    with open(
        "../data/output_filter_venue_2016_added_data/output_article.json", "r"
    ) as file:
        article_json_str = file.read()

    article_json = json.loads(article_json_str)

    values = article_json.values()

    first_year_pubs_with_author_name = []

    with open(
        f"../data/analysis/author_dblp/authors_first_year_pub.csv",
        "w",
        newline="",
    ) as output_csv:
        csv_writer = csv.DictWriter(
            output_csv,
            fieldnames=[
                "first_publication_year",
                "dblp_author_name",
                "title",
                "id",
            ],
        )
        first_year_pubs_with_author_name = []
        csv_writer.writeheader()
        for row in tqdm(values):
            institutions = dict()
            for author_name_dblp in row["author"].split("|"):
                author_row = dict()

                first_year_pub = -1
                if dblp_author_name not in first_year_pubs_with_author_name:
                    df_result_all_articles = df_articles_all[
                        df_articles_all["author"].str.contains(dblp_author_name)
                    ]
                    df_result_all_inproceedings = df_inproceedings_all[
                        df_inproceedings_all["author"].str.contains(dblp_author_name)
                    ]

                    first_year_pub_articles = df_result_all_articles["year"].min()
                    first_year_pub_inproceedings = df_result_all_inproceedings[
                        "year"
                    ].min()

                    first_year_pub = (
                        first_year_pub_inproceedings
                        if first_year_pub_articles > first_year_pub_inproceedings
                        else first_year_pub_articles
                    )
                else:
                    first_year_pub = first_year_pubs_with_author_name[author_name_dblp]

                author_row["first_publication_year"] = first_year_pub
                author_row["dblp_author_name"] = author_name_dblp
                author_row["title"] = row["title"]
                author_row["id"] = row["id"]
                csv_writer.writerow(author_row)

    # with open("../data/analysis/authors_first_year_pub.csv", "r") as file:
    #     csv_reader = csv.DictReader(file)
    #     for row in csv_reader:
    #         # Assuming 'author_name' is a column header in your CSV
    #         author_name = row["display_name"]
    #         first_year_pubs_with_author_name.append(author_name)

    # with open("../data/analysis/authors_first_year_pub_1.csv", "r") as file:
    #     csv_reader = csv.DictReader(file)
    #     for row in csv_reader:
    #         # Assuming 'author_name' is a column header in your CSV
    #         author_name = row["display_name"]
    #         first_year_pubs_with_author_name.append(author_name)
    # with open(
    #     f"../data/analysis/authors_first_year_pub_2.csv",
    #     "w",
    #     newline="",
    # ) as output_csv:
    #     csv_writer = csv.DictWriter(
    #         output_csv,
    #         fieldnames=[
    #             "first_publication_year",
    #             "raw_author_name",
    #             "display_name",
    #         ],
    #     )

    #     csv_writer.writeheader()
    #     for row in tqdm(values):
    #         for author in row["authorships"]:
    #             author_row = dict()

    #             display_name = author["author"]["display_name"]
    #             if not (display_name in first_year_pubs_with_author_name):
    #                 df_result_all_articles = df_articles_all[
    #                     df_articles_all["author"].str.contains(display_name)
    #                 ]
    #                 df_result_all_inproceedings = df_inproceedings_all[
    #                     df_inproceedings_all["author"].str.contains(display_name)
    #                 ]

    #                 first_year_pub_articles = df_result_all_articles["year"].min()
    #                 first_year_pub_inproceedings = df_result_all_inproceedings[
    #                     "year"
    #                 ].min()

    #                 first_year_pub = (
    #                     first_year_pub_inproceedings
    #                     if first_year_pub_articles > first_year_pub_inproceedings
    #                     else first_year_pub_articles
    #                 )
    #                 author_row["first_publication_year"] = first_year_pub
    #                 author_row["raw_author_name"] = author["raw_author_name"]
    #                 author_row["display_name"] = display_name
    #                 csv_writer.writerow(author_row)
    #             else:
    #                 pass


calculate_first_year_of_pub()
