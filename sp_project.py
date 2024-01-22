import pandas as pd
import re

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


 #Function to clean strings by removing text in brackets
def clean_string(s):
    if isinstance(s, str):
        return re.sub(r"\[.*?\]", "", s)
    else:
        return s

# Apply the cleaning function to each column in the DataFrame
for column in data.columns:
    data[column] = data[column].apply(clean_string)


# Find all columns that contain the phrase 
air_date_columns = [col for col in data.columns if "Original air date" in col or "Original release date" in col]
prod_code_columns = [col for col in data.columns if "Prod. code" in col or "Prod. code [399]" in col]
viewers_columns = [col for col in data.columns if "Viewers" in col or "viewers" in col]


# Verify the identified columns
print("Identified air date columns:", air_date_columns)
print("Identified Prod. code columns:", prod_code_columns)
print("Identified viewers_columns columns:", viewers_columns)

# Combine these columns into a single column
# For each row, select the first non-null value from the original  columns
data['Air Date'] = data[air_date_columns].bfill(axis=1).iloc[:, 0]
data['Prod. Code'] = data[prod_code_columns].bfill(axis=1).iloc[:, 0]
data['Viewers (millions)'] = data[viewers_columns].bfill(axis=1).iloc[:, 0]

# Drop the original air date columns with footnote indicators
data = data.drop(columns=air_date_columns)
data = data.drop(columns=prod_code_columns)
data = data.drop(columns="U.S. viewers (millions)")



# Update the "Viewers (millions)" column
data = data.assign(
    **{
        "Viewers (millions)": lambda df: (
            df["Viewers (millions)"]
            .str.extract(r'(\d+\.\d+|\d+)')  # Extract the first number (float or integer)
            [0]  # Extract returns a DataFrame; select the first column
            .astype("Float64")  # Convert the column to Float64
        )
    }
)
# Display the updated DataFrame
#print(data["Viewers (millions)"])





# Display the updated DataFrame for "Prod. code"
#print(data['Prod. code'])
#print(data["Prod. code"].sample(20))


#Convert column "Air Date" to date format
data['Air Date'] = pd.to_datetime(data['Air Date'], errors='coerce')



# Convert all columns of type 'object' to 'string'
for column in data.columns:
    if data[column].dtype == 'object':
        data[column] = data[column].astype(str)


# Verify the changes
#print(data['Air Date'].head())
#print(data.info())





#print(data.columns)
#data
#data.info()
#print(data["Air Date"].sample(20))


#data["Directed by"].value_counts()
#print(data.columns)
#data["Written by"].value_counts()
data[[ "Directed by"]].describe()
#data["Written by"].value_counts()
data[[ "Viewers (millions)"]].describe()

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter(data["Viewers (millions)"], data["# in season"])
ax.set_title("Scatter Plot of Viewers")
ax.set_xlabel("Average Viwers")
ax.set_ylabel("# in season")
fig.show()

from sklearn.linear_model import LinearRegression
x = data.loc[:, ["Viewers (millions)"]]
y = data.loc[:, "# in season"]

model = LinearRegression()
model.fit(x, y)
r_squared = f"R-Squared: {model.score(x, y):.2f}"
best_fit = f"y = {model.coef_[0]:.4f}x{model.intercept_:+.4f}"
y_pred = model.predict(x)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.plot(x, y_pred, color="red")
ax.text(7.25, 5.5, r_squared, fontsize=10)
ax.text(7.25, 7, best_fit, fontsize=10)
ax.set_title("Scatter Plot of Ratings")
ax.set_xlabel("Average IMDb Rating")
ax.set_ylabel("Average Rotten Tomatoes Rating")
fig.show()

# Calculate average viewers per season
average_viewers_per_season = data.groupby('# in season')['Viewers (millions)'].mean()

# Create the scatter plot
fig, ax = plt.subplots()
ax.scatter(data["Viewers (millions)"], data["# in season"])

# Plot the average viewers per season
# Here, we use a different marker style for averages
ax.scatter(average_viewers_per_season, average_viewers_per_season.index, color='red', marker='x', label='Average per Season')

# Adding labels and title
ax.set_title("Scatter Plot of Viewers")
ax.set_xlabel("Viewers (millions)")
ax.set_ylabel("# in Season")

# Add a legend
ax.legend()

# Show the plot
plt.show()