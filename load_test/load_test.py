# load_test/load_test.py
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://127.0.0.1:8000/predict"

PAYLOAD = {
    "amount_cents": 500000,
    "transaction_country": "NG",
    "channel": "ONLINE",
    "entry_mode": "APP"
}

TOTAL_REQUESTS = 1000
CONCURRENCY = 20
TIMEOUT = 2


def send_request(session):
    start = time.perf_counter()
    resp = session.post(URL, json=PAYLOAD, timeout=TIMEOUT)
    latency_ms = (time.perf_counter() - start) * 1000
    return resp.status_code, latency_ms

def warmup(session, n=50):
    for _ in range(n):
        try:
            session.post(URL, json=PAYLOAD, timeout=TIMEOUT)
        except Exception:
            pass

def run_load_test():
    success = 0
    failures = 0
    latencies = []


    print(
        f"Running load test | total={TOTAL_REQUESTS}, "
        f"concurrency={CONCURRENCY}"
    )

    with requests.Session() as session:

        warmup(session)

        start_time = time.perf_counter()

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
                futures = [
                    executor.submit(send_request, session)
                    for _ in range(TOTAL_REQUESTS)
                ]

                for future in as_completed(futures):
                    try:
                        status, latency = future.result()
                        if status == 200:
                            success += 1
                            latencies.append(latency)
                        else:
                            failures += 1
                    except Exception:
                        failures += 1

    duration = time.perf_counter() - start_time
    rps = success / duration if duration > 0 else 0

    print("\n--- Load Test Results ---")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Concurrency:    {CONCURRENCY}")
    print(f"Successful:    {success}")
    print(f"Failed:        {failures}")
    print(f"Duration:      {duration:.2f} s")
    print(f"Throughput:    {rps:.2f} req/s")


if __name__ == "__main__":
    run_load_test()
