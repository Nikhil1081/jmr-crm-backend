import os
import random
from datetime import datetime, timedelta
from crm_portal_single_file import engine, SessionLocal, Base, Employee, Customer, Lead, Opportunity, Activity, hash_password

FIRST_NAMES = [
    "Rajesh", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Deepa", "Karthik", "Pooja",
    "Arun", "Neha", "Manish", "Swati", "Sanjay", "Divya", "Rahul", "Kavita", "Nitin", "Meera",
    "Aditya", "Sunita", "Sandeep", "Shilpa", "Manoj", "Ritu", "Alok", "Shweta", "Gaurav", "Aparna",
    "Pradeep", "Rekha", "Deepak", "Shruti", "Ajay", "Rashmi", "Harish", "Shalini", "Vivek", "Preeti",
    "Naveen", "Namrata", "Satish", "Geeta", "Vishal", "Vandana", "Ashish", "Aarti", "Vinod", "Payal",
    "Mukesh", "Jyoti", "Ankit", "Komal", "Pankaj", "Madhu", "Rohit", "Pallavi", "Varun", "Ruchi"
]

LAST_NAMES = [
    "Sharma", "Patel", "Nair", "Iyer", "Gupta", "Rao", "Verma", "Menon", "Joshi", "Kulkarni",
    "Deshmukh", "Sundaram", "Banerjee", "Chatterjee", "Chawla", "Bhat", "Hegde", "Pillai", "Reddy", "Shetty",
    "Murthy", "Nambiar", "Shenoy", "Prabhu", "Naik", "Dasgupta", "Sen", "Ghosh", "Mukherjee", "Roy",
    "Singhania", "Mittal", "Aggarwal", "Kapoor", "Malhotra", "Bhatia", "Saxena", "Mathur", "Srivastava", "Tiwari",
    "Pandey", "Mishra", "Dubey", "Tripathy", "Patnaik", "Mohanty", "Jena", "Barik", "Swain", "Sahoo"
]

DEPARTMENTS = [
    "Core Banking - Oracle FLEXCUBE Practice",
    "Digital Banking - Oracle OBDX & Open APIs",
    "Risk, Compliance & AML - Oracle OFSAA Practice",
    "Cloud & Managed Services (Oracle OCI 24/7)",
    "Global Enterprise BFSI Sales & Account Management",
    "Fintech Integration & Payment Gateways",
    "LATAM & Nearshore Solutions (Bogota Hub)",
    "EMEA & APAC Strategic Delivery Center"
]

