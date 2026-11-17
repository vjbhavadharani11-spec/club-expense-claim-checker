# Judgment Framework & Human Safeguard Architecture

**Course:** CIT AI-Native Engineering Programme · Assessment 5  
**Project:** Club Expense Claim Checker  

---

## 1. System Evaluation Matrix

| Decision Domain | Claim Wrongly Marked `ok_to_pay` (False Positive) | Claim Wrongly Sent to `review.csv` (False Negative) | Mitigating Architecture / Rule |
| :--- | :--- | :--- | :--- |
| **Receipt / Bill Verification** | College disburses money for unverified or fabricated claims. Potential financial embezzlement or audit query by external university regulators. | Student or club representative experiences minor administrative delay. They must physically produce receipt or clarify with treasurer. | Python `check_facts()` independently inspects keyword attestation and negations ("no bill", "lost", "coming later") before permitting `bill = True`. |
| **Amount Extraction & Factuality** | Incorrect reimbursement (e.g. paying Rs. 6,000 for a 6-person Rs. 250 meal due to hallucinated multiplication). Risk of financial loss. | Claim routed to `needs_more_info`. Treasurer manually checks the actual physical receipt. | Python `numbers_in()` verifies that the LLM amount exists verbatim as digits in the note. Calculations are strictly disallowed. |
| **Single Claim Threshold (> Rs. 5,000)** | Bypasses higher faculty authorization; large unauthorized capital purchase slips through without sanction. | High-value claim requires extra signature. Delays payment by 1–2 days for committee review. | Strict threshold check in `decide()`: any amount > 5,000 routes immediately to `needs_approval`. |
| **Split Claim Detection** | Club evades scrutiny by submitting two claims of Rs. 3,000 and Rs. 2,800 on the same day for the same event category. | Legitimate multiple small purchases on the same day require faculty treasurer sign-off. | Daily aggregation using `(club, category, date)` dictionary keys. Triggers `needs_approval` if combined sum > Rs. 5,000. |
| **Budget Enforcement** | Club exceeds semester financial allocation. College funds run into deficit; other clubs starved of funds. | Legitimate purchase delayed until budget reallocation or supplementary grant is approved. | Cumulative spending tracked using `(club, category)` tuple keys. Over-limit claims flagged as `over_budget`. |

---

## 2. Risk Comparison & Philosophy
- **Impact Asymmetry:** In financial governance, a **False Positive** (`ok_to_pay` when it should not be) causes irreversible financial loss and compliance violations. A **False Negative** (`review.csv` when it is legitimate) causes a temporary human delay that is quickly corrected during manual inspection.
- **Fail-Safe Design:** All edge cases, uncertainties, and API communication errors safely route claims into `review.csv` (`needs_more_info`), ensuring zero unauthorized disbursements.

---

## 3. Human Checkpoint
- **Non-Negotiable Boundary:** The automated software **NEVER** makes payments, issues bank transfers, or marks claims as "approved" or "paid".
- **Faculty Treasurer Role:** The faculty treasurer reviews `payable.csv`, physically inspects the attached paper/digital tax invoice, confirms receipt validity against physical goods received, and signs every physical disbursement order.
