# Project Specification: Club Expense Claim Checker
**Course:** CIT AI-Native Engineering Programme · Semester 1 · Assessment 5  
**Student Project:** Individual Capstone Project  
**Domain:** College Club Finance & Audit  

---

## 1. Project Goal & System Boundary
The **Club Expense Claim Checker** is a Python-based console audit verification tool for student club expenditure claims. 
- **What it does:** Reads claim descriptions, invokes an LLM to extract structured claim facts (amount, category, bill attached status, short summary), verifies the extracted facts against raw note text using deterministic Python rules, checks club budgets and thresholds, and sorts each claim into an audit status.
- **System Boundary & Human Checkpoint:** The software **never makes payments or marks claims as "paid" / "approved"**. Its final output is an audit triage table (`payable.csv` and `review.csv`). The **faculty treasurer personally inspects bills and signs every payment decision**.

---

## 2. Input Specifications

### A. `claims.csv`
Contains raw expense submissions sorted in chronological order.
- **Columns:** `id`, `club`, `date`, `note`
- **Formatting Rule:** Notes containing commas (e.g. `"Rs. 1,250"`) must be enclosed in double quotes so standard CSV readers process them without splitting columns.
- **Dataset:** 22 realistic college club claims spanning 7 expense categories across 9 student clubs.

### B. `budgets.csv`
Defines the maximum spending limit allocated per club for each expense category.
- **Columns:** `category`, `limit_per_club`
- **Category Limits:**
  - `printing`: 2000 *(from course spec)*
  - `food`: 4000 *(from course spec)*
  - `equipment`: 10000 *(from course spec)*
  - `travel`: 5000 *(sample assumption)*
  - `prizes`: 4000 *(sample assumption)*
  - `costumes`: 5000 *(sample assumption)*
  - `other`: 3000 *(sample assumption)*

---

## 3. LLM Extraction Specification
The LLM extracts 4 fields as raw JSON:
```json
{
  "amount": 1250,
  "category": "printing",
  "bill": true,
  "summary": "Banner printing"
}
```
- **`amount`:** `integer` or `null`. Must match a total written in digits in the note. *Never calculate or infer an amount; never read numbers written solely in words.*
- **`category`:** One of `["printing", "food", "travel", "prizes", "equipment", "costumes", "other"]`.
- **`bill`:** `boolean` (`true` or `false`). `true` only if the note explicitly states a bill, receipt, invoice, or ticket is attached.
- **`summary`:** `string` (concise description, maximum 10 words).

---

## 4. Python Fact-Checking & Deterministic Validation Rules
To prevent hallucination, Python independently inspects the claim before running business logic:
1. **Fact Check - Amount:** Python extracts all numeric values (`numbers_in()`) from the raw note (handling commas like `"1,250"` -> `1250`). The LLM amount must be present in these numbers.
2. **Fact Check - Bill:** Python checks for bill-attestation keywords (bill, receipt, invoice, ticket) and verifies absence of negative qualifiers ("no bill", "lost", "missing", "later").
3. **Fallback & Robustness:** If the LLM returns invalid JSON, schema mismatches, or API exceptions, Python safely marks the claim as `needs_more_info` without crashing.

---

## 5. Strict Decision Priority Order
Claims are evaluated through a waterfall hierarchy:
1. `needs_more_info`: Amount is `null`, missing, or unverified by Python fact check.
2. `needs_bill`: `bill` is `false` (no bill/receipt attached).
3. `needs_approval`: Amount exceeds Rs. 5,000, OR multiple claims for the same club, same category, and same date together exceed Rs. 5,000 (potential split claim).
4. `over_budget`: The claim amount would cause the club's cumulative spend in that category to exceed `limit_per_club`.
5. `ok_to_pay`: None of the above flags apply.

*Crucial Accounting Rule:* **Only claims marked `ok_to_pay` count toward budget consumption.**

---

## 6. Output Specifications
1. **`payable.csv`**: Contains only `ok_to_pay` claims for the faculty treasurer's signature.
2. **`review.csv`**: Contains all flagged claims with the specific rejection reason and raw note.
3. **`results.csv`**: Master log containing all claims with final determined status.
4. **`summary.txt`**: Executive summary showing status counts, total amounts, and club category budget utilization.

---

## 7. Edge Cases & Handling
- **Commas in numbers (`Rs. 1,250`):** Normalized to integer `1250`.
- **Calculated amounts (`500 per person for 4`):** Strictly rejected / not computed; must be `null` or flagged.
- **Bill promised later / lost:** Treated as `bill: false` -> `needs_bill`.
- **Split claims on same date:** Accumulated per `(club, category, date)` tuple; if sum > 5000, marked `needs_approval`.
- **Budget overflow:** Running totals tracked with `(club, category)` dictionary keys.