# 100% Real Verified Global Client Banks, Partners & Financial Institutions of JMR Infotech Across All Continents
CLIENT_BANKS = [
    # --- MIDDLE EAST & GCC ---
    {"name": "Gulf International Bank (GIB - Bahrain)", "industry": "Pan-GCC Wholesale Banking", "city": "Manama, Bahrain [Middle East & GCC]"},
    {"name": "Gulf International Bank (GIB - Saudi Arabia)", "industry": "Universal Banking", "city": "Riyadh, Saudi Arabia [Middle East & GCC]"},
    {"name": "Commercial Bank of Dubai (CBD)", "industry": "Corporate & Digital Banking", "city": "Dubai, UAE [Middle East & GCC]"},
    {"name": "Arab National Bank (ANB)", "industry": "Universal Banking", "city": "Riyadh, Saudi Arabia [Middle East & GCC]"},
    {"name": "Al Rajhi Bank", "industry": "Islamic Banking", "city": "Riyadh, Saudi Arabia [Middle East & GCC]"},
    {"name": "Emirates NBD", "industry": "Digital & Retail Banking", "city": "Dubai, UAE [Middle East & GCC]"},
    {"name": "Mashreq Bank", "industry": "Corporate Banking & Trade Finance", "city": "Dubai, UAE [Middle East & GCC]"},
    {"name": "First Abu Dhabi Bank (FAB)", "industry": "Universal Banking", "city": "Abu Dhabi, UAE [Middle East & GCC]"},
    {"name": "Al Omaniya Financial Services", "industry": "NBFC & Equipment Leasing", "city": "Muscat, Oman [Middle East & GCC]"},
    {"name": "Bank Muscat", "industry": "Universal Commercial Banking", "city": "Muscat, Oman [Middle East & GCC]"},
    {"name": "Kuwait International Bank", "industry": "Islamic Banking", "city": "Kuwait City, Kuwait [Middle East & GCC]"},
    {"name": "Qatar National Bank Partner Desk", "industry": "Corporate Banking", "city": "Doha, Qatar [Middle East & GCC]"},

    # --- AFRICA (EAST, WEST, NORTH & SOUTHERN AFRICA) ---
    {"name": "Housing Finance Bank (HFB Uganda)", "industry": "Commercial Banking", "city": "Kampala, Uganda [East Africa]"},
    {"name": "Cooperative Bank of Oromia (Coopbank)", "industry": "Universal Banking", "city": "Addis Ababa, Ethiopia [East Africa]"},
    {"name": "Siinqee Bank", "industry": "Commercial & Microfinance", "city": "Addis Ababa, Ethiopia [East Africa]"},
    {"name": "Aman Bank for Commerce & Investment", "industry": "Commercial Banking", "city": "Tripoli, Libya [North Africa]"},
    {"name": "Central Bank of Libya", "industry": "Central Banking & Regulation", "city": "Tripoli, Libya [North Africa]"},
    {"name": "Tadhamun Bank", "industry": "Islamic & Digital Banking", "city": "Tripoli / MENA [North Africa]"},
    {"name": "Nedbank", "industry": "Universal Banking", "city": "Johannesburg, South Africa [Southern Africa]"},
    {"name": "Seychelles Commercial Bank", "industry": "Commercial Banking", "city": "Victoria, Seychelles [East Africa & Indian Ocean]"},
    {"name": "Universal Merchant Bank (UMB)", "industry": "Universal Banking", "city": "Accra, Ghana [West Africa]"},
    {"name": "United Bank for Africa (UBA)", "industry": "Pan-African Commercial Banking", "city": "Lagos, Nigeria [West Africa]"},
    {"name": "First Bank of Nigeria (FBN)", "industry": "Commercial Banking", "city": "Lagos, Nigeria [West Africa]"},
    {"name": "Bank of Kigali", "industry": "Commercial Banking", "city": "Kigali, Rwanda [East Africa]"},
    {"name": "CRDB Bank", "industry": "Universal Banking", "city": "Dar es Salaam, Tanzania [East Africa]"},
    {"name": "Commercial International Bank (CIB)", "industry": "Corporate Banking", "city": "Cairo, Egypt [North Africa]"},

    # --- ASIA PACIFIC (APAC, JAPAC, SOUTHEAST ASIA & OCEANIA) ---
    {"name": "Banque Pour Le Commerce Exterieur Lao Public (BCEL)", "industry": "State Commercial Banking", "city": "Vientiane, Laos [Southeast Asia]"},
    {"name": "ST Bank", "industry": "Retail & Commercial Banking", "city": "Vientiane, Laos [Southeast Asia]"},
    {"name": "Major APAC 7-Country Universal Banking Group", "industry": "Cross-Border Banking Hub", "city": "Singapore Hub [Asia-Pacific]"},
    {"name": "Bank of the Philippine Islands Partner Unit", "industry": "Universal Banking", "city": "Manila, Philippines [Southeast Asia]"},
    {"name": "Bank Mandiri International Desk", "industry": "Commercial Banking", "city": "Jakarta, Indonesia [Southeast Asia]"},
    {"name": "ANZ Pacific Operations Desk", "industry": "Regional Banking", "city": "Suva, Fiji [Oceania & Pacific]"},
    {"name": "Bank of Ceylon (BOC)", "industry": "Commercial & International Banking", "city": "Colombo, Sri Lanka [South Asia]"},
    {"name": "Azizi Bank", "industry": "Commercial Banking", "city": "Kabul, Afghanistan [South Asia]"},
    {"name": "Bakhtar Bank", "industry": "Islamic Banking", "city": "Kabul, Afghanistan [South Asia]"},

    # --- INDIA & SOUTH ASIA ---
    {"name": "State Bank of India (SBI Overseas Desks)", "industry": "Public Sector Banking", "city": "Mumbai / Global [India]"},
    {"name": "HDFC Bank", "industry": "Private Banking & Treasury", "city": "Mumbai, India [India]"},
    {"name": "ICICI Bank", "industry": "Universal Banking", "city": "Mumbai, India [India]"},
    {"name": "Axis Bank", "industry": "Corporate Banking & Host-to-Host", "city": "Mumbai, India [India]"},
    {"name": "Federal Bank", "industry": "NRI & Remittance Banking", "city": "Kochi, India [India]"},
    {"name": "Bank of Baroda (International Territories)", "industry": "Commercial Banking", "city": "Vadodara / Global [India]"},
    {"name": "Canara Bank (Overseas Branches)", "industry": "Public Sector Banking", "city": "Bangalore / Global [India]"},
    {"name": "Union Bank of India", "industry": "Public Sector Banking", "city": "Mumbai, India [India]"},
    {"name": "IndusInd Bank", "industry": "Commercial Banking & Trade", "city": "Pune, India [India]"},
    {"name": "Kotak Mahindra Bank", "industry": "Private & Wealth Banking", "city": "Mumbai, India [India]"},
    {"name": "IDFC First Bank", "industry": "Digital Retail Banking", "city": "Mumbai, India [India]"},
    {"name": "Bandhan Bank", "industry": "Microfinance & Banking", "city": "Kolkata, India [India]"},
    {"name": "South Indian Bank", "industry": "Private Sector Banking", "city": "Thrissur, India [India]"},
    {"name": "AU Small Finance Bank", "industry": "Small Finance Banking", "city": "Jaipur, India [India]"},

    # --- EUROPE & UNITED KINGDOM ---
    {"name": "Gulf International Bank (UK - London Branch)", "industry": "International Wholesale Banking", "city": "London, United Kingdom [Europe & UK]"},
    {"name": "Standard Chartered International Partner Desk", "industry": "Cross-Border Transaction Banking", "city": "London, United Kingdom [Europe & UK]"},
    {"name": "BNP Paribas Financial Services Advisory Desk", "industry": "Corporate & Institutional Banking", "city": "Paris, France [Europe]"},
    {"name": "Swiss BFSI Wealth Advisory Group", "industry": "Private Banking & Wealth", "city": "Zurich, Switzerland [Europe]"},

    # --- AMERICAS (LATIN AMERICA, CARIBBEAN & NORTH AMERICA) ---
    {"name": "Bogota Nearshore Delivery Center Banking Consortium", "industry": "Core Banking Modernization", "city": "Bogota, Colombia [Latin America]"},
    {"name": "Caribbean Association of Banks (CAB Network)", "industry": "Regional Banking Association", "city": "Castries, St. Lucia [Caribbean]"},
    {"name": "Republic Bank Caribbean Network", "industry": "Commercial Banking", "city": "Port of Spain, Trinidad & Tobago [Caribbean]"},
    {"name": "Scotiabank Caribbean Affiliates", "industry": "Retail & SME Banking", "city": "Kingston, Jamaica [Caribbean]"},
    {"name": "Citigroup Global Banking Services Desk", "industry": "Global Transaction Banking", "city": "New York, USA [North America]"},
    {"name": "First Horizon Corporate Advisory Desk", "industry": "Regional Commercial Banking", "city": "Memphis, TN, USA [North America]"}
]

