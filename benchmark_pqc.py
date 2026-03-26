import subprocess
import time
import pandas as pd
import os

# Define the algorithms you want to compare
# Included mlkem768 (Kyber) which is the current NIST standard
algorithms = ["x25519", "mlkem768", "X25519MLKEM768", "mlkem1024"]
iterations = 500  # Number of tests per algorithm
final_data = []

def run_test_with_timing(kem_alg):
    my_env = os.environ.copy()
    my_env["OPENSSL_MODULES"] = "/home/kirin/oqs-provider/_build/lib"
    
    # We use -brief and piping < /dev/null to ensure the client closes immediately
    cmd = f"openssl s_client -connect localhost:4433 -groups {kem_alg} -provider oqsprovider -provider default -brief < /dev/null"
    
    start_time = time.perf_counter()
    try:
        process = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            env=my_env,
            timeout=5
        )
        end_time = time.perf_counter()
        
        if process.returncode == 0:
            # Convert to milliseconds
            return (end_time - start_time) * 1000
        return None
    except Exception:
        return None

print("Starting PQC Benchmark...")

for alg in algorithms:
    print(f"Testing {alg}...", end=" ", flush=True)
    success_count = 0
    for i in range(iterations):
        elapsed = run_test_with_timing(alg)
        if elapsed is not None:
            final_data.append({"Algorithm": alg, "Handshake_Time_ms": round(elapsed, 2)})
            success_count += 1
    print(f"Done ({success_count}/{iterations} successful)")

# Save to Excel
df = pd.DataFrame(final_data)
df.to_excel("pqc_test_results.xlsx", index=False)
print("\nResults saved to pqc_test_results.xlsx")