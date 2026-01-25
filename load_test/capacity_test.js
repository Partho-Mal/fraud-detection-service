// docker run --rm -i -v "$PWD/load_test:/src" --add-host=host.docker.internal:host-gateway grafana/k6 run /src/capacity_test.js

// RUN:
// docker run --rm -i \
//   -v "$PWD/load_test:/src" \
//   --add-host=host.docker.internal:host-gateway \
//   grafana/k6 run /src/capacity_test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween, randomItem } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  // Key FAANG Metric: "Graceful Failure"
  // We test if the system sheds load (returns 503) instead of crashing (timeouts/500s)
  thresholds: {
    // Allow up to 5% failure rate during peak saturation (Load Shedding is expected)
    http_req_failed: ['rate<0.05'], 
    // Latency must stay under SLA (300ms) for 95% of successful requests
    http_req_duration: ['p(95)<300'], 
  },
  scenarios: {
    ramp_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        // 1. Warm Up (Safe Zone)
        { duration: '30s', target: 20 }, 
        // 2. Load Zone (Saturation Point)
        { duration: '30s', target: 40 }, 
        // 3. Stress Zone (Overload / Breaking Point)
        { duration: '30s', target: 60 }, 
        // 4. Cooldown
        { duration: '10s', target: 0 },  
      ],
      gracefulRampDown: '5s',
    },
  },
};

export default function () {
  const url = 'http://host.docker.internal:8000/predict';
  
  const rand = Math.random();
  let payload;

  // --- TRAFFIC PATTERN GENERATOR (Realism) ---
  if (rand < 0.6) {
    // === SCENARIO 1: The "Local Daily" (60%) ===
    // Regular Indian transactions
    payload = {
      transaction_id: `tx_${randomIntBetween(100000, 999999)}`,
      amount_cents: randomIntBetween(100, 5000), 
      transaction_country: "IN",
      channel: randomItem(["POS", "ATM"]), 
      entry_mode: randomItem(["CHIP", "SWIPE", "NFC"]) 
    };

  } else if (rand < 0.7) {
    // === SCENARIO 2: The "High Spender" (10%) ===
    // Buying electronics online in India
    payload = {
      transaction_id: `tx_${randomIntBetween(100000, 999999)}`,
      amount_cents: randomIntBetween(50000, 200000), 
      transaction_country: "IN",
      channel: "ONLINE",
      entry_mode: randomItem(["APP", "WEB"]) 
    };

  } else if (rand < 0.8) {
    // === SCENARIO 3: The "International Traveler" (10%) ===
    // Indians in UAE, Singapore, UK (Valid countries in your CSV)
    payload = {
      transaction_id: `tx_${randomIntBetween(100000, 999999)}`,
      amount_cents: randomIntBetween(2000, 15000),
      transaction_country: randomItem(["AE", "SG", "GB", "US"]), 
      channel: "POS",
      entry_mode: "CHIP"
    };

  } else {
    // === SCENARIO 4: The "Attack" (20%) ===
    // Fraud Simulation
    const isBot = Math.random() > 0.5;
    
    if (isBot) {
       // Bot Attack: High volume, small amounts
       payload = {
         transaction_id: `tx_bot_${randomIntBetween(100000, 999999)}`,
         amount_cents: randomIntBetween(100, 5000), 
         transaction_country: randomItem(["US", "IN"]), 
         channel: "ONLINE",
         entry_mode: "WEB"
       };
    } else {
       // "Card Dump" Fraud: High amount, Swipe/NFC
       payload = {
         transaction_id: `tx_fraud_${randomIntBetween(100000, 999999)}`,
         amount_cents: randomIntBetween(80000, 300000),
         transaction_country: "IN",
         channel: "POS",
         entry_mode: "SWIPE" 
       };
    }
  }

  const params = { headers: { 'Content-Type': 'application/json' } };
  const res = http.post(url, JSON.stringify(payload), params);
  
  // Debug: Print unexpected errors (Ignore 503 as it is expected load shedding)
  if (res.status !== 200 && res.status !== 503) {
      console.log(`Unexpected Error ${res.status}: ${res.body}`);
  }

  // We check for 200 (Success) OR 503 (Graceful Shedding)
  // This distinguishes "Controlled Failure" from "Crashes"
  check(res, { 
    'is handled gracefully': (r) => r.status === 200 || r.status === 503,
    'is success (200)': (r) => r.status === 200
  });

  // Short sleep to simulate real user pacing (0.05s to 0.2s)
  sleep(Math.random() * 0.15 + 0.05);
}