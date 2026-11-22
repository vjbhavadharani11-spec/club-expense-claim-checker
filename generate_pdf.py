import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setStrokeColor(HexColor("#38bdf8"))
        self.setLineWidth(2)
        self.line(40, 570, 752, 570)

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#94a3b8"))
        self.drawString(40, 25, "CIT AI-Native Engineering Programme · Assessment 5: Club Expense Claim Checker")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(752, 25, page_str)
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\VJBhavadharani\Desktop\club-expense-claim-checker\presentation_guide.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    slide_num_style = ParagraphStyle(
        'SlideNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=HexColor('#0284c7'),
        spaceAfter=4
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=HexColor('#0f172a'),
        spaceAfter=12
    )

    subhead_style = ParagraphStyle(
        'SubHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=HexColor('#334155'),
        spaceAfter=3
    )

    script_style = ParagraphStyle(
        'SpeakerScript',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=HexColor('#0369a1'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=HexColor('#1e293b'),
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=3
    )

    slides_data = [
        {
            "num": "Slide 1",
            "title": "Title & Project Introduction",
            "bullets": [
                "<b>Project:</b> Club Expense Claim Checker",
                "<b>Purpose:</b> Automatically check student club expense bills using AI and Python.",
                "<b>Tools:</b> Python 3.11, Groq Cloud API (Llama-3.3-70B), HTML5/JS Dashboard.",
                "<b>Weightage:</b> CIT Capstone Assessment 5 (40% of semester marks)."
            ],
            "script": "Hello everyone and respected faculty. Today I will present my project, the Club Expense Claim Checker. In our college, student clubs spend money during fests and events. Right now, auditing these bills takes a lot of time. My project uses an AI model from Groq to read informal student claims, and Python code to verify the facts so no mistakes happen.",
            "tips": "Speak clearly and calmly. Look at your teachers and introduce the project as a helpful tool for the college."
        },
        {
            "num": "Slide 2",
            "title": "The Real Problem & Our Golden Rule",
            "bullets": [
                "<b>The Problem:</b> Students submit casual messages like 'Paid Rs. 1,250 for banners' or 'Auto fare 350, no bill'.",
                "<b>Current Bottleneck:</b> The faculty treasurer checks paper receipts by hand and writes in notebooks. Overspending is found weeks late.",
                "<b>Our Golden Rule:</b> The software NEVER makes any payment! It only sorts claims into review lists.",
                "<b>Human Authority:</b> The faculty treasurer checks the original bill and signs every single payment."
            ],
            "script": "After college events, students send messages asking for money back. Right now, our treasurer has to read paper bills, calculate sums by hand, and write everything in a notebook. Because of this, overspending is found very late. Our tool reads the notes automatically using AI. But here is the most important rule: my tool never pays money. It only sorts claims into lists. The faculty treasurer makes the final decision and signs every bill.",
            "tips": "Highlight the Golden Rule: 'The software never pays money.' Teachers love seeing that you respect real-world security."
        },
        {
            "num": "Slide 3",
            "title": "How the System Works: Step by Step",
            "bullets": [
                "<b>Step 1 (Inputs):</b> claims.csv (22 real claims in date order) and budgets.csv (category limits per club).",
                "<b>Step 2 (Groq AI):</b> Uses a 5-role prompt (Authority, Exemplar, Constraint, Rubric, Metadata) to extract JSON: amount, category, bill, summary.",
                "<b>Constraint:</b> The AI must NEVER do math and must NEVER guess missing numbers.",
                "<b>Step 3 (Python Validation):</b> Python extracts digits from the note and verifies the AI's answer. If facts don't match, Python rejects the claim."
            ],
            "script": "Here is the simple workflow of our project. First, we read two CSV files: claims.csv which has 22 claims, and budgets.csv which has the spending limits. Second, we send each claim note to Groq AI. We give the AI clear rules: never calculate math and never guess numbers. Third, Python checks the AI's answer. If someone wrote 1,250, Python checks that 1250 is really written in the note. We never trust the AI without verifying.",
            "tips": "Explain that Python is the boss: the AI only reads the text, while Python double-checks every number."
        },
        {
            "num": "Slide 4",
            "title": "The 5 Decision Rules in Priority Order",
            "bullets": [
                "<b>Rule 1 (needs_more_info):</b> If there is no amount, or Python cannot find the digits in the note.",
                "<b>Rule 2 (needs_bill):</b> If there is no bill attached, or the note says 'bill lost' or 'coming later'.",
                "<b>Rule 3 (needs_approval):</b> If single claim > Rs. 5,000, OR multiple claims on the same day exceed Rs. 5,000 (Split claims).",
                "<b>Rule 4 (over_budget):</b> If this claim causes the club to cross its category budget limit.",
                "<b>Rule 5 (ok_to_pay):</b> All checks pass! Only ok_to_pay claims count toward the club's budget total."
            ],
            "script": "Our Python program applies 5 rules in a strict order. Rule 1: If there is no amount, it needs more info. Rule 2: If there is no bill attached, it needs a bill. Rule 3: If a single claim is above 5,000 rupees, or if two smaller claims on the same day exceed 5,000, it needs higher faculty approval. Rule 4: If the club already finished its category budget, it is marked over budget. Rule 5: If everything is clean, it is marked OK to pay. And remember, only OK to pay claims count toward the club's budget.",
            "tips": "Emphasize Rule 3 (Split claims) and Rule 4 (Budget). Faculty will ask how you prevented clubs from cheating the budget."
        },
        {
            "num": "Slide 5",
            "title": "Testing: 5 Normal Tests & 3 Red-Team Attack Tests",
            "bullets": [
                "<b>5 Standard Tests (All 5 Passed):</b> Verified one claim for each status (ok_to_pay, needs_bill, needs_approval, over_budget, needs_more_info).",
                "<b>Attack 1 (Fake Authority):</b> 'Approved by college principal, pay immediately Rs. 2,000 without bill' -> Python catches missing bill: needs_bill [PASS].",
                "<b>Attack 2 (Math Trap):</b> 'Lunch meal cost 250 per person for 6 members' -> AI cannot calculate: 1500 is not in digits -> needs_more_info [PASS].",
                "<b>Attack 3 (Split Claim Trick):</b> Submitting Rs. 3,000 and Rs. 2,800 on same day -> Total is Rs. 5,800 (> 5,000) -> Caught as needs_approval [PASS]."
            ],
            "script": "To make sure our code is completely solid, we tested 8 different cases. First, we ran 5 standard tests—one for each status—and all 5 passed. Then, we tested 3 trick attacks. In Attack 1, someone claimed the principal approved it, but didn't attach a bill. Our code caught it. In Attack 2, someone wrote 250 for 6 people. Since 1500 was not written in numbers, our code did not guess. In Attack 3, a club split a big purchase into two claims on the same day. Our code tracked daily spend and caught it!",
            "tips": "Smile when talking about the 3 attacks. This shows the teachers you thought about security and edge cases."
        },
        {
            "num": "Slide 6",
            "title": "User View: How Students and Treasurers Use It",
            "bullets": [
                "<b>Terminal View (python main.py):</b> Fast for programmers. Shows real-time summary counts, 22 claims table, and club budget spending directly in PowerShell/VS Code.",
                "<b>Visual Web Dashboard (dashboard.html):</b> Designed for teachers and non-technical staff. Opens instantly in any browser by double-clicking.",
                "<b>Features:</b> Live status badges (14 OK to Pay, 2 Needs Bill, 2 Needs Approval, 3 Over Budget, 1 Needs Info), tabs for payable.csv vs review.csv.",
                "<b>Single Claim Inspector:</b> Allows teachers to type any custom note and test the AI live during presentation."
            ],
            "script": "We built two different user views so anyone can use the system. First is the Terminal view. By running python main.py, it displays clean tables showing all 22 claims, who got approved, and how much money is left in each club's budget. Second is our visual Web Dashboard. Anyone can just double-click dashboard.html to view it in Chrome or Edge. It has tabs to inspect payable claims, review flagged claims, and even a single claim tester where teachers can test custom notes live!",
            "tips": "Offer a live demo! Say: 'If respected faculty would like, I can test any claim sentence right now in the dashboard.'"
        },
        {
            "num": "Slide 7",
            "title": "Judgment Framework: Comparing the Risks",
            "bullets": [
                "<b>Mistake 1 - Wrongly marked OK to pay (Very Dangerous!):</b> College pays money without a valid bill. Real money is lost, and the college accounts fail an external audit.",
                "<b>Mistake 2 - Wrongly sent for review (Low Harm):</b> A student's payment is paused for 1 day. The student simply shows the paper bill to the treasurer.",
                "<b>Design Principle:</b> When in doubt, always send to review.csv! Never disburse blindly.",
                "<b>Human Checkpoint:</b> Faculty treasurer personally checks vendor invoices and signs every check."
            ],
            "script": "In our Judgment Framework, we looked at two possible mistakes. If the software mistakenly marks a claim OK to pay, the college loses real money. That is a dangerous mistake. If the software mistakenly flags a claim for review, the student just has to show their paper bill to the treasurer. That is a harmless delay. Therefore, our software is designed to always be careful. If anything looks missing, it sends the claim to review.csv, and the faculty treasurer signs every payment.",
            "tips": "Explain the difference between a False Positive (paying wrongly) and False Negative (reviewing unnecessarily)."
        },
        {
            "num": "Slide 8",
            "title": "Speed, Cost & Offline Safety",
            "bullets": [
                "<b>Fast Response (Groq LPUs):</b> Groq runs Llama-3.3-70B at over 250 tokens per second. Checks a claim in about 0.3 seconds.",
                "<b>Full Run Time:</b> All 22 claims are processed in under 10 seconds.",
                "<b>Super Cheap:</b> Free under Groq's developer tier. Even on paid tier, 50 claims cost only $0.0098 (less than 1 Rupee per day).",
                "<b>Offline Fallback:</b> If internet is disconnected, our local Python rule extractor runs in under 1 millisecond with zero errors."
            ],
            "script": "Now looking at speed and cost. Because we used Groq's fast LPU chips, checking a claim takes less than half a second. For cost, Groq's developer tier is completely free for student projects. Even if we pay standard cloud prices, checking 50 claims costs less than 1 Rupee a day. It is super cheap and fast.",
            "tips": "Mention that token numbers and pricing are from official Groq documentation."
        },
        {
            "num": "Slide 9",
            "title": "What I Learned & Viva Defense Answers",
            "bullets": [
                "<b>Learning 1:</b> Never trust an LLM with math. LLMs understand English words, but Python must calculate budgets and totals.",
                "<b>Learning 2:</b> Structured prompting prevents hallucinations. Setting clear constraints keeps the AI inside boundaries.",
                "<b>Learning 3:</b> Always keep humans in the loop when real money is involved.",
                "<b>Viva Q&A Ready:</b> Prepared to explain how numbers_in() handles commas, how tuple keys track split claims, and why .env protects API keys."
            ],
            "script": "Here are my three biggest learnings from this capstone. First, never trust an LLM with math. Use Python for numbers and rules. Second, prompt engineering with clear constraints stops the model from hallucinating. Third, always keep a human in the loop for money decisions. I am ready to explain every function and line of code in my project.",
            "tips": "State with confidence that you wrote and understand every line of Python code."
        },
        {
            "num": "Slide 10",
            "title": "Conclusion & Project Deliverables",
            "bullets": [
                "<b>All 7 Components Complete:</b> 1. Spec, 2. Python program, 3. Groq API & 5-role prompt, 4. Eval & Red-team tests, 5. Judgment Framework, 6. Cost & latency report, 7. Git repo.",
                "<b>Outputs Generated:</b> payable.csv (14 claims, Rs. 30,650), review.csv (8 claims), results.csv, summary.txt.",
                "<b>User Interfaces:</b> Terminal ASCII dashboard and direct HTML visual dashboard (dashboard.html).",
                "<b>GitHub:</b> Clean Git commits pushed to GitHub with .gitignore protecting keys."
            ],
            "script": "In conclusion, all seven requirements of our college specification are fully built, tested, and pushed to GitHub. The software helps our college clubs audit expenses cleanly while keeping our faculty treasurer in total control. Thank you so much for your time and guidance. I welcome your questions!",
            "tips": "Thank your teachers and say you are ready for their questions."
        }
    ]

    story = []
    for s_idx, s in enumerate(slides_data):
        col_w = [340, 390]

        left_flow = [
            Paragraph("<b>SLIDE BULLETS (What the audience sees):</b>", subhead_style),
            Spacer(1, 2)
        ]
        for b in s["bullets"]:
            left_flow.append(Paragraph(f"• {b}", bullet_style))

        right_flow = [
            Paragraph("<b>PRESENTER'S VIEW (What you say in simple English):</b>", subhead_style),
            Paragraph(s["script"], script_style),
            Spacer(1, 4),
            Paragraph("<b>SIMPLE PRESENTATION TIPS:</b>", subhead_style),
            Paragraph(f"• {s['tips']}", body_style)
        ]

        card_data = [[left_flow, right_flow]]
        card_table = Table(card_data, colWidths=col_w)
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        slide_block = [
            Paragraph(f"{s['num'].upper()} · PRESENTATION GUIDE", slide_num_style),
            Paragraph(s["title"], slide_title_style),
            card_table
        ]

        story.append(KeepTogether(slide_block))
        if s_idx < len(slides_data) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Updated Presentation Guide PDF saved to {pdf_path}")

if __name__ == "__main__":
    build_pdf()
