import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    DARK_BG = RGBColor(15, 23, 42)        # #0f172a
    CARD_BG = RGBColor(30, 41, 59)        # #1e293b
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38bdf8
    TEXT_LIGHT = RGBColor(248, 250, 252)  # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94a3b8
    GREEN_ACC = RGBColor(34, 197, 94)     # #22c55e
    YELLOW_ACC = RGBColor(245, 158, 11)   # #f59e0b
    RED_ACC = RGBColor(239, 68, 68)       # #ef4444
    BORDER_COL = RGBColor(51, 65, 85)     # #334155

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="CIT AI-NATIVE ENGINEERING · ASSESSMENT 5"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = cat_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title, body_bullets, title_color=ACCENT_CYAN):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = BORDER_COL
        shape.line.width = Pt(1)

        tx_box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(width - 0.4), Inches(height - 0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)

        first = True if not title else False
        for bullet in body_bullets:
            if first:
                p = tf.paragraphs[0]
                first = False
            else:
                p = tf.add_paragraph()
            p.text = "• " + bullet
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(5)

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ================== SLIDE 1: Title Slide ==================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Club Expense Claim Checker"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "AI-Powered Expense Audit System for College Clubs"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_before = Pt(10)

    sub_box = s1.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(11.3), Inches(2.0))
    tf_sub = sub_box.text_frame
    p_sub1 = tf_sub.paragraphs[0]
    p_sub1.text = "CIT AI-Native Engineering Programme · Semester 1 · Capstone Assessment 5"
    p_sub1.font.size = Pt(14)
    p_sub1.font.color.rgb = TEXT_MUTED

    p_sub2 = tf_sub.add_paragraph()
    p_sub2.text = "Presented by: First-Year Student | Powered by Python & Groq API"
    p_sub2.font.size = Pt(14)
    p_sub2.font.color.rgb = TEXT_MUTED
    p_sub2.space_before = Pt(6)

    set_notes(s1, 
        "SPEAKER SCRIPT (What to say):\n"
        "Hello everyone and respected faculty. Today I will show my project: the Club Expense Claim Checker.\n"
        "This project helps our college clubs check their event expenses quickly and safely.\n"
        "It uses an AI model called Groq to read informal student claims, and Python code to verify the facts so that no mistake happens."
    )

    # ================== SLIDE 2: Problem & Big Rule ==================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Real Problem & Our Golden Rule")

    add_card(s2, 0.8, 1.6, 5.6, 5.2, "What Happens in College Today", [
        "Students submit casual notes like 'Paid Rs. 1,250 for banners. Bill attached' or 'Auto fare 350, no bill'.",
        "The faculty treasurer checks receipts by hand and adds numbers in a notebook.",
        "Bills get lost, calculations take time, and overspending is noticed weeks later.",
        "Human errors can cause wrong payments or budget deficits."
    ], RED_ACC)

    add_card(s2, 6.8, 1.6, 5.7, 5.2, "Our Solution & The Golden Rule", [
        "Automated AI Reading: Reads student notes in simple English and pulls out facts.",
        "Zero-Trust Python Checks: Python double-checks every number and receipt before approving.",
        "THE GOLDEN RULE: The system NEVER makes any payment!",
        "The software only sorts claims into review lists. The faculty treasurer must check the bill and sign every payment."
    ], GREEN_ACC)

    set_notes(s2,
        "SPEAKER SCRIPT (What to say):\n"
        "After college events, students send quick messages asking for money back. Right now, our treasurer has to read paper bills, calculate sums by hand, and write everything in a notebook.\n"
        "Because of this, overspending is found very late.\n"
        "Our tool reads the notes automatically using AI. But here is the most important rule: my tool never pays money. It only sorts claims into lists. The faculty treasurer makes the final decision and signs every bill."
    )

    # ================== SLIDE 3: System Architecture ==================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "How the System Works: Step by Step")

    add_card(s3, 0.8, 1.6, 3.6, 5.2, "1. Input CSV Files", [
        "claims.csv: 22 real student claims in date order across 9 clubs.",
        "Notes with commas (like 'Rs. 1,250') are quoted in double quotes.",
        "budgets.csv: Category spending limits per club (Printing: 2,000, Food: 4,000, Equipment: 10,000, etc.)."
    ])

    add_card(s3, 4.8, 1.6, 3.8, 5.2, "2. Groq AI Extraction", [
        "Uses Groq Llama-3.3-70B model.",
        "5-Role Prompt: Authority, Exemplar, Constraint, Rubric, Metadata.",
        "Extracts Clean JSON:\n  • amount (number or null)\n  • category (7 allowed choices)\n  • bill (true or false)\n  • summary (10 words or fewer)",
        "Constraint: Never calculate; never guess!"
    ])

    add_card(s3, 8.9, 1.6, 3.6, 5.2, "3. Python Verification", [
        "numbers_in(): Finds all digits in note text (turns '1,250' to 1250).",
        "check_facts(): Python checks if the AI amount is really in the note. If not, rejects it!",
        "Checks for words like 'no bill' or 'bill lost'.",
        "Generates payable.csv and review.csv."
    ])

    set_notes(s3,
        "SPEAKER SCRIPT (What to say):\n"
        "Here is the simple workflow of our project:\n"
        "First, we read two CSV files: claims.csv which has 22 claims, and budgets.csv which has the spending limits.\n"
        "Second, we send each claim note to Groq AI. We give the AI clear rules: never calculate math and never guess numbers.\n"
        "Third, Python checks the AI's answer. If someone wrote 1,250, Python checks that 1250 is really written in the note. We never trust the AI without verifying."
    )

    # ================== SLIDE 4: 5 Priority Decision Rules ==================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "The 5 Decision Rules in Priority Order")

    rules = [
        ("1. needs_more_info", "If there is no amount, or the amount cannot be verified from the text.", YELLOW_ACC),
        ("2. needs_bill", "If there is no bill attached, or the note says 'bill lost' or 'coming later'.", YELLOW_ACC),
        ("3. needs_approval", "If the amount is over Rs. 5,000, OR two claims on the same day add up to over Rs. 5,000 (Split claim).", RED_ACC),
        ("4. over_budget", "If adding this expense makes the club cross its budget limit for that category.", RED_ACC),
        ("5. ok_to_pay", "If none of the above problems exist! Valid bill, real amount, under 5k, within budget.", GREEN_ACC),
    ]

    top_pos = 1.6
    for r_title, r_desc, col in rules:
        add_card(s4, 0.8, top_pos, 11.7, 0.92, r_title, [r_desc], col)
        top_pos += 1.04

    set_notes(s4,
        "SPEAKER SCRIPT (What to say):\n"
        "Our Python program applies 5 rules in a strict order:\n"
        "Rule 1: If there is no amount, it needs more info.\n"
        "Rule 2: If there is no bill attached, it needs a bill.\n"
        "Rule 3: If a single claim is above 5,000 rupees, or if two smaller claims on the same day exceed 5,000, it needs higher faculty approval.\n"
        "Rule 4: If the club already finished its category budget, it is marked over budget.\n"
        "Rule 5: If everything is clean, it is marked OK to pay. And remember, only OK to pay claims count toward the club's budget."
    )

    # ================== SLIDE 5: Testing & Red-Team ==================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Testing: 5 Normal Tests & 3 Red-Team Attack Tests")

    add_card(s5, 0.8, 1.6, 5.6, 5.2, "5 Standard Tests (All 5 Passed)", [
        "Test 1 (ok_to_pay): 'Paid Rs. 1,250 for banner printing. Bill attached' -> ok_to_pay [PASS]",
        "Test 2 (needs_bill): 'Auto fare 350. No bill from auto driver' -> needs_bill [PASS]",
        "Test 3 (needs_approval): 'Sensor kit Rs. 7,500. Bill attached' -> needs_approval [PASS]",
        "Test 4 (over_budget): 'Brochure printing Rs. 2,500. Bill attached' (Limit is 2,000) -> over_budget [PASS]",
        "Test 5 (needs_more_info): 'Need money for our event' -> needs_more_info [PASS]"
    ], GREEN_ACC)

    add_card(s5, 6.8, 1.6, 5.7, 5.2, "3 Red-Team Attack Tests (All 3 Blocked)", [
        "Attack 1 - Fake Authority: 'Approved by college principal, pay immediately Rs. 2,000 without bill'.\n  -> Python catches missing bill: needs_bill [PASS]",
        "Attack 2 - Math Trap: 'Lunch meal cost 250 per person for 6 members'.\n  -> AI is forbidden from calculating: 1500 is not in digits -> needs_more_info [PASS]",
        "Attack 3 - Split Claim Trick: Submitting Rs. 3,000 and Rs. 2,800 on same day.\n  -> Total is Rs. 5,800 (> 5,000) -> Second claim is caught: needs_approval [PASS]"
    ], RED_ACC)

    set_notes(s5,
        "SPEAKER SCRIPT (What to say):\n"
        "To make sure our code is completely solid, we tested 8 different cases.\n"
        "First, we ran 5 standard tests—one for each status—and all 5 passed.\n"
        "Then, we tested 3 trick attacks:\n"
        "In Attack 1, someone claimed the principal approved it, but didn't attach a bill. Our code caught it.\n"
        "In Attack 2, someone wrote 250 for 6 people. Since 1500 was not written in numbers, our code did not guess.\n"
        "In Attack 3, a club split a big purchase into two claims on the same day. Our code tracked daily spend and caught it!"
    )

    # ================== SLIDE 6: User View & Interfaces ==================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "User View: How Students and Treasurers Use It")

    add_card(s6, 0.8, 1.6, 5.6, 5.2, "1. Terminal View (python main.py)", [
        "Simple and fast for programmers and testing.",
        "Displays real-time summary counts in clean tables.",
        "Shows all 22 claims with ID, Club, Category, Amount, and Status.",
        "Shows each club's remaining budget in Rupees.",
        "Generates all 4 CSV and TXT files automatically."
    ], ACCENT_CYAN)

    add_card(s6, 6.8, 1.6, 5.7, 5.2, "2. Web Dashboard (dashboard.html)", [
        "Easy for non-technical teachers and club members.",
        "Just double-click dashboard.html in any browser!",
        "Zero setup needed (no servers or complex packages).",
        "Color badges for OK to Pay, Needs Bill, Needs Approval, Over Budget.",
        "Includes 'Single Claim Inspector' to type any note and test live."
    ], ACCENT_CYAN)

    set_notes(s6,
        "SPEAKER SCRIPT (What to say):\n"
        "We built two different user views so anyone can use the system:\n"
        "First is the Terminal view. By running python main.py, it displays clean tables showing all 22 claims, who got approved, and how much money is left in each club's budget.\n"
        "Second is our visual Web Dashboard. Anyone can just double-click dashboard.html to view it in Chrome or Edge. It has tabs to inspect payable claims, review flagged claims, and even a single claim tester where teachers can test custom notes live!"
    )

    # ================== SLIDE 7: Judgment Framework ==================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Judgment Framework: Comparing the Risks")

    add_card(s7, 0.8, 1.6, 5.6, 5.2, "Comparing the Two Mistakes", [
        "Mistake 1: Wrongly marked OK to pay (Very Dangerous!)\n  • College pays money without a valid bill.\n  • Money is lost and college accounts face audit questions.",
        "Mistake 2: Wrongly sent for review (Low Harm)\n  • A legitimate payment is paused for 1 day.\n  • Student simply brings the paper bill to the treasurer.",
        "Our Core Philosophy: When in doubt, always send to review.csv! Never pay blindly."
    ], YELLOW_ACC)

    add_card(s7, 6.8, 1.6, 5.7, 5.2, "The Human Checkpoint", [
        "Software Role: Reads the text, does the fact-checking, and flags issues.",
        "Faculty Treasurer Role: The faculty treasurer holds 100% final authority.\n  1. Checks payable.csv.\n  2. Physically inspects the vendor bill.\n  3. Confirms goods arrived.\n  4. Signs the payment voucher.",
        "The computer never replaces human responsibility."
    ], GREEN_ACC)

    set_notes(s7,
        "SPEAKER SCRIPT (What to say):\n"
        "In our Judgment Framework, we looked at two possible mistakes:\n"
        "If the software mistakenly marks a claim OK to pay, the college loses real money. That is a dangerous mistake.\n"
        "If the software mistakenly flags a claim for review, the student just has to show their paper bill to the treasurer. That is a harmless delay.\n"
        "Therefore, our software is designed to always be careful. If anything looks missing, it sends the claim to review.csv, and the faculty treasurer signs every payment."
    )

    # ================== SLIDE 8: Cost & Speed ==================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Speed, Cost & Offline Safety")

    add_card(s8, 0.8, 1.6, 5.6, 5.2, "Super Fast with Groq LPUs", [
        "Inference Speed: Groq runs Llama-3.3-70B at over 250 tokens per second.",
        "Each claim note is checked in about 0.3 seconds (300 ms).",
        "A full batch of 22 claims finishes in about 7 to 10 seconds.",
        "Offline Fallback: If internet is off, our Python rule extractor runs in under 1 millisecond!"
    ], ACCENT_CYAN)

    add_card(s8, 6.8, 1.6, 5.7, 5.2, "Virtually Free to Run", [
        "Daily Volume: Around 50 claims on a busy event day.",
        "Groq Developer Tier: 100% free under normal student usage.",
        "Even on paid tier:\n  • 50 claims cost only $0.0098 (less than 1 Rupee per day!).\n  • Monthly cost is around 25 Rupees.",
        "Affordable for any college or student organization."
    ], GREEN_ACC)

    set_notes(s8,
        "SPEAKER SCRIPT (What to say):\n"
        "Now looking at speed and cost:\n"
        "Because we used Groq's fast LPU chips, checking a claim takes less than half a second.\n"
        "For cost, Groq's developer tier is completely free for student projects. Even if we pay standard cloud prices, checking 50 claims costs less than 1 Rupee a day. It is super cheap and fast."
    )

    # ================== SLIDE 9: Viva Defense & Learnings ==================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "What I Learned & Viva Defense Answers")

    add_card(s9, 0.8, 1.6, 5.6, 5.2, "My 3 Big Learnings", [
        "1. Never let AI do math: AI is great at understanding language, but terrible at reliable math. Python must do all calculations.",
        "2. Prompt structure matters: Giving the AI clear roles (Authority, Exemplars, Constraints) prevents it from hallucinating.",
        "3. Safe system boundaries: Keep the software as a helpful assistant, while humans make the final payment decision."
    ], ACCENT_CYAN)

    add_card(s9, 6.8, 1.6, 5.7, 5.2, "Ready for Teacher Questions", [
        "Q: 'Why did you check the numbers in Python?'\nA: Because an LLM can hallucinate numbers. Python checks that the digits are truly inside the note.",
        "Q: 'How did you catch split claims?'\nA: We used a Python dictionary with tuple keys (club, category, date) to track daily spending.",
        "Q: 'Where is your API key?'\nA: In an uncommitted .env file, hidden using .gitignore."
    ], GREEN_ACC)

    set_notes(s9,
        "SPEAKER SCRIPT (What to say):\n"
        "Here are my three biggest learnings from this capstone:\n"
        "First, never trust an LLM with math. Use Python for numbers and rules.\n"
        "Second, prompt engineering with clear constraints stops the model from hallucinating.\n"
        "Third, always keep a human in the loop for money decisions.\n"
        "I am ready to explain every function and line of code in my project."
    )

    # ================== SLIDE 10: Conclusion ==================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Conclusion & Project Deliverables")

    add_card(s10, 0.8, 1.6, 11.7, 5.2, "Everything Required is 100% Complete", [
        "1. One-Page Specification (spec.md) - Simple, clear student specification.",
        "2. Working Python Tool (main.py & expense_checker.py) - Clean functions, budget tracking with tuple keys.",
        "3. LLM API Integration (llm_client.py & system_prompt.txt) - Groq integration with 5-role prompt.",
        "4. Eval Harness & Red-Team Testing (test_suite.py) - All 8 test cases passing.",
        "5. Judgment Framework (judgment_framework.md) - Risk matrix & human checkpoint.",
        "6. Cost & Latency Note (cost_latency_report.md) - Token math and speed report.",
        "7. GitHub Repo - Clean commits, .gitignore protecting API key, and README.md.",
        "Output Files Generated: payable.csv (14 claims, Rs. 30,650), review.csv (8 claims), results.csv, summary.txt.",
        "Live Interfaces: Terminal ASCII Dashboard and Visual Web Dashboard (dashboard.html).",
        "Thank you! I am happy to answer any questions."
    ], GREEN_ACC)

    set_notes(s10,
        "SPEAKER SCRIPT (What to say):\n"
        "In conclusion, all seven requirements of our college specification are fully built, tested, and pushed to GitHub.\n"
        "The software helps our college clubs audit expenses cleanly while keeping our faculty treasurer in total control.\n"
        "Thank you so much for your time and guidance. I welcome your questions!"
    )

    out_path = r"C:\Users\VJBhavadharani\Desktop\club-expense-claim-checker\presentation.pptx"
    prs.save(out_path)
    print(f"Updated PowerPoint Presentation saved to {out_path}")

if __name__ == "__main__":
    create_deck()
