# load_test/latency_test.py
import requests
import time
import numpy as np

URL = "http://127.0.0.1:8000/predict"

PAYLOAD = {
    "amount_cents": 500000,
    "transaction_country": "NG",
    "channel": "ONLINE",
    "entry_mode": "APP"
}

def run_benchmark(n=200):
    latencies = []
    failures = 0

    session = requests.Session()

    print(f"Sending {n} requests to {URL}...")

    for _ in range(n):
        try:
            start = time.time()
            resp = session.post(URL, json=PAYLOAD, timeout=2)
            latency = (time.time() - start) * 1000

            if resp.status_code == 200:
                latencies.append(latency)
            else:
                failures += 1

            time.sleep(0.005)  # realistic pacing

        except Exception as e:
            failures += 1

    if not latencies:
        print("❌ All requests failed. Aborting stats.")
        return

    latencies = np.array(latencies)

    print("\n--- Latency Results ---")
    print(f"Total Requests: {n}")
    print(f"Successful:    {len(latencies)}")
    print(f"Failed:        {failures}")
    print(f"Average:       {np.mean(latencies):.2f} ms")
    print(f"Median (p50):  {np.percentile(latencies, 50):.2f} ms")
    print(f"95th % (p95):  {np.percentile(latencies, 95):.2f} ms")
    print(f"99th % (p99):  {np.percentile(latencies, 99):.2f} ms")

if __name__ == "__main__":
    run_benchmark()

# import requests
# import time
# import numpy as np

# # Endpoint URL
# URL = "http://127.0.0.1:8000/predict"

# # Payload (High-risk transaction to trigger full model path)
# PAYLOAD = {
#   "amount_cents": 500000,
#   "transaction_country": "NG",
#   "channel": "ONLINE",
#   "entry_mode": "APP"
# }

# def run_benchmark(n=200):
#     latencies = []
#     print(f"🚀 Sending {n} requests to {URL}...")

#     for i in range(n):
#         try:
#             start = time.time()
#             resp = requests.post(URL, json=PAYLOAD)
#             # Measure round-trip time in milliseconds
#             latency = (time.time() - start) * 1000
#             latencies.append(latency)
#         except Exception as e:
#             print(f"Request failed: {e}")

#     # Calculate Metrics
#     latencies = np.array(latencies)
#     p50 = np.percentile(latencies, 50)  # Median
#     p95 = np.percentile(latencies, 95)  # The Resume Metric
#     p99 = np.percentile(latencies, 99)  # The "Worst Case" (mostly)
    
#     print("\n--- 📊 Latency Results ---")
#     print(f"Total Requests: {n}")
#     print(f"Average:       {np.mean(latencies):.2f} ms")
#     print(f"Median (p50):  {p50:.2f} ms")
#     print(f"95th % (p95):  {p95:.2f} ms  <-- YOUR RESUME CLAIM")
#     print(f"99th % (p99):  {p99:.2f} ms")
    
#     if p95 < 10:
#         print("\n✅ PASSED: System meets the <10ms requirement.")
#     else:
#         print(f"\n⚠️ WARNING: p95 is {p95:.2f}ms (Target: <10ms)")

# if __name__ == "__main__":
#     # Ensure server is running first!
#     run_benchmark()