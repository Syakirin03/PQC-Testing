notes: Script used will be added on later date, as well as example of successful run

Markdown
# Post-Quantum Cryptography (PQC) TLS 1.3 Performance Benchmark

## 📌 Project Summary
This repository contains the benchmarking suite and network analysis tools developed for a university thesis on Network Security. The project measures the real-world performance impact of migrating from classical cryptographic algorithms to quantum-resistant (Post-Quantum) algorithms within a TLS 1.3 tunnel.

By utilizing a custom-compiled OpenSSL server with the `oqsprovider` (liboqs), this project captures precise handshake latency and packet fragmentation data across different security levels. 

**Algorithms Analyzed:**
* **X25519** (Classical Baseline)
* **ML-KEM-768 & ML-KEM-1024** (NIST Standardized Lattice-based KEMs)
* **X25519MLKEM768** (Industry-Standard Hybrid Key Exchange)
* **FrodoKEM-1344-AES** (Conservative / Heavyweight Baseline)

## 🗂️ Repository Contents

* `benchmark_pqc.py`: The client-side Python script that automates socket connections and records handshake latencies in milliseconds.

* `visualize_pqc.py`: Data analysis script using `pandas` and `seaborn` to calculate overhead percentages and generate comparison charts.

* `pqc_test_results.xlsx`: The raw statistical output of the benchmark runs.

* `pqc_handshake.pcap`: Sample Wireshark packet capture demonstrating TCP fragmentation caused by large PQC public keys.

---
Step-by-Step Reproduction Guide

### 1. Prerequisites

To run this lab, you must have a Linux environment (e.g., Ubuntu via VirtualBox) with OpenSSL natively compiled to include the Open Quantum Safe provider (`oqsprovider`). You can visit the official github oqs provider project repo on how to set up the enviroment, ensure you test all the algorithms are available for you to use

Set up your Python virtual environment and install dependencies:

bash

`python3 -m venv pqc_test`

`source pqc_test/bin/activate`

`pip install pandas openpyxl matplotlib seaborn`

2. Start the OpenSSL PQC Server
The OpenSSL server acts as the target for our TLS 1.3 handshakes. It must be explicitly configured to accept classical, standalone PQC, and hybrid key exchange groups.
`
Run the following command in a dedicated terminal:

Bash

`openssl s_server -provider oqsprovider -provider default \`
 ` -cert server.crt -key server.key -www -tls1_3 \`
`  -groups x25519:mlkem768:X25519MLKEM768:mlkem1024:frodo1344aes \`
`  -port 4433`
  `
  
3. Capture Network Traffic (Optional but Recommended)
To analyze payload sizes and packet fragmentation, start a tcpdump capture on the loopback interface before running the benchmark:


Bash

`sudo tcpdump -i lo port 4433 -w pqc_handshake.pcap`

4. Run the Benchmark
Execute the Python automation script. The script will negotiate 10 separate TLS 1.3 handshakes for each algorithm, calculating the time taken from the initial TCP SYN to the finalized TLS session.

Bash

`python3 benchmark_pqc.py`

Expected Output: The script will print the success rate (e.g., 10/10 successful) and export the raw timing data to pqc_test_results.xlsx. You can change how many test you want to run directly in the script

5. Data Visualization and Analysis

Once the benchmark completes, run the visualization script to calculate the exact latency overhead and generate the comparative bar chart.

Bash

`python3 visualize_pqc.py`
