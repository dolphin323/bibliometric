import os
import csv

# Directory containing CSV files
directory_path = "./output_csv"

START_YEAR = 2016
# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)

        output_file = "./output_filter_year_2016/" + filename
        # Process the CSV file
        with open(file_path, "r") as csv_file, open(
            output_file, "a", newline=""
        ) as output_csv:
            csv_reader = csv.DictReader(csv_file, delimiter=";")

            fieldnames = csv_reader.fieldnames

            # Prepare writer for the output CSV file
            csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

            # Write header to output file if it's empty
            if os.stat(output_file).st_size == 0:
                csv_writer.writeheader()

            # Iterate through each row in the CSV file
            for row in csv_reader:
                # Check if the column value matches the filter condition
                if row["year"] and int(row["year"]) >= START_YEAR:
                    # Write the filtered row to the output CSV file
                    csv_writer.writerow(row)
