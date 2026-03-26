import pandas as pd

# Load the data
df = pd.read_excel('pqc_test_results.xlsx')

# Calculate averages per algorithm
averages = df.groupby('Algorithm')['Handshake_Time_ms'].mean()

# Define the baseline (Classical)
baseline = averages['x25519']

print("--- PQC Performance Analysis ---")
print(f"Classical Baseline (x25519): {baseline:.2f} ms\n")

# Calculate overhead for the others
for alg, avg in averages.items():
    if alg == 'x25519':
        continue
    
    overhead_ms = avg - baseline
    overhead_percent = (overhead_ms / baseline) * 100
    
    print(f"Algorithm: {alg}")
    print(f"  Avg Time: {avg:.2f} ms")
    print(f"  Latency Increase: +{overhead_ms:.2f} ms ({overhead_percent:.2f}%)")
    print("-" * 30)