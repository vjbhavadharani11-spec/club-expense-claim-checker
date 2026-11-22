# Cost and Latency Engineering Report

**Course:** CIT AI-Native Engineering Programme · Assessment 5  
**Project:** Club Expense Claim Checker  
**Target Platform:** Groq Cloud API  
**Target Model:** `llama-3.3-70b-versatile`  
**Pricing Source:** Groq Official Cloud Pricing Documentation (https://groq.com/pricing)  

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
*Note: Groq LPUs (Language Processing Units) deliver industry-leading inference speeds.*

- **Network Round Trip Time (RTT):** ~150 ms - 220 ms.
- **Inference Time (Groq LPU Llama-3.3-70B):** ~80 ms - 150 ms (speeds exceed 250-300 tokens/sec).
- **Total Expected Latency per API Call:** **~250 ms – 370 ms per claim** (synchronous single-item call).
- **Batch Processing for 50 Claims:**
  - *Sequential processing:* ~12 to 18 seconds total run time.
  - *Concurrent processing (ThreadPool):* Under 2 seconds total.
  - *Offline Deterministic Fallback:* **< 1 millisecond per claim** (0 network latency).

---

## 3. Financial Cost Estimation & Free-Tier Limits (Groq Official Rates)

### Official Pricing (Groq Llama-3.3-70b-versatile)
- **Input Tokens:** \$0.59 per 1,000,000 tokens (\$0.00059 / 1k tokens)
- **Output Tokens:** \$0.79 per 1,000,000 tokens (\$0.00079 / 1k tokens)
- **Free Developer Tier Limits:** Groq provides free access with limits of **30 Requests Per Minute (RPM)** and **6,000 Tokens Per Minute (TPM)**, and **14,400 Requests Per Day (RPD)**.
  - Our daily requirement is only 50 requests/day, which uses less than **0.35%** of the free daily allowance.

### Daily Cost Calculations (50 Claims on Paid Tier)
1. **Input Cost:**
   $$\text{Daily Input Tokens} = 50 \times 275 = 13,750 \text{ tokens}$$
   $$\text{Cost} = \frac{13,750}{1,000,000} \times \$0.59 = \$0.008112$$

2. **Output Cost:**
   $$\text{Daily Output Tokens} = 50 \times 45 = 2,250 \text{ tokens}$$
   $$\text{Cost} = \frac{2,250}{1,000,000} \times \$0.79 = \$0.001777$$

3. **Total Cost:**
   $$\text{Total Daily Cost} = \$0.008112 + \$0.001777 = \$0.009889 \text{ (approx. 0.99 US cents / ~0.82 INR)}$$
   $$\text{Monthly Cost (30 days)} \approx \$0.296 \text{ (~24.60 INR per month)}$$

*Conclusion:* On Groq Cloud, development and student testing is completely **free** under the Groq developer tier, and less than 1 rupee per day if billed under production usage.
