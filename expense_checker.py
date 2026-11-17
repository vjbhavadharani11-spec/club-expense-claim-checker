"""
expense_checker.py - Complete Club Expense Claim Checker Program.
CIT AI-Native Engineering Capstone Project: Assessment 5

This program reads claims.csv and budgets.csv, calls an LLM to extract claim facts,
independently verifies all facts using deterministic Python rules, enforces budget limits,
and writes out the required CSV and summary reports.
"""

import os
import sys
import csv
import json
import re

# Add project directory to search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_client import call_llm

# Allowed categories mandated by the specification
ALLOWED_CATEGORIES = ["printing", "food", "travel", "prizes", "equipment", "costumes", "other"]

def load_budgets(filepath: str) -> dict:
    """
    Reads budgets.csv and returns a dictionary of category limits.
    Example: {"printing": 2000, "food": 4000, "equipment": 10000, ...}
    """
    budgets = {}
    if not os.path.exists(filepath):
        return budgets
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"].strip().lower()
            try:
                budgets[cat] = int(row["limit_per_club"].strip())
            except ValueError:
                budgets[cat] = 0
    return budgets

def load_claims(filepath: str) -> list:
    """
    Reads claims.csv and returns a list of claim dictionaries.
    Each item contains: id, club, date, note.
    """
    claims = []
    if not os.path.exists(filepath):
        return claims
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claims.append({
                "id": row["id"].strip(),
                "club": row["club"].strip(),
                "date": row["date"].strip(),
                "note": row["note"].strip()
            })
    return claims

def numbers_in(note: str) -> list:
    """
    Extracts all integer numbers from the note, correctly handling commas (e.g. '1,250' -> 1250).
    Ignores calendar years like 2026 when part of a hyphenated or slashed date.
    """
    # Exclude date patterns like 2026-10-01
    matches = re.findall(r'(?<!\d-)(?<!\d/)\b(\d{1,3}(?:,\d{3})+|\d+)\b', note)
    results = []
    for m in matches:
        clean_num = int(m.replace(",", ""))
        # Filter out 2026 if it looks like the current event year
        if clean_num != 2026:
            results.append(clean_num)
    return results

def is_valid(llm_data: dict) -> bool:
    """
    Validates that the LLM response is a dictionary matching the required schema.
    Fields required:
    - amount: int or None
    - category: in ALLOWED_CATEGORIES
    - bill: bool
    - summary: str with 10 words or fewer
    """
    if not isinstance(llm_data, dict):
        return False
    
    # Check fields presence
    for req in ["amount", "category", "bill", "summary"]:
        if req not in llm_data:
            return False
            
    # Check types
    if llm_data["amount"] is not None and not isinstance(llm_data["amount"], int):
        return False
    if llm_data["category"] not in ALLOWED_CATEGORIES:
        return False
    if not isinstance(llm_data["bill"], bool):
        return False
    if not isinstance(llm_data["summary"], str):
        return False
    if len(llm_data["summary"].split()) > 10:
        return False
        
    return True

def check_facts(llm_data: dict, note: str) -> bool:
    """
    Python independently verifies the LLM output against the raw claim note.
    Rule 1: If amount is present, it MUST match one of the numbers written in the note.
    Rule 2: If bill is True, note MUST contain bill keywords and NO negative qualifiers.
    """
    note_nums = numbers_in(note)
    llm_amount = llm_data.get("amount")

    # If LLM claims an amount, verify it exists in the note
    if llm_amount is not None:
        if llm_amount not in note_nums:
            return False

    # Check bill status factuality
    note_lower = note.lower()
    has_bill_word = any(w in note_lower for w in ["bill", "receipt", "invoice", "ticket"])
    has_negative = any(neg in note_lower for neg in ["no bill", "bill lost", "lost", "without bill", "later", "coming later"])

    if llm_data.get("bill") is True:
        if not has_bill_word or has_negative:
            return False
            
    return True