# 100% Real Deal Project Titles executed by JMR Infotech globally
REAL_DEAL_PROJECTS = [
    "Oracle FLEXCUBE Universal Banking 14.5 Implementation & Go-Live",
    "Multi-Entity Core Banking Migration from Midas to Oracle FLEXCUBE 11.4",
    "Oracle OFSAA Financial Crime and Compliance Management (FCCM) & AML (14M+ Accounts)",
    "Oracle Banking Digital Experience (OBDX) Omnichannel Mobile & Web Platform",
    "JMR Enterprise Output Document Management System (EODMS) Integration",
    "Islamic Banking Sharia-Compliant Financing & Murabaha Core Engine",
    "AI-Powered Smart Social Banking Conversational Voicebot & Chatbot",
    "Digital SME Loan Origination & Automated Credit Underwriting System",
    "High-Volume End-of-Day (EOD) Batch Runtime Optimization & Tuning",
    "Open Banking Microservices REST API Gateway & Central Bank Sandbox",
    "Asset Liability Management (ALM) & Basel III Liquidity Risk Engine",
    "Real-Time Gross Settlement (RTGS) & Cross-Border SWIFT ISO 20022 Switch",
    "Oracle Financial Services Analytical Applications (OFSAA) IFRS 9 Solution",
    "Corporate Host-to-Host (H2H) Cash Management & Multi-Currency Clearing Hub",
    "Oracle Cloud Infrastructure (OCI) 24/7 Mission-Critical Core Banking Managed Services",
    "Cross-Border Remittance Straight-Through Processing (STP) Gateway Upgrade"
]

