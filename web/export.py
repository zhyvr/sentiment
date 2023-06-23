import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Retrieve data from the input_data table
cursor.execute('SELECT sentence, sentiment FROM input_data')
data = cursor.fetchall()

# Define the output CSV file path
csv_file = 'output.csv'

# Write the data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['sentence', 'sentiment'])  # Write header row
    writer.writerows(data)  # Write data rows

print(f'Data exported to {csv_file} successfully!')

# Close the database connection
conn.close()
