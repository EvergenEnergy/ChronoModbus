import pandas as pd
import numpy as np

# Step 1: Generate 24-hour time slots with 5-min intervals
time_intervals = pd.date_range(start="00:00", end="23:55", freq="5T").time
df = pd.DataFrame(time_intervals, columns=["Time"])

# Step 2: Create an energy production curve resembling a bell shape
active_start = 7 * 60  # 7am in minutes
active_end = 17 * 60  # 5pm in minutes
total_minutes = 24 * 60  # Total minutes in a day

# Calculate the mean and standard deviation for bell curve
mean_time = (active_start + active_end) // 2
std_deviation = (active_end - active_start) / 6
factor = 100

# Generate energy values
df['Minutes'] = df['Time'].apply(lambda x: x.hour * 60 + x.minute)
df['Energy'] = df['Minutes'].apply(
    lambda x: np.exp(-((x - mean_time) ** 2) / (2 * std_deviation ** 2)) if active_start <= x <= active_end else 0
)

# Normalise the Energy values
df['Energy'] = df['Energy'] / df['Energy'].max()

# Step 3: Add random noise to the data
noise = 0.05  # 5% noise
df['Energy'] = df['Energy'] * (1 + noise * (np.random.rand(len(df)) - 0.5))
df['Energy'] = df['Energy'] * 100


# Step 4: Export to CSV
df.drop(columns=['Minutes'], inplace=True)
df.to_csv("24H_PV_Farm_Data.csv", index=False)