def classify(llm_data: dict, note: str) -> dict:
    """
    Takes LLM output, validates schema and fact checks it.
    If invalid or facts fail, creates a safe sanitized version.
    """
    if not is_valid(llm_data) or not check_facts(llm_data, note):
        return {
            "amount": None,
            "category": "other",
            "bill": False,
            "summary": "Verification failed"
        }
    return llm_data

def decide(claim: dict, verified_data: dict, budgets: dict, running_totals: dict, daily_club_spending: dict) -> tuple:
    """
    Applies the college payment decision rules in strict priority order:
    1. needs_more_info: no amount.
    2. needs_bill: no bill.
    3. needs_approval: amount > 5000, or same club + category + date total > 5000 (split claim).
    4. over_budget: spending in that category would exceed budget limit.
    5. ok_to_pay: meets all rules.
    
    Returns (status, reason)
    """
    amount = verified_data.get("amount")
    category = verified_data.get("category", "other")
    bill = verified_data.get("bill", False)
    club = claim["club"]
    date = claim["date"]

    # Rule 1: No amount
    if amount is None or amount <= 0:
        return "needs_more_info", "Missing or unverified amount"

    # Rule 2: No bill
    if not bill:
        return "needs_bill", "No bill or receipt attached"

    # Rule 3: Above Rs. 5,000 or split claim on same date
    split_key = (club, category, date)
    projected_daily = daily_club_spending.get(split_key, 0) + amount
    if amount > 5000:
        return "needs_approval", f"Claim amount Rs. {amount:,} exceeds single-claim threshold of Rs. 5,000"
    if projected_daily > 5000:
        return "needs_approval", f"Combined claims for {club} in {category} on {date} total Rs. {projected_daily:,} (exceeds Rs. 5,000 split threshold)"

    # Rule 4: Over budget check
    budget_key = (club, category)
    limit = budgets.get(category, 0)
    current_spend = running_totals.get(budget_key, 0)
    if current_spend + amount > limit:
        return "over_budget", f"Claim Rs. {amount:,} pushes total ({current_spend + amount:,}) over category budget of Rs. {limit:,}"

    # Rule 5: OK to pay
    return "ok_to_pay", "Claim verified and within budget"

def process_all_claims(claims_path: str, budgets_path: str) -> tuple:
    """
    Processes all claims sequentially, updating running totals ONLY for ok_to_pay claims.
    Returns (results, running_totals, budgets, status_counts)
    """
    budgets = load_budgets(budgets_path)
    claims = load_claims(claims_path)

    running_totals = {}       # Key: (club, category) -> total spent
    daily_club_spending = {}  # Key: (club, category, date) -> total claimed on that day
    
    results = []
    status_counts = {
        "ok_to_pay": 0,
        "needs_bill": 0,
        "needs_approval": 0,
        "over_budget": 0,
        "needs_more_info": 0
    }

    for claim in claims:
        # Step 1: Call LLM
        raw_llm = call_llm(claim["note"])
        
        # Step 2: Classify and verify facts
        verified_data = classify(raw_llm, claim["note"])
        
        # Step 3: Apply decision rules in order
        status, reason = decide(claim, verified_data, budgets, running_totals, daily_club_spending)
        
        # Step 4: Track daily spending for split claim detection
        amount = verified_data.get("amount") or 0
        split_key = (claim["club"], verified_data.get("category", "other"), claim["date"])
        daily_club_spending[split_key] = daily_club_spending.get(split_key, 0) + amount

        # Step 5: ONLY add to budget running totals if ok_to_pay
        if status == "ok_to_pay":
            budget_key = (claim["club"], verified_data["category"])
            running_totals[budget_key] = running_totals.get(budget_key, 0) + amount

        status_counts[status] = status_counts.get(status, 0) + 1

        results.append({
            "id": claim["id"],
            "club": claim["club"],
            "date": claim["date"],
            "note": claim["note"],
            "amount": verified_data.get("amount"),
            "category": verified_data.get("category"),
            "bill": verified_data.get("bill"),
            "summary": verified_data.get("summary"),
            "status": status,
            "reason": reason
        })

    return results, running_totals, budgets, status_counts

