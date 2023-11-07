import pandas as pd
import csv

# Load your microbiome profile data into a pandas DataFrame called 'data'
data = pd.read_csv('genus.csv', index_col=0)  # Assuming the first column contains species names

# Compute the correlation matrix
correlation_matrix = data.corr()

# Set a threshold for the correlation coefficient
threshold = 0.7

# Find the edge list based on the correlation coefficient
edges = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        correlation = correlation_matrix.iloc[i, j]
        if abs(correlation) > threshold:
            species_1 = correlation_matrix.columns[i]
            species_2 = correlation_matrix.columns[j]
            edges.append((species_1, species_2, correlation))

# Print the edge list
print("Edge List:")
for edge in edges:
    species_1, species_2, correlation = edge
    print(f"{species_1} -- {species_2} (Correlation: {correlation})")

# Save the edge list to a CSV file
output_file = 'edge_list.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Species 1', 'Species 2', 'Correlation'])
    writer.writerows(edges)

print(f"Edge list saved to '{output_file}'.")
