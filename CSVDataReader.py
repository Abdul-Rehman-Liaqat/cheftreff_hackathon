import pandas as pd

# Specify the correct encoding while reading the CSV file with pandas
df = pd.read_csv("data/MMX_Hackathon2025_year2021.csv", encoding="ISO-8859-1")

# Display the DataFrame (optional)
print(df)