// RUN:
    // docker run --rm -i \
    // -v "$PWD/load_test:/src" \
    // --add-host=host.docker.internal:host-gateway \
    // grafana/k6 run /src/stress_test_realism.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween, randomItem } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  stages: [
    { duration: '10s', target: 50 },
    { duration: '30s', target: 50 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<100'],
    http_req_failed: ['rate<0.01'], // Zero errors allowed
  },
};

export default function () {
  const url = 'http://host.docker.internal:8000/predict';
  
  const rand = Math.random();
  let payload;

  if (rand < 0.6) {
    // === SCENARIO 1: The "Local Daily" (60%) ===
    // Regular Indian transactions
    payload = {
      amount_cents: randomIntBetween(100, 5000), 
      transaction_country: "IN",
      channel: randomItem(["POS", "ATM"]), // 'ATM' is valid in your data!
      entry_mode: randomItem(["CHIP", "SWIPE", "NFC"]) // Valid physical modes
    };

  } else if (rand < 0.7) {
    // === SCENARIO 2: The "High Spender" (10%) ===
    // Buying electronics online in India
    payload = {
      amount_cents: randomIntBetween(50000, 200000), 
      transaction_country: "IN",
      channel: "ONLINE",
      entry_mode: randomItem(["APP", "WEB"]) // 'WEB' is your 'Manual/CVV' equivalent
    };

  } else if (rand < 0.8) {
    // === SCENARIO 3: The "International Traveler" (10%) ===
    // Indians in UAE, Singapore, UK (Valid countries in your CSV)
    payload = {
      amount_cents: randomIntBetween(2000, 15000),
      transaction_country: randomItem(["AE", "SG", "GB", "US"]), 
      channel: "POS",
      entry_mode: "CHIP"
    };

  } else {
    // === SCENARIO 4: The "Attack" (20%) ===
    // Fraud Simulation using VALID schema values
    const isBot = Math.random() > 0.5;
    
    if (isBot) {
       // Bot Attack: High volume, small amounts, using WEB
       payload = {
         amount_cents: randomIntBetween(100, 5000), 
         transaction_country: randomItem(["US", "IN"]), // Bot pretending to be local
         channel: "ONLINE",
         entry_mode: "WEB" // Vulnerable mode
       };
    } else {
       // "Card Dump" Fraud: High amount, Swipe/NFC
       payload = {
         amount_cents: randomIntBetween(80000, 300000),
         transaction_country: "IN",
         channel: "POS",
         entry_mode: "SWIPE" // Magstripe fraud
       };
    }
  }

  const params = { headers: { 'Content-Type': 'application/json' } };
  const res = http.post(url, JSON.stringify(payload), params);
  
  // Debug: Print error if it happens
  if (res.status !== 200) {
      console.log(`Error ${res.status}: ${res.body}`);
  }

  check(res, { 'is status 200': (r) => r.status === 200 });
  sleep(Math.random() * 0.15 + 0.05);
}