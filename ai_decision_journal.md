# AI Decision Journal: Engineering Trade-offs & Architecture Decisions

**Course:** CIT AI-Native Engineering Programme · Assessment 5  
**Project:** Club Expense Claim Checker  

---

### Decision 1: Hybrid Architecture (LLM Fact Extraction + Deterministic Python Rules)
- **Problem:** Should we let the LLM make the final payment decision (e.g. prompt it: *"Decide if this claim is ok to pay"*), or restrict it strictly to information extraction?
- **Decision:** Restrict LLM to structured entity extraction (`amount`, `category`, `bill`, `summary`) and execute all decision rules (`decide()`) strictly inside deterministic Python code.
- **Rationale:** LLMs are probabilistic models prone to hallucinations, prompt injections, and arithmetic errors. Financial governance demands 100% deterministic, auditable decisions. Python enforces exact budget thresholds and mathematical comparisons without variability.

---

### Decision 2: 5-Role System Prompting Framework
- **Problem:** How to prevent the LLM from hallucinating missing numbers or trying to calculate per-person costs?
- **Decision:** Structured prompt using Authority, Exemplar, Constraint, Rubric, and Metadata roles.
- **Rationale:** Clear Constraints ("Never calculate", "Never read words as numbers") combined with few-shot Exemplars give the model explicit reference boundaries, dramatically reducing schema non-compliance and hallucinations.

---

### Decision 3: Zero-Trust Python Fact-Checking (`check_facts` & `numbers_in`)
- **Problem:** What if the LLM invents a number or ignores a "no bill" note?
- **Decision:** Python independently parses digits from the raw note text and cleans commas (`"1,250"` -> `1250`). If the LLM amount is not in the text numbers, Python rejects it immediately.
- **Rationale:** Establishes defense-in-depth: Never trust LLM output without code-level verification.

---

### Decision 4: Split Claim Detection with Tuple Keys `(club, category, date)`
- **Problem:** Clubs might split a large purchase (e.g. Rs. 5,800) into two smaller claims (Rs. 3,000 + Rs. 2,800) submitted on the same day to evade the Rs. 5,000 threshold.
- **Decision:** Track cumulative claims per `(club, category, date)` tuple in a dictionary.
- **Rationale:** Enables instant detection of split claims on the same day without requiring an external database.

---

### Decision 5: Fail-Safe Offline Fallback Mechanism
- **Problem:** What if the student runs the program without internet, with a rate-limited API key, or without an API key?
- **Decision:** Built-in deterministic regex fallback in `llm_client.py` that mirrors the 5-role prompt extraction logic.
- **Rationale:** The application never crashes due to external API errors, providing seamless local testing and evaluation.
