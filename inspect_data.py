import pandas as pd

df = pd.read_csv("/home/ubuntu/upload/mindMonitor_2026-01-12--20-17-092.csv", header=1)
print("Data Shape:", df.shape)
print("\n--- Row 98 ---")
print(df.iloc[98].iloc[31:36])
print("\n--- Row 99 ---")
print(df.iloc[99].iloc[31:36])
print("\n--- Row 100 ---")
print(df.iloc[100].iloc[31:36])
print("\n--- Row 101 ---")
print(df.iloc[101].iloc[31:36])