def write_reports(results: list, running_totals: dict, budgets: dict, status_counts: dict, output_dir: str):
    """
    Writes out the four required output files:
    1. payable.csv - Only ok_to_pay claims
    2. review.csv - Flagged claims with reasons
    3. results.csv - All claims and statuses
    4. summary.txt - Status counts and budget analysis
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. payable.csv
    payable_path = os.path.join(output_dir, "payable.csv")
    with open(payable_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "club", "date", "category", "amount", "summary"])
        for r in results:
            if r["status"] == "ok_to_pay":
                writer.writerow([r["id"], r["club"], r["date"], r["category"], r["amount"], r["summary"]])

    # 2. review.csv
    review_path = os.path.join(output_dir, "review.csv")
    with open(review_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "club", "date", "category", "amount", "status", "reason", "note"])
        for r in results:
            if r["status"] != "ok_to_pay":
                writer.writerow([
                    r["id"], r["club"], r["date"], r["category"], 
                    r["amount"] if r["amount"] is not None else "",
                    r["status"], r["reason"], r["note"]
                ])

    # 3. results.csv
    results_path = os.path.join(output_dir, "results.csv")
    with open(results_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id", "club", "date", "category", "amount", "bill", "status", "reason", "note"])
        for r in results:
            writer.writerow([
                r["id"], r["club"], r["date"], r["category"],
                r["amount"] if r["amount"] is not None else "",
                r["bill"], r["status"], r["reason"], r["note"]
            ])

    # 4. summary.txt
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("CLUB EXPENSE CLAIM CHECKER - SUMMARY AUDIT REPORT\n")
        f.write("=" * 70 + "\n\n")

        f.write("1. CLAIM STATUS COUNTS\n")
        f.write("-" * 40 + "\n")
        total_claims = len(results)
        for st in ["ok_to_pay", "needs_bill", "needs_approval", "over_budget", "needs_more_info"]:
            cnt = status_counts.get(st, 0)
            f.write(f"  {st:<18} : {cnt:>3} claims\n")
        f.write("-" * 40 + "\n")
        f.write(f"  TOTAL CLAIMS       : {total_claims:>3} claims\n\n")

        f.write("2. CLUB BUDGET SPENDING BREAKDOWN (Only ok_to_pay claims counted)\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Club':<22} | {'Category':<12} | {'Spent (Rs.)':<12} | {'Limit (Rs.)':<12} | {'Remaining'}\n")
        f.write("-" * 70 + "\n")

        # Sort by club name then category
        sorted_keys = sorted(running_totals.keys())
        total_payable_amount = 0
        for (club, cat) in sorted_keys:
            spent = running_totals[(club, cat)]
            total_payable_amount += spent
            limit = budgets.get(cat, 0)
            remaining = limit - spent
            f.write(f"{club:<22} | {cat:<12} | Rs. {spent:>8,} | Rs. {limit:>8,} | Rs. {remaining:>8,}\n")
            
        f.write("-" * 70 + "\n")
        f.write(f"TOTAL AMOUNT APPROVED FOR PAYMENT: Rs. {total_payable_amount:,}\n")
        f.write("=" * 70 + "\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    claims_file = os.path.join(base_dir, "claims.csv")
    budgets_file = os.path.join(base_dir, "budgets.csv")
    
    print("Starting Club Expense Claim Checker...")
    results, running_totals, budgets, status_counts = process_all_claims(claims_file, budgets_file)
    
    write_reports(results, running_totals, budgets, status_counts, base_dir)
    print(f"Audit processing complete! {len(results)} claims processed.")
    print("Generated files:")
    print(" - payable.csv")
    print(" - review.csv")
    print(" - results.csv")
    print(" - summary.txt")

if __name__ == "__main__":
    main()
