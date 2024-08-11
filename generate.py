import pandas as pd
import numpy as np

# Function to determine class based on parameters
def determine_class(params):
    # Extract parameters for each drone
    D1 = params[:4]
    D2 = params[4:8]
    D3 = params[8:12]
    D4 = params[12:16]
    D5 = params[16:]

    # Calculate scores for each drone
    def score(battery, distance, rest_time, cl_distance):
        return (60 - 1.5*distance) + battery + (rest_time / 10) - 2.5*cl_distance

    scores = {
        'D1': score(*D1),
        'D2': score(*D2),
        'D3': score(*D3),
        'D4': score(*D4),
        'D5': score(*D5)
    }
    
    # Find the class with the highest score
    return max(scores, key=scores.get)

# Create empty dataframe
columns = ['id', 'D1_1', 'D1_2', 'D1_3', 'D1_4', 'D2_1', 'D2_2', 'D2_3', 'D2_4',
           'D3_1', 'D3_2', 'D3_3', 'D3_4', 'D4_1', 'D4_2', 'D4_3', 'D4_4',
           'D5_1', 'D5_2', 'D5_3', 'D5_4', 'CLASS']
data = []

# Generate 200 rows of data
for i in range(1, 2000):
    # Random values within specified ranges for each drone
    params = []
    for _ in range(5):
        battery = np.random.randint(0, 101)
        distance = np.random.randint(0, 30)
        rest_time = np.random.randint(0, 301)
        cl_distance = np.random.choice([-5] + list(range(0, 30)))
        params.extend([battery, distance, rest_time, cl_distance])
    
    # Determine class label
    class_label = determine_class(params)
    
    # Append row with an id
    data.append([i] + params + [class_label])

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to CSV file
df.to_csv('drone_classification_data_extended.csv', index=False)

print("Data generation complete. 200 rows saved to 'drone_classification_data_extended.csv'.")
