import pandas as pd

# Read CSV files
df1 = pd.read_csv(
    "../data/research_age/index_dblp_all_citations_first_500_month.csv"
)  # Replace 'file1.csv' with your CSV file path
df2 = pd.read_csv(
    "../data/research_age/index_dblp_all_citations_first_500.csv"
)  # Replace 'file2.csv' with your CSV file path
df3 = pd.read_csv(
    "../data/research_age/index_dblp_all_first_500_filtered_types.csv"
)  # Replace 'file1.csv' with your CSV file path
df4 = pd.read_csv(
    "../data/research_age/index_dblp_journals_first_500_filtered_types.csv"
)
df4 = pd.read_csv("../data/research_age/dblp_all.csv")
# Concatenate DataFrames
merged_df = pd.concat([df1, df2, df3, df4])

# Remove duplicates based on a specific column or combination of columns
unique_values = merged_df.drop_duplicates(
    subset=["dblp_author_name"]
)  # Replace 'column_name' with your column name

# Save unique values to a new CSV file
unique_values.to_csv("../data/research_age/dblp_all_merged_final.csv", index=False)
