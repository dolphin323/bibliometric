import os
import csv

JOURNAL_VENUES = [
    "Inf. Softw. Technol.",
    "J. Syst. Softw.",
    "IEEE Trans. Software Eng.",
    "Softw. Pract. Exp.",
    "Softw. Test. Verification Reliab.",
    "ACM Trans. Program. Lang. Syst.",
    "ACM Trans. Softw. Eng. Methodol.",
    "J. Softw. Evol. Process.",
    "Int. J. Softw. Tools Technol. Transf.",
    "Empir. Softw. Eng.",
    "J. Softw. Evol. Process.",
]

CONFERENCES_VENUES = [
    "ICSA",
    "ASE",
    "ESOP",
    "ICSE",
    "SANER",
    "XP",
    "ISSTA",
    "ESEM",
    "ICSME",
    "PEPM@POPL",
    "EASE",
    "FASE",
]

# output_articles_path = "./output_filter_year_2016/output_article.csv"
# output_articles_filter_path = "./output_filter_venue_2016/output_article.csv"

# with open(output_articles_path, "r") as csv_file, open(
#     output_articles_filter_path, "w", newline=""
# ) as output_csv:
#     csv_reader = csv.DictReader(csv_file)

#     fieldnames = csv_reader.fieldnames

#     csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

#     csv_writer.writeheader()

#     for row in csv_reader:
#         if row["journal"] in JOURNAL_VENUES:
#             csv_writer.writerow(row)

output_inproceedings_path = "../data/output_filter_year_2016/output_inproceedings.csv"
output_inproceedings_filter_path = (
    "../data/conferences_including_comp_workshops_etc/output_venue_inproceedings.csv"
)

with open(output_inproceedings_path, "r") as csv_file, open(
    output_inproceedings_filter_path, "w", newline=""
) as output_csv:
    csv_reader = csv.DictReader(csv_file)

    fieldnames = csv_reader.fieldnames

    csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    csv_writer.writeheader()

    for row in csv_reader:
        for substring in CONFERENCES_VENUES:
            if substring in row["booktitle"].split():
                csv_writer.writerow(row)
        # return False
        # if row["booktitle"] in CONFERENCES_VENUES or row["booktitle"].endswith(" FSE"):
        #     csv_writer.writerow(row)
