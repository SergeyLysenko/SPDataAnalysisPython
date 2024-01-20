import pandas as pd

# Load all tables from the URL into a list
south_park_tables = pd.read_html(
      "https://en.wikipedia.org/wiki/List_of_South_Park_episodes"
)

# Select and concatenate the specified tables
selected_tables = [south_park_tables[i] for i in range(1, 27)]
south_park_data = pd.concat(selected_tables).convert_dtypes()

# Rename columns if necessary
new_column_names = {
     "No. overall": "Number",
     "No. in season": "# in season",
}
data = south_park_data.rename(columns=new_column_names)

# Find all columns that contain the phrase 
air_date_columns = [col for col in data.columns if "Original air date" in col]
prod_code_columns = [col for col in data.columns if "Prod. code " in col]
viewers_columns = [col for col in data.columns if "Viewers" in col or "viewers" in col]


# Verify the identified columns
print("Identified air date columns:", air_date_columns)
print("Identified Prod. code columns:", prod_code_columns)
print("Identified viewers_columns columns:", viewers_columns)

# Combine these columns into a single column
# For each row, select the first non-null value from the original  columns
data['Air Date'] = data[air_date_columns].bfill(axis=1).iloc[:, 0]
data['Prod Code'] = data[prod_code_columns].bfill(axis=1).iloc[:, 0]
data['Viewers (millions)'] = data[viewers_columns].bfill(axis=1).iloc[:, 0]

# Drop the original air date columns with footnote indicators
data = data.drop(columns=air_date_columns)
data = data.drop(columns=prod_code_columns)
data = data.drop(columns="U.S. viewers (millions)")
# Display the DataFrame's column names to confirm
print(data.columns)
data