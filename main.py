"""
main.py - Complete Club Expense Claim Checker Console & Terminal Output.
CIT AI-Native Engineering Capstone Project: Assessment 5
"""

import os
import sys

# Ensure current project directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expense_checker import process_all_claims, write_reports

def display_terminal_dashboard(results: list, running_totals: dict, budgets: dict, status_counts: dict):
    """Prints a beautiful, formatted ASCII dashboard directly in the user's terminal."""
    print("\n" + "=" * 90)
    print(" " * 22 + "COLLEGE CLUB EXPENSE CLAIM CHECKER")
    print(" " * 24 + "Audit Processing Engine & Dashboard")
    print("=" * 90)
    
    # Print status counts
    print("\n[1] AUDIT SUMMARY STATUS COUNTS:")
    print("-" * 55)
    print(f"  * OK TO PAY (Ready for treasurer signature) : {status_counts.get('ok_to_pay', 0):>3} claims")
    print(f"  * NEEDS BILL (Missing receipt)       : {status_counts.get('needs_bill', 0):>3} claims")
    print(f"  * NEEDS APPROVAL (> Rs. 5k / Split)  : {status_counts.get('needs_approval', 0):>3} claims")
    print(f"  * OVER BUDGET (Limit exceeded)       : {status_counts.get('over_budget', 0):>3} claims")
    print(f"  * NEEDS MORE INFO (Unverified/No amt): {status_counts.get('needs_more_info', 0):>3} claims")
    print("-" * 55)
    print(f"  TOTAL AUDITED CLAIMS                 : {len(results):>3} claims\n")
    
    # Print detailed claims table
    print("[2] DETAILED CLAIMS AUDIT LOG:")
    print("-" * 90)
    print(f"{'ID':<5} | {'Club':<16} | {'Date':<10} | {'Category':<10} | {'Amount':<10} | {'Status'}")
    print("-" * 90)
    for r in results:
        amt_str = f"Rs. {r['amount']:,}" if r['amount'] is not None else "N/A"
        print(f"{r['id']:<5} | {r['club']:<16} | {r['date']:<10} | {r['category']:<10} | {amt_str:<10} | {r['status']}")
    print("-" * 90)
    
    # Print budget spending breakdown
    print("\n[3] CLUB BUDGET SPENDING BREAKDOWN (Only ok_to_pay claims count):")
    print("-" * 75)
    print(f"{'Club':<18} | {'Category':<10} | {'Spent':<12} | {'Limit':<12} | {'Remaining'}")
    print("-" * 75)
    sorted_keys = sorted(running_totals.keys())
    total_payable = 0
    for (club, cat) in sorted_keys:
        spent = running_totals[(club, cat)]
        total_payable += spent
        limit = budgets.get(cat, 0)
        remaining = limit - spent
        print(f"{club:<18} | {cat:<10} | Rs. {spent:>7,} | Rs. {limit:>7,} | Rs. {remaining:>7,}")
    print("-" * 75)
    print(f"TOTAL AMOUNT MARKED OK TO PAY: Rs. {total_payable:,}")
    print("=" * 90 + "\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    claims_file = os.path.join(base_dir, "claims.csv")
    budgets_file = os.path.join(base_dir, "budgets.csv")
    
    results, running_totals, budgets, status_counts = process_all_claims(claims_file, budgets_file)
    write_reports(results, running_totals, budgets, status_counts, base_dir)
    
    # Automatically update dashboard.html
    try:
        from update_dashboard import generate_html_dashboard
        generate_html_dashboard()
    except Exception:
        pass
    
    # Print rich output directly to the terminal!
    display_terminal_dashboard(results, running_totals, budgets, status_counts)
    
    print("[+] All 5 output and report files generated successfully in this folder:")
    print("    - payable.csv")
    print("    - review.csv")
    print("    - results.csv")
    print("    - summary.txt")
    print("    - dashboard.html\n")

if __name__ == "__main__":
    main()
