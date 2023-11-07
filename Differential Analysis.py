import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

# Load the microbiome expression profile data in CSV format
# Replace "expression_profile.csv" with the actual filename and path of your data
data = pd.read_csv("genus.csv", index_col=0)

# Load the sample metadata
# Replace "metadata.csv" with the actual filename and path of your metadata file
metadata = pd.read_csv("metadata.csv", index_col=0)

# Merge the data and metadata based on sample names
data = data.merge(metadata, left_index=True, right_index=True)

# Extract the species columns from the data
species_columns = data.columns[:-3]

# Perform differential abundance analysis for each species
results = []
for species in species_columns:
    # Extract abundance values for the current species
    group1 = data[data['treatment'] == 'Healthy'][species].values
    group2 = data[data['treatment'] == 'marijuana'][species].values

    # Perform t-test to compare groups
    t_stat, p_value = ttest_ind(group1, group2)

    # Store the results
    result = {
        'Species': species,
        'Log2 Fold Change': np.log2(np.mean(group2) / np.mean(group1)),
        'P-value': p_value
    }
    results.append(result)

# Convert the results to a pandas DataFrame
results_df = pd.DataFrame(results)

# Filter significant results (adjust p-value threshold as desired)
significant_results = results_df[results_df['P-value'] < 0.05]

# Sort results by log2 fold change
significant_results = significant_results.sort_values(by='Log2 Fold Change', ascending=False)

# Print the top differentially abundant species
top_species = significant_results.head(10)  # Change the value to display more or fewer top species
print(top_species)

# Plot the top differentially abundant species
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.barh(y=top_species['Species'], width=top_species['Log2 Fold Change'], color='steelblue')
plt.xlabel('Log2 Fold Change')
plt.ylabel('Species')
plt.title('Differential Abundance Analysis')
plt.tight_layout()
plt.show()