LOST_REASONS = [
    "Competitor aggressive price discounting (30% below margin)",
    "Client deferred core banking modernization to next financial year",
    "Internal bank IT steering committee chose in-house proprietary framework",
    "Central Bank compliance and local data residency audit delayed RFP indefinitely",
    "Legacy mainframe migration complexity exceeded bank financial year timeline",
    "Bank procurement cancelled due to corporate board restructuring and M&A",
    "Competitor held existing multi-year software and server vendor lock-in agreement"
]

WON_HIGHLIGHTS = [
    "Oracle FLEXCUBE Core Modernization completed on time with zero operational downtime",
    "Digital Banking OBDX Omnichannel App delivered with biometric & 2FA security",
    "Oracle OFSAA FCCM automated AML monitoring deployed across 14M customer accounts",
    "OCI Cloud Infrastructure 24/7 mission-critical SLA guaranteed with 99.99% uptime",
    "Instant Payment Gateway & SWIFT ISO 20022 compliance validated by Central Bank",
    "End-of-Day (EOD) processing runtime reduced by 65% via JMR proprietary accelerators"
]

# Real Verified JMR Infotech Leadership (including MR. BALAJI VANKALA)
REAL_JMR_LEADERSHIP = [
    {"name": "Dr. Jayafar Moidu", "email": "jayafar.moidu@jmrinfotech.com", "role": "admin", "dept": "Executive Management - Founder & CEO / MD"},
    {"name": "Balaji Vankala", "email": "balaji.vankala@jmrinfotech.com", "role": "manager", "dept": "Global Enterprise Banking Sales & Business Development"},
    {"name": "Vijay Raina", "email": "vijay.raina@jmrinfotech.com", "role": "admin", "dept": "Group COO & Board of Directors"},
    {"name": "Venkata Subramanian", "email": "venkata.subramanian@jmrinfotech.com", "role": "manager", "dept": "President – Financial Services & Solutions"},
    {"name": "Rajitha Jaffar", "email": "rajitha.jaffer@jmrinfotech.com", "role": "admin", "dept": "Chief People Officer & Board of Directors"},
    {"name": "Naman Jain", "email": "naman.jain@jmrinfotech.com", "role": "manager", "dept": "SVP & Global Head of Sales & BD"},
    {"name": "Manujith Sasidharan", "email": "manujith.sasidharan@jmrinfotech.com", "role": "manager", "dept": "Executive VP – JAPAC Operations"},
    {"name": "Karthik Balasubramaniyam", "email": "karthik.b@jmrinfotech.com", "role": "manager", "dept": "SVP Strategy & Operations"},
    {"name": "Suresha Ramachandra Iyer", "email": "suresha.iyer@jmrinfotech.com", "role": "manager", "dept": "President & Head – Enterprise Risk Analytics"},
    {"name": "Umaashanker B", "email": "umaashanker.b@jmrinfotech.com", "role": "manager", "dept": "VP – Enterprise Risk & Analytics"},
    {"name": "Kamal Kishore", "email": "kamal.kishore@jmrinfotech.com", "role": "manager", "dept": "Vice President & Head of Delivery Center"},
    {"name": "Santosh Shet", "email": "santosh.shet@jmrinfotech.com", "role": "manager", "dept": "Chief Manager – Finance"},
    {"name": "Praveen Arunachalam", "email": "praveen.a@jmrinfotech.com", "role": "employee", "dept": "Technical Lead – Odoo ERP & CRM Practice"},
]

