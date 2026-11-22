# Club Expense Claim Checker
**CIT AI-Native Engineering Programme · Semester 1 · Capstone Project (Assessment 5)**

An automated financial audit triage assistant for college club expense claims. The system uses a Large Language Model (**Groq API** running `llama-3.3-70b-versatile`) guided by a 5-role prompt to extract structured claim details, independently verifies all data with deterministic Python validation rules, enforces category budgets and split-claim detection, and outputs structured audit reports for the faculty treasurer.

---

## 📌 Key Architectural Principles
1. **Never Pays Money:** The tool is strictly a triage tool; it pays nothing and never marks claims as "approved" or "paid".
2. **Human Checkpoint:** The faculty treasurer physically inspects paper/digital bills and signs every reimbursement.
3. **Zero-Trust Validation:** Python independently checks that amounts exist verbatim in the claim note and verifies bill attestation.
4. **Defense Against Adversarial Inputs:** Resists prompt injection, calculation traps, and split-claim threshold evasion.

---

## 📂 Project Repository Structure
```text
club-expense-claim-checker/
│
├── claims.csv              # Input: 22 student club claims in date order
├── budgets.csv             # Input: Category spending limits per club
│
├── system_prompt.txt       # 5-role system prompt (Authority, Exemplar, Constraint, Rubric, Metadata)
├── llm_client.py           # Groq API integration (llama-3.3-70b-versatile) with offline fallback
├── expense_checker.py      # Core program with validation & decision functions
├── main.py                 # Primary entry point with formatted terminal dashboard output
├── test_single_claim.py    # Checkpoint 2 single claim test runner
├── test_suite.py           # Checkpoint 4 test harness (5 status claims + 3 red-team attacks)
│
├── payable.csv             # Output: Only claims marked OK to pay
├── review.csv              # Output: Flagged claims with reason and raw note
├── results.csv             # Output: Master record of all claims and statuses
├── summary.txt             # Output: Executive summary and club budget utilization tables
├── dashboard.html          # Interactive visual web dashboard (open directly in browser)
├── presentation.pptx       # 10-slide PowerPoint presentation with presenter notes
├── presentation_guide.pdf  # Complete presenter notes & simple English speaker script
│
├── spec.md                 # One-page Project Specification
├── judgment_framework.md   # Judgment Framework & Risk Matrix
├── cost_latency_report.md  # Detailed Cost and Latency Engineering Analysis (Groq LPU)
├── ai_decision_journal.md  # Architecture trade-offs and design rationale
├── reflection.md           # 400-word Capstone Project Reflection
├── .env.example            # Sample environment variables template
├── .gitignore              # Protects .env and Python cache from Git tracking
└── README.md               # Complete project documentation and guide
```

---

## 🚀 Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10+ installed.
- (Optional) Groq API Key from [Groq Console](https://console.groq.com/keys).

### 2. Environment Configuration
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(If no API key is provided, the system seamlessly uses its built-in deterministic fallback extractor for offline grading and demonstration).*

### 3. Run Checkpoint 2 (Single Claim Test)
```bash
python test_single_claim.py
```

### 4. Run Main Application (Processes All 22 Claims)
```bash
python main.py
```
This prints the terminal dashboard and generates `payable.csv`, `review.csv`, `results.csv`, `summary.txt`, and updates `dashboard.html`.

### 5. Run Stage 4 Evaluation & Red-Team Test Suite
```bash
python test_suite.py
```
Executes all 5 status evaluation checks and 3 adversarial red-team tests.

---

## ⚙️ Decision Rules Waterfall Order
Claims are processed through `decide()` in this strict priority:
1. `needs_more_info`: Missing, zero, or unverified amount.
2. `needs_bill`: Missing bill or receipt.
3. `needs_approval`: Single claim > Rs. 5,000, OR combined claims on same date for same club & category > Rs. 5,000.
4. `over_budget`: Spend in that category exceeds club limit.
5. `ok_to_pay`: Passes all checks. *Only these claims count towards the budget.*

---

## 📊 Summary of Audit Results (22 Claims)
- `ok_to_pay`: 14 claims (Rs. 30,650 approved)
- `needs_bill`: 2 claims
- `needs_approval`: 2 claims
- `over_budget`: 3 claims
- `needs_more_info`: 1 claim
