import csv
import requests
from tqdm import tqdm

output_inproceedings_filter_path = "../data/conferences_including_comp_workshops_etc/output_venue_columns_inproceedings.csv"
output_inproceedings_filter_columns_path = "../data/conferences_including_comp_workshops_etc/output_venue_columns_inproceedings_added_data.csv"


# Function to add a named new column
def add_named_column(input_file, output_file):
    # Open the input CSV file for reading
    with open(input_file, "r", newline="") as infile:
        reader = csv.reader(infile)
        # Get the header row
        header = next(reader)
        # Add the new column name to the header
        header.append("cited_by_count")
        header.append("publication_date")
        header.append("publication_year")

        # Create a list to hold the rows with the added column
        rows = [header]

        # Open the output CSV file for writing
        with open(output_file, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            # Write the rows with the added column and named header to the new CSV file
            writer.writerows(rows)

            # for _ in range(931):
            #     next(reader)

            # Read and process rows from the start index
            rows_from_index = list(reader)

            # Iterate through each row in the CSV
            for row in tqdm(rows_from_index):
                try:
                    doi_link = [
                        string
                        for string in row[4].split("|")
                        if string.startswith("https://doi.org/")
                    ][0]
                    # print(doi_link)
                    response = requests.get(
                        f"https://api.openalex.org/works/{doi_link}"
                    )
                    # print(response)
                    response_data = response.json()
                    # Modify row or add new column here
                    # For example, adding a new column with a constant value 'New Value'
                    row.append(response_data.get("cited_by_count", ""))
                    row.append(response_data.get("publication_date", ""))
                    row.append(response_data.get("publication_year", ""))
                    writer.writerow(row)
                except:
                    print(row)
                # writer.writerow(row)
                # # Append the modified row to the list
                # rows.append(row)

    # # Open the output CSV file for writing
    # with open(output_file, "w", newline="") as outfile:
    #     writer = csv.writer(outfile)
    #     # Write the rows with the added column and named header to the new CSV file
    #     writer.writerows(rows)


add_named_column(
    output_inproceedings_filter_path, output_inproceedings_filter_columns_path
)