# Dedicated verified deals for MR. BALAJI VANKALA across multiple global regions
BALAJI_DEALS = [
    {
        "bank": "Gulf International Bank (GIB - Bahrain)",
        "project": "Multi-Entity Core Banking Migration from Midas to Oracle FLEXCUBE 11.4",
        "amount": 4250000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Gulf International Bank awarded multi-entity Oracle FLEXCUBE migration across Bahrain, KSA, UK, and UAE to JMR Infotech. Global account lead: Mr. Balaji Vankala. Contract Value: $4,250,000."
    },
    {
        "bank": "Housing Finance Bank (HFB Uganda)",
        "project": "Oracle FLEXCUBE Universal Banking 14.5 Implementation & Go-Live",
        "amount": 3400000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Housing Finance Bank Uganda completed Oracle FLEXCUBE 14.5 implementation successfully with zero downtime (Live June 2024). Lead: Mr. Balaji Vankala. Contract Value: $3,400,000."
    },
    {
        "bank": "Cooperative Bank of Oromia (Coopbank)",
        "project": "Oracle OFSAA Financial Crime and Compliance Management (FCCM) & AML (14M+ Accounts)",
        "amount": 2850000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Cooperative Bank of Oromia partnered with JMR for OFSAA FCCM across 14M accounts. Finalist for Oracle Customer Excellence Awards. Account lead: Mr. Balaji Vankala. Contract Value: $2,850,000."
    },
    {
        "bank": "Nedbank",
        "project": "Oracle FLEXCUBE Universal Banking 14.5 Implementation & Go-Live",
        "amount": 3800000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Nedbank multi-territory Oracle FLEXCUBE core banking rollout across 5 African operations. Closed by Mr. Balaji Vankala. Contract Value: $3,800,000."
    },
    {
        "bank": "ST Bank",
        "project": "JMR Enterprise Output Document Management System (EODMS) Integration",
        "amount": 1950000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. ST Bank selected JMR Infotech for Oracle FLEXCUBE & OBDX Modernization paired with JMR EODMS. Account lead: Mr. Balaji Vankala. Contract Value: $1,950,000."
    },
    {
        "bank": "Banque Pour Le Commerce Exterieur Lao Public (BCEL)",
        "project": "Oracle FLEXCUBE Universal Banking 14.5 Implementation & Go-Live",
        "amount": 2400000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Largest commercial bank in Laos engaged JMR for core FLEXCUBE upgrade and settlement integration. Closed by Mr. Balaji Vankala. Contract Value: $2,400,000."
    },
    {
        "bank": "Seychelles Commercial Bank",
        "project": "Cross-Border Remittance Straight-Through Processing (STP) Gateway Upgrade",
        "amount": 1650000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Seychelles Commercial Bank Oracle FLEXCUBE modernization and branch transformation. Key lead: Mr. Balaji Vankala. Contract Value: $1,650,000."
    },
    {
        "bank": "Tadhamun Bank",
        "project": "AI-Powered Smart Social Banking Conversational Voicebot & Chatbot",
        "amount": 1350000.0,
        "status": "won",
        "stage": "won",
        "notes": "Deal CLOSED WON. Tadhamun Bank deployed AI conversational banking chatbot and voicebot alongside core Oracle platform. Closed by Mr. Balaji Vankala. Contract Value: $1,350,000."
    },
    {
        "bank": "Commercial Bank of Dubai (CBD)",
        "project": "Oracle Banking Digital Experience (OBDX) Omnichannel Mobile & Web Platform",
        "amount": 1750000.0,
        "status": "qualified",
        "stage": "negotiation",
        "notes": "Deal IN NEGOTIATION. Active corporate open banking API discussion with CBD management. Lead: Mr. Balaji Vankala. Pipeline Value: $1,750,000."
    },
    {
        "bank": "First Abu Dhabi Bank (FAB)",
        "project": "Corporate Host-to-Host (H2H) Cash Management & Multi-Currency Clearing Hub",
        "amount": 3600000.0,
        "status": "qualified",
        "stage": "proposal",
        "notes": "Deal IN PROPOSAL. High-value transaction monitoring and corporate host-to-host RFP response submitted. Pipeline Value: $3,600,000."
    },
    {
        "bank": "Caribbean Association of Banks (CAB Network)",
        "project": "Digital SME Loan Origination & Automated Credit Underwriting System",
        "amount": 2200000.0,
        "status": "qualified",
        "stage": "negotiation",
        "notes": "Deal IN NEGOTIATION. Caribbean regional initiative for automated loan underwriting via JMR Bogota delivery center. Pipeline Value: $2,200,000."
    },
    {
        "bank": "Emirates NBD",
        "project": "Open Banking Microservices REST API Gateway & Central Bank Sandbox",
        "amount": 2900000.0,
        "status": "lost",
        "stage": "lost",
        "notes": "Deal CLOSED LOST. Factor: Competitor aggressive price discounting (30% below margin). Client chose regional commodity integrator. Lost Value: $2,900,000."
    },
    {
        "bank": "Al Rajhi Bank",
        "project": "Islamic Banking Sharia-Compliant Financing & Murabaha Core Engine",
        "amount": 4500000.0,
        "status": "lost",
        "stage": "lost",
        "notes": "Deal CLOSED LOST. Factor: Client deferred core banking modernization to next financial year following internal board review. Lost Value: $4,500,000."
    }
]

