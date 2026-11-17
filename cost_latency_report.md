# Cost and Latency Engineering Report

**Course:** CIT AI-Native Engineering Programme · Assessment 5  
**Project:** Club Expense Claim Checker  
**Target Model:** Google Gemini 1.5 Flash (via Gemini API)  
**Pricing Source:** Google Cloud Vertex AI / Gemini API Official Public Pricing (Standard Tier)  

---

## 1. Operational Workload Assumptions (1 Day of Input)
- **Daily Volume:** 50 expense claims submitted across all campus clubs on an active event day.
- **API Calls:** 1 API call per submitted claim = **50 API calls/day**.
- **Token Estimation per Call:**
  - **System Prompt:** ~250 tokens (Authority, Exemplar, Constraint, Rubric, Metadata).
  - **User Input Note:** ~25 tokens per claim description.
  - **Total Input Tokens:** ~275 tokens per call.
  - **LLM Output (JSON):** ~45 tokens per call (`{"amount": 1250, "category": "printing", "bill": true, "summary": "..."}`).

---

## 2. Latency Benchmarks
*Note: Latency depends on server region, network round-trip time (RTT), and concurrent load.*

- **Network Round Trip Time (RTT):** ~150 ms - 250 ms.
- **Model Time-to-First-Token & Generation (Gemini 1.5 Flash):** ~300 ms - 450 ms.
- **Total Expected Latency per API Call:** **~500 ms – 750 ms per claim** (synchronous single-item call).
- **Batch Processing for 50 Claims:**
  - *Sequential processing:* ~30 to 40 seconds total run time.
  - *Concurrent processing (ThreadPool):* Under 5 seconds total.
  - *Offline Deterministic Fallback:* **< 1 millisecond per claim** (0 network latency).

---

## 3. Financial Cost Estimation per Day

### Official Pricing (Gemini 1.5 Flash)
- **Input Tokens (Prompts <= 128k):** \$0.075 per 1,000,000 tokens (\$0.000075 / 1k tokens)
- **Output Tokens:** \$0.30 per 1,000,000 tokens (\$0.00030 / 1k tokens)
- **Free Tier Allowance:** Gemini API offers up to 15 Requests Per Minute (RPM) completely free of charge.

### Daily Cost Calculations (50 Claims)
1. **Input Cost:**
   $$\text{Daily Input Tokens} = 50 \times 275 = 13,750 \text{ tokens}$$
   $$\text{Cost} = \frac{13,750}{1,000,000} \times \$0.075 = \$0.001031$$

2. **Output Cost:**
   $$\text{Daily Output Tokens} = 50 \times 45 = 2,250 \text{ tokens}$$
   $$\text{Cost} = \frac{2,250}{1,000,000} \times \$0.30 = \$0.000675$$

3. **Total Cost:**
   $$\text{Total Daily Cost} = \$0.001031 + \$0.000675 = \$0.001706 \text{ (approx. 0.17 US cents / ~0.14 INR)}$$
   $$\text{Monthly Cost (30 days)} \approx \$0.051 \text{ (~4.25 INR per month)}$$

*Conclusion:* The tool operates virtually cost-free on the Google Gemini Free Tier, and costs less than 15 paise per day even when scaled to paid tier billing.
