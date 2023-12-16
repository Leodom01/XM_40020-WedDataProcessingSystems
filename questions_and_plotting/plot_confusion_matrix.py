#AI GENERATED DO NOT SUBMIT

import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('questions.csv')

# Get the last two columns
y_true = df.iloc[:, -2]
y_pred = df.iloc[:, -1]

# Compute the confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Plot the confusion matrix
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

# Save the plot to a file
plt.savefig('confusion_matrix.png')

# Show the plot
plt.show()