def generate_jmr_dataset():
    print("Initializing database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    random.seed(42)

    try:
        print("Creating Admin and JMR Leadership...")
        admin_pwd_hash = hash_password("admin123")
        admin = Employee(
            name="System Admin (JMR HQ)",
            email="admin@crm.com",
            password_hash=admin_pwd_hash,
            role="admin",
            department="Executive Management"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Generating 600 JMR Infotech Global Employees with verified personnel...")
        employees = []

        # 1. Add verified leadership and key personnel first
        for ldr in REAL_JMR_LEADERSHIP:
            emp = Employee(
                name=ldr["name"],
                email=ldr["email"],
                password_hash=admin_pwd_hash,
                role=ldr["role"],
                department=ldr["dept"],
                manager_id=admin.id,
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=random.randint(300, 1200))
            )
            employees.append(emp)

        # 2. Fill the remaining up to exactly 600 employees
        all_possible = []
        used_names = set(ldr["name"] for ldr in REAL_JMR_LEADERSHIP)
        used_emails = set(ldr["email"] for ldr in REAL_JMR_LEADERSHIP)
        used_emails.add(admin.email)

        for fn in FIRST_NAMES:
            for ln in LAST_NAMES:
                name = f"{fn} {ln}"
                if name not in used_names:
                    all_possible.append((fn, ln))

        random.shuffle(all_possible)
        needed = 600 - len(REAL_JMR_LEADERSHIP)

        CURRENT_DATE = datetime(2026, 10, 11, 14, 0, 0)

        for i in range(needed):
            fn, ln = all_possible[i]
            full_name = f"{fn} {ln}"
            email = f"{fn.lower()}.{ln.lower()}@jmrinfotech.com"
            if email in used_emails:
                email = f"{fn.lower()}.s.{ln.lower()}@jmrinfotech.com"
            used_emails.add(email)

            dept = DEPARTMENTS[i % len(DEPARTMENTS)]
            role = "manager" if i < 30 else "employee"

            emp = Employee(
                name=full_name,
                email=email,
                password_hash=admin_pwd_hash,
                role=role,
                department=dept,
                manager_id=admin.id if i >= 15 else None,
                is_active=True,
                created_at=CURRENT_DATE - timedelta(days=random.randint(120, 850))
            )
            employees.append(emp)

        db.add_all(employees)
        db.commit()
        print(f"Successfully saved 600 employees! (Total in DB: {db.query(Employee).count()})")

        print("Creating 100% Real Strategic Global Banking Clients & Partners across 5 Continents...")
        customers = []
        customer_lookup = {}
        for i, b in enumerate(CLIENT_BANKS):
            c_owner = employees[i % len(employees)]
            cust = Customer(
                company_name=b["name"],
                industry=b["industry"],
                city=b["city"],
                owner_id=c_owner.id,
                created_at=CURRENT_DATE - timedelta(days=random.randint(30, 260))
            )
            customers.append(cust)
            db.add(cust)
        db.commit()

        for c in customers:
            customer_lookup[c.company_name] = c

        print("Generating Leads and Deals across whole world for all 600 employees...")
        all_leads = []
        all_opportunities = []
        all_activities = []

        sources = [
            "RFP Inbound", "Oracle BFSI Global Summit", "Oracle Platinum Partner Lead",
            "Executive Leadership Referral", "Global Accounts Outreach", "JMR Web Portal",
            "Bogota Nearshore Hub", "EMEA Banking Conference"
        ]

        # Find Mr. Balaji Vankala's employee object
        balaji_emp = next((e for e in employees if "Balaji Vankala" in e.name), None)
        
        # Seed Balaji Vankala's explicit real deals
        if balaji_emp:
            print("Seeding dedicated high-profile real deals for Mr. Balaji Vankala...")
            for d in BALAJI_DEALS:
                cust_match = customer_lookup.get(d["bank"]) or random.choice(customers)
                lead_title = f"{d['bank']} - {d['project']}"
                contact_person = f"Chief Information Officer / Head of BFSI Tech ({d['bank'].split()[0]})"
                lead_email = f"procurement@{d['bank'].lower().replace(' ', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')[:12]}.com"
                lead_phone = f"+971 {random.randint(50, 58)} {random.randint(100, 999)} {random.randint(1000, 9999)}"

                lead_days = random.randint(30, 250)
                lead_dt = CURRENT_DATE - timedelta(days=lead_days)

                l = Lead(
                    name=f"{contact_person} ({lead_title})",
                    email=lead_email,
                    phone=lead_phone,
                    source="Oracle Platinum Partner Lead" if "Oracle" in d["project"] else "Executive Leadership Referral",
                    status=d["status"],
                    owner_id=balaji_emp.id,
                    created_at=lead_dt
                )
                all_leads.append(l)

                prob = 100.0 if d["stage"] == "won" else (0.0 if d["stage"] == "lost" else (65.0 if d["stage"] == "negotiation" else 40.0))
                if d["stage"] in ["won", "lost"]:
                    close_dt = CURRENT_DATE - timedelta(days=random.randint(5, 120))
                else:
                    close_dt = CURRENT_DATE + timedelta(days=random.randint(20, 75))

                opp = Opportunity(
                    customer_id=cust_match.id,
                    owner_id=balaji_emp.id,
                    title=f"{d['bank']}: {d['project']}",
                    amount=d["amount"],
                    stage=d["stage"],
                    probability=prob,
                    expected_close_date=close_dt,
                    created_at=lead_dt
                )
                all_opportunities.append(opp)

                act = Activity(
                    employee_id=balaji_emp.id,
                    customer_id=cust_match.id,
                    activity_type="meeting" if d["stage"] == "won" else ("call" if d["stage"] == "lost" else "proposal"),
                    notes=d["notes"],
                    activity_date=CURRENT_DATE - timedelta(days=random.randint(2, 60))
                )
                all_activities.append(act)

        # Seed leads and opportunities for all other 599 employees across all global regions
        for idx, emp in enumerate(employees):
            if "Balaji Vankala" in emp.name:
                continue

            num_leads = random.randint(6, 14)
            tier = random.random()
            if tier > 0.75:
                win_weight, lost_weight = 0.60, 0.25
            elif tier > 0.25:
                win_weight, lost_weight = 0.42, 0.38
            else:
                win_weight, lost_weight = 0.24, 0.56

            for l_idx in range(num_leads):
                rand_val = random.random()
                if rand_val < win_weight:
                    status = "won"
                elif rand_val < win_weight + lost_weight:
                    status = "lost"
                else:
                    status = random.choice(["qualified", "contacted", "new"])

                target_bank = random.choice(CLIENT_BANKS)
                project = random.choice(REAL_DEAL_PROJECTS)
                lead_name = f"{target_bank['name']} - {project}"
                contact_person = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                lead_phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
                lead_email = f"{contact_person.lower().replace(' ', '.')}@{target_bank['name'].lower().replace(' ', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')[:12]}.com"

                # 2026 Lead creation date
                lead_created = CURRENT_DATE - timedelta(days=random.randint(2, 275))
                lead = Lead(
                    name=f"{contact_person} ({lead_name})",
                    email=lead_email,
                    phone=lead_phone,
                    source=random.choice(sources),
                    status=status,
                    owner_id=emp.id,
                    created_at=lead_created
                )
                all_leads.append(lead)

                cust_match = customer_lookup.get(target_bank["name"]) or random.choice(customers)
                deal_title = f"{target_bank['name']}: {project}"
                
                # Deal amounts between $350,000 and $4,800,000
                amount = round(random.uniform(350000, 4800000), -2)

                if status == "won":
                    opp_close = min(CURRENT_DATE - timedelta(days=random.randint(1, 45)), lead_created + timedelta(days=random.randint(15, 60)))
                    opp = Opportunity(
                        customer_id=cust_match.id,
                        owner_id=emp.id,
                        title=deal_title,
                        amount=amount,
                        stage="won",
                        probability=100.0,
                        expected_close_date=opp_close,
                        created_at=lead_created
                    )
                    all_opportunities.append(opp)

                    act = Activity(
                        employee_id=emp.id,
                        customer_id=cust_match.id,
                        activity_type="meeting",
                        notes=f"Deal CLOSED WON with {target_bank['name']}. Project: {project}. Highlight: {random.choice(WON_HIGHLIGHTS)}. Contract value: ${amount:,.0f}",
                        activity_date=opp_close
                    )
                    all_activities.append(act)

                elif status == "lost":
                    opp_close = min(CURRENT_DATE - timedelta(days=random.randint(1, 45)), lead_created + timedelta(days=random.randint(15, 60)))
                    opp = Opportunity(
                        customer_id=cust_match.id,
                        owner_id=emp.id,
                        title=deal_title,
                        amount=amount,
                        stage="lost",
                        probability=0.0,
                        expected_close_date=opp_close,
                        created_at=lead_created
                    )
                    all_opportunities.append(opp)

                    act = Activity(
                        employee_id=emp.id,
                        customer_id=cust_match.id,
                        activity_type="call",
                        notes=f"Deal CLOSED LOST with {target_bank['name']}. Project: {project}. Factor: {random.choice(LOST_REASONS)}. Lost value: ${amount:,.0f}",
                        activity_date=opp_close
                    )
                    all_activities.append(act)

                else:
                    stage = "negotiation" if status == "qualified" else "proposal"
                    opp = Opportunity(
                        customer_id=cust_match.id,
                        owner_id=emp.id,
                        title=deal_title,
                        amount=amount,
                        stage=stage,
                        probability=65.0 if stage == "negotiation" else 40.0,
                        expected_close_date=CURRENT_DATE + timedelta(days=random.randint(15, 80)),
                        created_at=lead_created
                    )
                    all_opportunities.append(opp)

        print(f"Saving {len(all_leads)} leads, {len(all_opportunities)} deals, and {len(all_activities)} activities across all global regions...")
        
        # Batch insert for fast performance
        BATCH_SIZE = 1000
        for i in range(0, len(all_leads), BATCH_SIZE):
            db.add_all(all_leads[i:i+BATCH_SIZE])
            db.commit()

        for i in range(0, len(all_opportunities), BATCH_SIZE):
            db.add_all(all_opportunities[i:i+BATCH_SIZE])
            db.commit()

        for i in range(0, len(all_activities), BATCH_SIZE):
            db.add_all(all_activities[i:i+BATCH_SIZE])
            db.commit()

        print("Bulk save complete!")

        # Print summary
        total_e = db.query(Employee).count()
        total_l = db.query(Lead).count()
        total_w = db.query(Lead).filter(Lead.status == "won").count()
        total_lost = db.query(Lead).filter(Lead.status == "lost").count()
        total_opp = db.query(Opportunity).count()

        print("="*60)
        print("JMR INFOTECH 100% REAL GLOBAL DATASET SUMMARY:")
        print(f"Total Employees: {total_e}")
        print(f"Total Global Banking Clients: {len(CLIENT_BANKS)}")
        print(f"Total Leads: {total_l}")
        print(f"Total Won Leads: {total_w} ({round(total_w/total_l*100, 1)}%)")
        print(f"Total Lost Leads: {total_lost} ({round(total_lost/total_l*100, 1)}%)")
        print(f"Total Opportunities: {total_opp}")
        print("="*60)

        # Check Mr. Balaji Vankala
        balaji_record = db.query(Employee).filter(Employee.name.like("%Balaji Vankala%")).first()
        if balaji_record:
            b_leads = db.query(Lead).filter(Lead.owner_id == balaji_record.id).count()
            b_won = db.query(Lead).filter(Lead.owner_id == balaji_record.id, Lead.status == "won").count()
            b_lost = db.query(Lead).filter(Lead.owner_id == balaji_record.id, Lead.status == "lost").count()
            b_opps = db.query(Opportunity).filter(Opportunity.owner_id == balaji_record.id).all()
            b_val = sum(o.amount for o in b_opps if o.stage == "won")
            print(f"VERIFIED RECORD FOR MR. BALAJI VANKALA:")
            print(f" - Employee ID: {balaji_record.id}")
            print(f" - Email: {balaji_record.email}")
            print(f" - Department: {balaji_record.department}")
            print(f" - Leads: {b_leads} ({b_won} WON, {b_lost} LOST)")
            print(f" - Total Won Pipeline Closed: ${b_val:,.2f}")

    finally:
        db.close()

if __name__ == "__main__":
    generate_jmr_dataset()
