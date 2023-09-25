import pandas as pd
import numpy as np

# Step 1: Generate 24-hour time slots with 5-min intervals
time_intervals = pd.date_range(start="00:00", end="23:59", freq="1T").time
df = pd.DataFrame(time_intervals, columns=["Time"])

# Step 2: Create a power consumption curve based on sinusoidal function
total_minutes = 24 * 60  # Total minutes in a day

# Generate energy values
df['Minutes'] = df['Time'].apply(lambda x: x.hour * 60 + x.minute)

# Sinusoidal function centered around midday (720 minutes)
amplitude = 25  # Maximum variation in energy consumption due to temperature
offset = 50  # Base energy consumption
df['Power'] = amplitude * np.sin(2 * np.pi * (df['Minutes'] - 720) / total_minutes) + offset

# Step 3: Add random noise to the data
noise = 0.05  # 5% noise
df['Power'] = df['Power'] * (1 + noise * (np.random.rand(len(df)) - 0.5))

# Step 4: Export to CSV
df.drop(columns=['Minutes'], inplace=True)
df.to_csv("24H_Industrial_Refrigeration_Data.csv", index=False)
