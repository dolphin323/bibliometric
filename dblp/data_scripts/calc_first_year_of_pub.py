import pandas as pd
import json
from tqdm import tqdm
from itertools import islice
import multiprocessing as mp
import csv


def divide_dict(d, n):
    it = iter(d)
    for i in range(136, len(d), n):
        yield {k: d[k] for k in islice(it, n)}


# first_year_pubs_with_author_name =


# df_articles = df_articles.reset_index()  # make sure indexes pair with number of rows
def proccess_features(info):
    values = info["values"].values()
    df_articles_all = info["df_articles_all"]
    df_inproceedings_all = info["df_inproceedings_all"]

    with open(
        f"../data/analysis/author_dblp/authors_first_year_pub{info['num_of_file']}.csv",
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


# def main():
#     df_articles_all = pd.read_csv(
#         "../data/output_csv/output_article.csv", sep=";", low_memory=False
#     )
#     df_inproceedings_all = pd.read_csv(
#         "../data/output_csv/output_inproceedings.csv", sep=";", low_memory=False
#     )

#     df_articles_all = df_articles_all[
#         df_articles_all["author"].apply(lambda x: isinstance(x, str))
#     ]
#     df_inproceedings_all = df_inproceedings_all[
#         df_inproceedings_all["author"].apply(lambda x: isinstance(x, str))
#     ]

#     with open(
#         "../data/output_filter_venue_2016_added_data/output_inproceedings.json", "r"
#     ) as file:
#         article_json_str = file.read()

#     article_json = json.loads(article_json_str)

#     list_for_proccess = []
#     for index, value in enumerate(divide_dict(article_json, 3000)):
#         list_for_proccess.append(
#             {
#                 "num_of_file": index,
#                 "values": value,
#                 "df_articles_all": df_articles_all,
#                 "df_inproceedings_all": df_inproceedings_all,
#             }
#         )

#     pool = mp.Pool(2)
#     result = pool.map(proccess_features, list_for_proccess)


# if __name__ == "__main__":
#     main()
