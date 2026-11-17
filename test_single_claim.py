"""
test_single_claim.py - Stage 2 checkpoint test.
Tests extraction on a single claim using the 5-role system prompt.
"""

import os
import sys
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_client import call_llm

def test_checkpoint_item():
    claim_note = "Paid Rs. 1,250 for banner printing at Copy Point. Bill attached"
    print("=" * 60)
    print("CHECKPOINT 2 TEST: ONE ITEM END-TO-END")
    print("=" * 60)
    print(f"Input Claim Note: \"{claim_note}\"")
    print("-" * 60)
    
    result = call_llm(claim_note)
    
    print("Raw LLM / Extractor Response:")
    print(json.dumps(result, indent=2))
    print("-" * 60)
    
    # Validation checks
    assert isinstance(result, dict), "Result must be a JSON dictionary"
    assert "amount" in result and result["amount"] == 1250, "Amount must be 1250"
    assert "category" in result and result["category"] == "printing", "Category must be printing"
    assert "bill" in result and result["bill"] is True, "Bill must be True"
    assert "summary" in result and len(result["summary"].split()) <= 10, "Summary must be <= 10 words"
    
    print(">>> SUCCESS: Checkpoint 2 passed! LLM extraction is valid and matches schema.")
    print("=" * 60)

if __name__ == "__main__":
    test_checkpoint_item()
