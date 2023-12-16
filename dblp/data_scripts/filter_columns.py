import pandas as pd

output_inproceedings_filter_path = (
    "../data/conferences_including_comp_workshops_etc/output_venue_inproceedings.csv"
)
output_inproceedings_filter_columns_path = "../data/conferences_including_comp_workshops_etc/output_venue_columns_inproceedings.csv"

csv = pd.read_csv(output_inproceedings_filter_path)

# List of columns to keep
columns_to_keep = [
    "id",
    "title",
    "author",
    "booktitle",
    "ee",
    "year",
    "key",
    "journal",
]  # Specify the columns you want to keep

# Get columns that are present in the DataFrame and not in the list of columns to keep
columns_to_drop = [col for col in csv.columns if col not in columns_to_keep]

csv = csv.drop(columns_to_drop, axis=1)
csv.to_csv(output_inproceedings_filter_columns_path)
