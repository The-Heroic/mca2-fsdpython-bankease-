import os
import sys
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

DOCS_DIR = r"C:\Users\akanu\Desktop\MCA\HCL Training\BankEase\docs"
PRIMARY_PDF_PATH = os.path.join(DOCS_DIR, "BankEase_Comprehensive_Project_Report.pdf")
UPDATED_PDF_PATH = os.path.join(DOCS_DIR, "BankEase_Comprehensive_Project_Report_Updated.pdf")
PDF_PATH = UPDATED_PDF_PATH

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0D3B66"))
        # Header
        self.drawString(54, 750, "P044 | BankEase - NextGen Net Banking Application — Comprehensive Project Report")
        self.setStrokeColor(colors.HexColor("#0D3B66"))
        self.setLineWidth(0.8)
        self.line(54, 742, 558, 742)
        # Footer
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(54, 32, "ABES Engineering College • MCA 2nd Year • FSD Python • Roll No: 2500320140029")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Color Palette
    primary_color = colors.HexColor("#0D3B66")       # Navy Blue
    secondary_color = colors.HexColor("#1D5FA7")     # Slate Blue
    accent_color = colors.HexColor("#008080")        # Deep Teal
    highlight_bg = colors.HexColor("#EBF3FA")        # Light Blue Tint
    highlight_border = colors.HexColor("#0969DA")    # Vibrant Blue
    alert_bg = colors.HexColor("#FFF8E6")            # Warning / Alert Warm Amber
    alert_border = colors.HexColor("#B08800")        # Dark Amber
    success_bg = colors.HexColor("#E6FFED")          # Light Green Tint
    success_border = colors.HexColor("#2DA44E")      # Crisp Green
    dark_text = colors.HexColor("#1F2328")           # High Contrast Charcoal
    muted_text = colors.HexColor("#59636E")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=dark_text,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary_color
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0969DA"),
        backColor=colors.HexColor("#F6F8FA"),
        spaceAfter=2
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=dark_text
    )

    callout_title = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=primary_color
    )

    story = []

    def make_callout(content_list, bg=highlight_bg, border=highlight_border):
        data = [[content_list]]
        t = Table(data, colWidths=[512])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 1.5, border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>ABES ENGINEERING COLLEGE • MCA DEPARTMENT</b><br/><font color='#59636E'>FULL STACK DEVELOPMENT WITH PYTHON (FSD PYTHON) • CAPSTONE PROJECT</font>",
        ParagraphStyle('SuperBadge', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=primary_color, alignment=1, spaceAfter=10)
    ))
    story.append(Paragraph("BankEase — NextGen Net Banking Application", title_style))
    story.append(Paragraph("Comprehensive Project Documentation, System Architecture & Technical Verification", subtitle_style))
    story.append(HRFlowable(width="70%", thickness=2, color=accent_color, spaceBefore=0, spaceAfter=12))

    # HIGHLIGHTED REPOSITORY CALLOUT BANNER (Requirement 1)
    repo_highlight_content = [
        Paragraph("<b>OFFICIAL GITHUB PROJECT REPOSITORY & CODEBASE</b>", callout_title),
        Spacer(1, 2),
        Paragraph(
            "<b>Repository URL:</b> <font color='#0969DA'><u><b>https://github.com/The-Heroic/mca2-fsdpython-bankease-</b></u></font><br/>"
            "<b>Release Tag:</b> <font color='#008080'><b>v1.0.0</b></font> (Production Candidate) &nbsp;|&nbsp; "
            "<b>Branch Model:</b> GitFlow (<code>main</code>, <code>develop</code>, feature branches) &nbsp;|&nbsp; "
            "<b>License:</b> MIT Academic License",
            callout_text
        )
    ]
    story.append(make_callout(repo_highlight_content, bg=highlight_bg, border=highlight_border))
    story.append(Spacer(1, 12))

    # CANDIDATE & ACADEMIC CREDENTIALS TABLE (Requirement 3: Roll no, Batch ID, Project ID, Project Mentor)
    cred_table_data = [
        [
            Paragraph("<b>Candidate Roll No:</b>", table_cell_bold),
            Paragraph("<b><font color='#0D3B66' size='9'>2500320140029</font></b>", table_cell_style),
            Paragraph("<b>Project ID:</b>", table_cell_bold),
            Paragraph("<b><font color='#0D3B66' size='9'>FSD Python - P044</font></b>", table_cell_style)
        ],
        [
            Paragraph("<b>Batch ID:</b>", table_cell_bold),
            Paragraph("<b>ABES_OND26_MCA 2ndYear_FSD Python_Batch 01</b>", table_cell_style),
            Paragraph("<b>Project Mentor:</b>", table_cell_bold),
            Paragraph("<b><font color='#008080' size='9'>Mr. Madana</font></b>", table_cell_style)
        ],
        [
            Paragraph("<b>Student Name:</b>", table_cell_bold),
            Paragraph("Anurag", table_cell_style),
            Paragraph("<b>Academic Program:</b>", table_cell_bold),
            Paragraph("Master of Computer Applications (MCA 2nd Year)", table_cell_style)
        ],
        [
            Paragraph("<b>Institution:</b>", table_cell_bold),
            Paragraph("ABES Engineering College, Ghaziabad", table_cell_style),
            Paragraph("<b>Training Partner:</b>", table_cell_bold),
            Paragraph("HCL Training / Corporate Skills Program", table_cell_style)
        ],
    ]
    cred_table = Table(cred_table_data, colWidths=[105, 170, 95, 142])
    cred_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F8FB")),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#1D5FA7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(cred_table)
    story.append(Spacer(1, 10))

    # TECHNICAL PROJECT METADATA TABLE
    meta_table_data = [
        [Paragraph("<b>Domain & Category:</b>", table_cell_bold), Paragraph("FinTech, Retail Banking, Double-Entry Ledger, Regulatory Compliance", table_cell_style)],
        [Paragraph("<b>Technology Stack:</b>", table_cell_bold), Paragraph("Python 3.11/3.13 • Django 4.2 LTS • DRF • React 18 • Vite • Bootstrap 5 • MySQL 8.0 InnoDB", table_cell_style)],
        [Paragraph("<b>Database Architecture:</b>", table_cell_bold), Paragraph("<b>3NF Normalized</b> across <b>20 Relational Tables</b> with Foreign Key Constraints & Indexes", table_cell_style)],
        [Paragraph("<b>Security & Cryptography:</b>", table_cell_bold), Paragraph("Stateless SimpleJWT (Access/Refresh), PBKDF2-SHA256 (600k rounds), Row Locking, Audit Trail", table_cell_style)],
        [Paragraph("<b>Testing & Verification:</b>", table_cell_bold), Paragraph("<b>11 Pytest Suites</b> (100% Pass Rate across all 10 Business Modules)", table_cell_style)],
        [Paragraph("<b>Agile Lifecycle Scope:</b>", table_cell_bold), Paragraph("<b>12 Epics</b> (P18-E01 to E12) • <b>37 User Stories</b> • <b>17 Deliverables</b> (D01–D17) Completed", table_cell_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[120, 392])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFDFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#2B7A78")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D8E2DC")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 12))
    # Quick Summary Highlight on Cover
    summary_callout = [
        Paragraph("<b>EXECUTIVE HIGHLIGHT:</b> BankEase modernizes digital retail banking by unifying customer self-service with officer administrative controls. Key innovations include <b>row-level database locking (select_for_update)</b> preventing concurrent balance double-debits, <b>automated AML anomaly alerts</b> (>= ₹5,00,000), <b>reducing-balance EMI mathematical engines</b>, and <b>3-attempt failed credential account lockouts</b>.", callout_text)
    ]
    story.append(make_callout(summary_callout, bg=colors.HexColor("#F8F9FA"), border=colors.HexColor("#D0D7DE")))

    story.append(PageBreak())

    # =========================================================================
    # 1. EXECUTIVE SUMMARY & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Project Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "<b>BankEase (P044 / P18)</b> is an enterprise-grade full-stack net banking application designed to modernize retail digital banking. Built under the <b>Full Stack Development with Python (FSD Python)</b> track at <b>ABES Engineering College</b>, it provides an intuitive web interface for retail customers, branch management tooling for bank officers, and rigorous oversight consoles for compliance auditors and administrators.",
        body_style
    ))
    story.append(Paragraph(
        "The project directly addresses critical real-world banking challenges: eliminating database race conditions during concurrent account balance debits, strictly enforcing regulatory cooling periods for new transfer payees, preventing credential brute-forcing via automated account lockouts, providing mathematical amortization schedules for consumer loans, and maintaining immutable audit trails for compliance verification.",
        body_style
    ))

    # Callout: Critical Architectural Highlights
    story.append(make_callout([
        Paragraph("<b>CRITICAL BANKING SAFEGUARDS IMPLEMENTED:</b>", callout_title),
        Paragraph("• <b>Concurrency & Double-Debit Protection:</b> Wrapped inside atomic DB transactions using row-level locking (<code>select_for_update()</code>).<br/>"
                  "• <b>Payee Cooling Period:</b> Mandatory cooling delay prevents unauthorized fraud after newly added beneficiaries.<br/>"
                  "• <b>Brute-Force Lockout:</b> Locks customer profiles immediately after 3 consecutive invalid password attempts.<br/>"
                  "• <b>AML Surveillance:</b> Automated AML monitors trigger compliance flags on single transactions >= ₹5,00,000.", callout_text)
    ], bg=alert_bg, border=alert_border))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Core Strategic Objectives:", h2_style))
    story.append(Paragraph("• <b>Robust Multi-Role Authentication:</b> Stateless JWT tokens with role claims (<code>CUSTOMER</code>, <code>BANK_OFFICER</code>, <code>ADMIN</code>, <code>AUDITOR</code>) and automatic account lockout after 3 consecutive failed attempts.", bullet_style))
    story.append(Paragraph("• <b>Account & Ledger Management:</b> Flexible opening of Savings, Current, and Salary accounts, KYC identity tracking, and date/type filtered account statements.", bullet_style))
    story.append(Paragraph("• <b>Atomic Concurrency Control:</b> High-speed intra-bank and inter-bank transfers (IMPS, NEFT, RTGS, UPI) wrapped in database-level row locking to guarantee mathematical consistency and zero overdrafts.", bullet_style))
    story.append(Paragraph("• <b>Integrated Financial Ecosystem:</b> BBPS-compliant utility bill payments with auto-pay rules, loan application & reducing-rate EMI servicing, and Fixed Deposit / Recurring Deposit wealth portfolios.", bullet_style))
    story.append(Paragraph("• <b>Audit Trails & Risk Compliance:</b> Automated flagging of high-value Anti-Money Laundering (AML) transactions and immutable security audit logs.", bullet_style))

    # =========================================================================
    # 2. SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Enterprise System Architecture & Technology Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "BankEase employs a clean, decoupled <b>3-Tier Architecture</b> ensuring strict separation of concerns, high maintainability, and enterprise-grade resilience:",
        body_style
    ))

    arch_data = [
        [Paragraph("Architectural Tier", table_header_style), Paragraph("Component Technologies", table_header_style), Paragraph("Key Responsibilities & Design Patterns", table_header_style)],
        [
            Paragraph("<b>Presentation Layer</b><br/>(Client-Side SPA)", table_cell_bold),
            Paragraph("• React 18<br/>• Vite Build Engine<br/>• Bootstrap 5<br/>• Axios Client", table_cell_style),
            Paragraph("Single Page Application (SPA), role-based tab routing, client-side input validation, responsive mobile-first UI, Axios HTTP request interceptors automatically injecting <code>Authorization: Bearer &lt;token&gt;</code>.", table_cell_style)
        ],
        [
            Paragraph("<b>Application Layer</b><br/>(REST API Server)", table_cell_bold),
            Paragraph("• Python 3.11 / 3.13<br/>• Django 4.2 LTS<br/>• Django REST Framework<br/>• SimpleJWT", table_cell_style),
            Paragraph("10 modular micro-apps under <code>backend/apps/</code>, stateless JWT token issuing & blacklisting, role-based permission classes (<code>IsBankOfficerOrAdmin</code>), database atomic transactions, reducing-balance EMI calculations.", table_cell_style)
        ],
        [
            Paragraph("<b>Database Layer</b><br/>(Relational Storage)", table_cell_bold),
            Paragraph("• MySQL 8.0 Community<br/>• InnoDB Storage Engine<br/>• utf8mb4 Charset<br/>• PyMySQL Adapter", table_cell_style),
            Paragraph("3NF-normalized relational schema across 20 tables, ACID compliance, foreign key constraints with cascade/restrict rules, B-tree indexes on lookup columns, and SQLite fallback for local test execution.", table_cell_style)
        ],
    ]
    arch_table = Table(arch_data, colWidths=[110, 140, 262])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)

    story.append(PageBreak())

    # =========================================================================
    # 3. THE 10 CORE MODULES SPECIFICATION
    # =========================================================================
    story.append(Paragraph("3. Detailed Functional Modules Specification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))

    modules_data = [
        ("Module 1: User Authentication & RBAC", "Handles secure customer registration, credential verification, and JWT session token generation. Password hashing utilizes PBKDF2-SHA256 with 600,000 rounds. Implements custom role assignment across Customer, Bank Officer, Administrator, and Auditor roles. Integrates an automated security lockout locking profiles after 3 consecutive failed attempts."),
        ("Module 2: Account Management", "Supports opening and lifecycle management of Savings, Current, and Salary accounts. Generates unique 12-digit account numbers mapped to IFSC codes. Tracks real-time account balances, minimum balance compliance, nominee assignments, and provides statement inquiries with transaction type and date range filters."),
        ("Module 3: Funds Transfer Engine", "Executes intra-bank (book transfers) and inter-bank clearing (IMPS, NEFT, RTGS, UPI). Enforces beneficiary registration, IFSC syntax validation, and configurable cooling periods. Employs Django atomic transactions with row-level database locking (select_for_update) to guarantee balance integrity and zero race conditions."),
        ("Module 4: Bill Payment (BBPS)", "Comprehensive utility biller directory covering Electricity, Water, Piped Gas, Broadband, DTH, Mobile Postpaid, and Credit Card categories. Enables customer biller linking, auto-pay threshold setup, instant bill fetch, and issuance of digital BBPS payment receipts with unique transaction references."),
        ("Module 5: Loan Management", "End-to-end credit workflow featuring a mathematical client-side reducing-balance EMI calculator. Supports loan applications with credit appraisal and CIBIL score tracking. Bank officers verify applicant documents and trigger one-click disbursal, automatically creating monthly installment amortization schedules."),
        ("Module 6: Investment Services", "Wealth management portal allowing customers to subscribe to Fixed Deposits (FD), Recurring Deposits (RD), and Mutual Fund portfolios. Calculates projected maturity amounts based on annual compounded return rates, and manages premature closure payouts with automated penalty deductions."),
        ("Module 7: Customer Support Portal", "Multi-category ticketing mechanism enabling customers to lodge inquiries (Disputed Transactions, Account Issues, KYC Updates). Facilitates real-time, threaded discussion records between customers and assigned bank officers, transitioning tickets from OPEN to IN_PROGRESS and RESOLVED."),
        ("Module 8: Security and Compliance", "Comprehensive risk management framework. Features KYC document uploads with officer verification workflows, an immutable security audit trail logging every administrative and authentication event (with IP addresses and User-Agents), and automated AML monitors flagging transactions >= INR 5,00,000."),
        ("Module 9: Notifications & Alerts", "Multi-channel event listener broadcasting real-time in-app alerts for balance deductions, security logins from new IPs, upcoming bill reminders, and loan EMI processing. Features unread badge counter and bulk mark-all-read updates."),
        ("Module 10: Executive Dashboard & Reporting", "Role-aware executive analytics. Customers view consolidated net worth, total investments, and visual credit vs debit summaries. Bank officers inspect pending KYC backlogs, loan applications, and flagged compliance queues. Features on-demand CSV financial statement downloads.")
    ]

    for title, desc in modules_data:
        story.append(Paragraph(f"<b><font color='#0D3B66'>{title}</font></b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. DATABASE DESIGN & 3NF NORMALIZATION
    # =========================================================================
    story.append(Paragraph("4. Relational Database Design & 3NF Schema", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "The BankEase database (<code>bankease_db</code>) is engineered in full compliance with the <b>Third Normal Form (3NF)</b>. Every non-prime attribute is non-transitively dependent on the primary key, eliminating data duplication, update anomalies, and inconsistencies.",
        body_style
    ))

    db_tables_data = [
        [Paragraph("Table Name", table_header_style), Paragraph("Module", table_header_style), Paragraph("Type", table_header_style), Paragraph("Primary Key", table_header_style), Paragraph("Foreign Key Relationships", table_header_style)],
        [Paragraph("roles", table_cell_bold), Paragraph("M1: Auth", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("role_id", code_style), Paragraph("None (System Roles: CUSTOMER, OFFICER, ADMIN, AUDITOR)", table_cell_style)],
        [Paragraph("branches", table_cell_bold), Paragraph("M1 & M2", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("branch_id", code_style), Paragraph("None (IFSC Code unique index)", table_cell_style)],
        [Paragraph("users", table_cell_bold), Paragraph("M1: Auth", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("user_id", code_style), Paragraph("roles(role_id), branches(home_branch_id)", table_cell_style)],
        [Paragraph("bank_accounts", table_cell_bold), Paragraph("M2: Accounts", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("account_id", code_style), Paragraph("users(user_id), branches(branch_id)", table_cell_style)],
        [Paragraph("beneficiaries", table_cell_bold), Paragraph("M3: Transfers", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("beneficiary_id", code_style), Paragraph("users(user_id)", table_cell_style)],
        [Paragraph("transactions", table_cell_bold), Paragraph("M3: Transfers", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("transaction_id", code_style), Paragraph("bank_accounts(account_id), counterparty, beneficiary", table_cell_style)],
        [Paragraph("biller_directory", table_cell_bold), Paragraph("M4: Bills", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("biller_id", code_style), Paragraph("None (BBPS National Biller Catalog)", table_cell_style)],
        [Paragraph("customer_billers", table_cell_bold), Paragraph("M4: Bills", table_cell_style), Paragraph("Associative", table_cell_style), Paragraph("customer_biller_id", code_style), Paragraph("users(user_id), biller_directory(biller_id), account", table_cell_style)],
        [Paragraph("bill_payments", table_cell_bold), Paragraph("M4: Bills", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("bill_payment_id", code_style), Paragraph("customer_billers, bank_accounts, transactions", table_cell_style)],
        [Paragraph("loan_products", table_cell_bold), Paragraph("M5: Loans", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("loan_product_id", code_style), Paragraph("None (Product Catalog: Home, Auto, Personal)", table_cell_style)],
        [Paragraph("loan_applications", table_cell_bold), Paragraph("M5: Loans", table_cell_style), Paragraph("Entity", table_cell_style), Paragraph("loan_id", code_style), Paragraph("users, bank_accounts, loan_products, officer", table_cell_style)],
        [Paragraph("loan_repayments", table_cell_bold), Paragraph("M5: Loans", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("repayment_id", code_style), Paragraph("loan_applications(loan_id), transactions", table_cell_style)],
        [Paragraph("investment_plans", table_cell_bold), Paragraph("M6: Investments", table_cell_style), Paragraph("Master", table_cell_style), Paragraph("plan_id", code_style), Paragraph("None (Plan Catalog: FD, RD, Mutual Funds)", table_cell_style)],
        [Paragraph("investments", table_cell_bold), Paragraph("M6: Investments", table_cell_style), Paragraph("Entity", table_cell_style), Paragraph("investment_id", code_style), Paragraph("users, bank_accounts, investment_plans", table_cell_style)],
        [Paragraph("support_tickets", table_cell_bold), Paragraph("M7: Support", table_cell_style), Paragraph("Entity", table_cell_style), Paragraph("ticket_id", code_style), Paragraph("users(user_id), officer, transactions", table_cell_style)],
        [Paragraph("ticket_messages", table_cell_bold), Paragraph("M7: Support", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("message_id", code_style), Paragraph("support_tickets(ticket_id), users(sender_user_id)", table_cell_style)],
        [Paragraph("kyc_documents", table_cell_bold), Paragraph("M8: Security", table_cell_style), Paragraph("Entity", table_cell_style), Paragraph("kyc_doc_id", code_style), Paragraph("users(user_id), officer", table_cell_style)],
        [Paragraph("security_audit_logs", table_cell_bold), Paragraph("M8: Security", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("audit_id", code_style), Paragraph("users(user_id)", table_cell_style)],
        [Paragraph("notifications", table_cell_bold), Paragraph("M9: Alerts", table_cell_style), Paragraph("Transaction", table_cell_style), Paragraph("notification_id", code_style), Paragraph("users(user_id)", table_cell_style)],
        [Paragraph("report_exports", table_cell_bold), Paragraph("M10: Reports", table_cell_style), Paragraph("Entity", table_cell_style), Paragraph("report_id", code_style), Paragraph("users(generated_by_user_id)", table_cell_style)],
    ]

    db_table = Table(db_tables_data, colWidths=[95, 75, 60, 85, 197])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(db_table)

    story.append(Spacer(1, 8))
    # Edge Cases Callout Box (Requirement 1 Highlight)
    edge_cases_content = [
        Paragraph("<b>CRITICAL TEST SEED DATA & VALIDATION EDGE-CASES:</b>", callout_title),
        Paragraph("1. <b>Edge Case 1 (user_id=11):</b> Empty optional fields (NULL DOB, PAN, Aadhaar, address) and zero-balance account in PENDING_KYC status.<br/>"
                  "2. <b>Edge Case 2 (user_id=12):</b> Exact maximum length boundary testing (120-char legal name and 255-char residential address).<br/>"
                  "3. <b>Edge Cases 3 & 4 (user_id=13, 14):</b> Duplicate-looking names in same city ('Rohit Kumar Sharma' vs 'Rohit Kumar  Sharma') with distinct PANs and accounts.<br/>"
                  "4. <b>Edge Case 5 (user_id=15):</b> Locked profile (failed_attempts=5, is_locked=TRUE) with FROZEN accounts and FLAGGED high-risk transfers.", callout_text)
    ]
    story.append(make_callout(edge_cases_content, bg=highlight_bg, border=highlight_border))

    story.append(PageBreak())

    # =========================================================================
    # 5. AGILE METHODOLOGY & SPRINT BREAKDOWN
    # =========================================================================
    story.append(Paragraph("5. Agile Methodology & Sprint Execution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "The project was executed following a 90-hour Agile roadmap divided into 4 structured sprints. All features were developed on dedicated feature branches off <code>develop</code>, verified with automated tests, and merged using non-fast-forward (<code>--no-ff</code>) pull requests.",
        body_style
    ))

    sprint_data = [
        [Paragraph("Sprint", table_header_style), Paragraph("Duration", table_header_style), Paragraph("Git Tag", table_header_style), Paragraph("Delivered Epics & User Stories", table_header_style), Paragraph("Deliverables Verified", table_header_style)],
        [
            Paragraph("<b>Sprint 0</b>", table_cell_bold),
            Paragraph("6 Hours", table_cell_style),
            Paragraph("<font color='#0969DA'><b>v0.1.0</b></font>", table_cell_style),
            Paragraph("<b>P18-E01 (Setup & Design):</b><br/>US01-US04. Repository setup, 3NF database schema, seed data, wireframes, project skeleton, JWT login.", table_cell_style),
            Paragraph("<b>D01–D03</b><br/>Repo, Wireframes, Database schema & seed scripts.", table_cell_style)
        ],
        [
            Paragraph("<b>Sprint 1</b>", table_cell_bold),
            Paragraph("28 Hours", table_cell_style),
            Paragraph("<font color='#0969DA'><b>v0.2.0</b></font>", table_cell_style),
            Paragraph("<b>P18-E02 to E05:</b><br/>US05-US16. User Authentication, Account Management, and Funds Transfer engine with atomic locking.", table_cell_style),
            Paragraph("<b>D04–D07</b><br/>Working Auth, Accounts, Transfers, Bills backend & UI.", table_cell_style)
        ],
        [
            Paragraph("<b>Sprint 2</b>", table_cell_bold),
            Paragraph("28 Hours", table_cell_style),
            Paragraph("<font color='#0969DA'><b>v0.3.0</b></font>", table_cell_style),
            Paragraph("<b>P18-E06 to E08:</b><br/>US17-US25. Bill Payment, Loan Management (EMI engine & disbursal), and Investment Services.", table_cell_style),
            Paragraph("<b>D08–D10</b><br/>Working Loans, Investments, and Support ticketing.", table_cell_style)
        ],
        [
            Paragraph("<b>Sprint 3</b>", table_cell_bold),
            Paragraph("28 Hours", table_cell_style),
            Paragraph("<font color='#008080'><b>v1.0.0</b></font>", table_cell_style),
            Paragraph("<b>P18-E09 to E12:</b><br/>US26-US37. Security/Compliance, Notifications & Alerts, Dashboard Analytics, Test Report, and Final Release.", table_cell_style),
            Paragraph("<b>D11–D17</b><br/>Security, Alerts, Reporting, Test Report (D14), Slides (D16), Final Release (D17).", table_cell_style)
        ],
    ]
    sprint_table = Table(sprint_data, colWidths=[65, 55, 65, 185, 142])
    sprint_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(sprint_table)

    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. TESTING & VERIFICATION SUMMARY
    # =========================================================================
    story.append(Paragraph("6. Quality Assurance & Test Verification Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))
    
    # Test Suite Pass Banner (Requirement 1 Highlight)
    story.append(make_callout([
        Paragraph("<b>AUTOMATED TEST SUITE STATUS: 100% PASS RATE (11 / 11 SUITES PASSED)</b>", ParagraphStyle('SuccessTitle', parent=callout_title, textColor=colors.HexColor("#1A7F37"))),
        Paragraph("All 10 business modules passed automated Pytest verification in <b>1.48 seconds</b>. Zero test regressions. Atomic transfers, concurrency isolation, balance verification, and security lockouts fully confirmed.", callout_text)
    ], bg=success_bg, border=success_border))
    story.append(Spacer(1, 8))

    test_data = [
        [Paragraph("Test Suite & Function", table_header_style), Paragraph("Module", table_header_style), Paragraph("Evaluation Objective & Acceptance Criteria", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("test_health_check", code_style), Paragraph("System", table_cell_style), Paragraph("Validates API availability and service version string", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_customer_registration_and_login_flow", code_style), Paragraph("M1: Auth", table_cell_style), Paragraph("Verifies user creation, password hashing, JWT token issue, and /me/ profile retrieval", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_account_locks_after_three_failed_attempts", code_style), Paragraph("M1: Auth", table_cell_style), Paragraph("Enforces account lockout on 3 consecutive invalid passwords (is_locked=True)", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_account_opening_officer_kyc_approval_and_intrabank_transfer", code_style), Paragraph("M2 & M3", table_cell_style), Paragraph("Tests PENDING_KYC opening, Officer KYC verification, and atomic balance debit/credit", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_transfer_rejects_insufficient_balance_and_cooling_beneficiary", code_style), Paragraph("M3: Transfers", table_cell_style), Paragraph("Blocks transfers exceeding available funds and enforces beneficiary cooling period", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_bill_payment_workflow", code_style), Paragraph("M4: Bills", table_cell_style), Paragraph("Links BBPS biller, computes convenience fees, debits account, and issues receipt", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_loan_application_disbursal_and_emi_payment", code_style), Paragraph("M5: Loans", table_cell_style), Paragraph("Calculates EMI, officer sanctions disbursal, creates schedule, and executes EMI payment", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_investment_booking_and_premature_closure", code_style), Paragraph("M6: Investments", table_cell_style), Paragraph("Books FD, projects maturity, and tests premature withdrawal with penalty deduction", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_support_ticket_lifecycle", code_style), Paragraph("M7: Support", table_cell_style), Paragraph("Raises ticket, exchanges discussion messages, and marks status as RESOLVED", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_kyc_verification_and_audit_logs", code_style), Paragraph("M8: Security", table_cell_style), Paragraph("Submits KYC doc, verifies officer approval, and asserts immutable audit log entries", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
        [Paragraph("test_notifications_and_dashboard_reporting", code_style), Paragraph("M9 & M10", table_cell_style), Paragraph("Tests alert badge count, mark-all-read, dashboard KPIs, and CSV export streaming", table_cell_style), Paragraph("<font color='#1A7F37'><b>✔ PASSED</b></font>", table_cell_style)],
    ]

    test_table = Table(test_data, colWidths=[150, 68, 230, 64])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(test_table)

    story.append(PageBreak())

    # =========================================================================
    # 7. INSTALLATION, SETUP & RUN GUIDE
    # =========================================================================
    story.append(Paragraph("7. Local Deployment & Setup Instructions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))

    # HIGHLIGHT REPO AND CREDENTIALS (Requirement 1 Highlight)
    story.append(make_callout([
        Paragraph("<b>PRE-CONFIGURED EVALUATION & DEMONSTRATION CREDENTIALS:</b>", callout_title),
        Paragraph("• <b>Retail Customer:</b> <code>aarav.sharma@example.com</code> / <code>Secure@123</code> (Active balance: ₹1,25,000.00)<br/>"
                  "• <b>Branch Officer:</b> <code>vikram.officer@bankease.com</code> / <code>Officer@123</code> (KYC approval & loan sanction)<br/>"
                  "• <b>System Admin:</b> <code>admin@bankease.com</code> / <code>Admin@123</code> (Full security compliance access)<br/>"
                  "• <b>Edge-Case Locked User:</b> <code>locked.user@example.com</code> / <code>WrongPassword</code> (Demonstrates 3-attempt lockout)", callout_text)
    ], bg=highlight_bg, border=highlight_border))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Step 1: Clone Repository & Create Virtual Environment", h2_style))
    story.append(Paragraph("git clone https://github.com/The-Heroic/mca2-fsdpython-bankease-.git<br/>cd mca2-fsdpython-bankease-<br/>python -m venv backend/venv<br/>backend/venv/Scripts/pip install -r backend/requirements.txt", code_style))

    story.append(Paragraph("Step 2: Database Initialization (MySQL 8.0)", h2_style))
    story.append(Paragraph("Execute the normalized schema DDL and realistic Indian sample seed data:", body_style))
    story.append(Paragraph("Get-Content database/schema.sql | & \"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe\" -u root -p<br/>Get-Content database/seed_data.sql | & \"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe\" -u root -p bankease_db", code_style))

    story.append(Paragraph("Step 3: Run Django Database Migrations & Pytest Suite", h2_style))
    story.append(Paragraph("cd backend<br/>.\\venv\\Scripts\\python.exe manage.py migrate<br/>.\\venv\\Scripts\\pytest.exe", code_style))

    story.append(Paragraph("Step 4: Launch Backend & Frontend Servers", h2_style))
    story.append(Paragraph("<b>Terminal 1 (Backend API Server):</b>", body_style))
    story.append(Paragraph("cd backend<br/>.\\venv\\Scripts\\python.exe manage.py runserver", code_style))
    story.append(Paragraph("<b>Terminal 2 (React Vite Frontend):</b>", body_style))
    story.append(Paragraph("cd frontend<br/>npm install<br/>npm run dev", code_style))
    story.append(Paragraph("Access the application in your browser at: <b><code>http://localhost:5173</code></b>", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Deliverables Evaluation Sign-Off", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceBefore=2, spaceAfter=8))

    signoff_data = [
        [Paragraph("Deliverable Code & Description", table_header_style), Paragraph("Evaluation Criteria", table_header_style), Paragraph("Artifact Reference", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("<b>D01–D03:</b> Architecture & DB", table_cell_bold), Paragraph("Repository, 3NF DDL, Seed data, ER Diagram", table_cell_style), Paragraph("<code>database/schema.sql</code>, <code>seed_data.sql</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
        [Paragraph("<b>D04–D13:</b> 10 Functional Modules", table_cell_bold), Paragraph("Data models, REST APIs, React screens & tests", table_cell_style), Paragraph("<code>backend/apps/</code>, <code>frontend/src/</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
        [Paragraph("<b>D14:</b> Comprehensive Test Report", table_cell_bold), Paragraph("Test execution log, 11 tests, defect resolution log", table_cell_style), Paragraph("<code>docs/test_report.md</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
        [Paragraph("<b>D15:</b> REST API Documentation", table_cell_bold), Paragraph("43 endpoints with request/response schemas", table_cell_style), Paragraph("<code>docs/api_docs.md</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
        [Paragraph("<b>D16:</b> Presentation Slide Deck", table_cell_bold), Paragraph("10-slide comprehensive deck for viva review", table_cell_style), Paragraph("<code>docs/presentation_slides.md</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
        [Paragraph("<b>D17:</b> Final Software Release", table_cell_bold), Paragraph("Merged to <code>main</code>, release tag <code>v1.0.0</code>", table_cell_style), Paragraph("Git Tag: <code>refs/tags/v1.0.0</code>", code_style), Paragraph("<font color='#1A7F37'><b>Complete</b></font>", table_cell_style)],
    ]
    signoff_table = Table(signoff_data, colWidths=[120, 160, 150, 82])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D0D7DE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E1E4E8")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(signoff_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "<b>Submitted By:</b> Anurag &nbsp;|&nbsp; "
        "<b>Roll No:</b> 2500320140029 &nbsp;|&nbsp; "
        "<b>Project ID:</b> FSD Python - P044 &nbsp;|&nbsp; "
        "<b>Mentor:</b> Mr. Madana &nbsp;|&nbsp; "
        "<b>Institution:</b> ABES Engineering College",
        ParagraphStyle('FooterSign', fontName='Helvetica-Bold', fontSize=8.5, textColor=primary_color, alignment=1)
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated comprehensive project report PDF: {UPDATED_PDF_PATH}")
    try:
        shutil.copyfile(UPDATED_PDF_PATH, PRIMARY_PDF_PATH)
        print(f"Successfully updated primary PDF: {PRIMARY_PDF_PATH}")
    except Exception as e:
        print(f"Primary PDF is currently open/locked by another process. Updated version saved at: {UPDATED_PDF_PATH}")

if __name__ == '__main__':
    build_pdf()
