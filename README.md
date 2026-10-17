# 🛡️ ScamShield AI — Intelligent Cyber Scam Detection & Digital Safety Platform

> **A professional, offline-first cybersecurity web application built for HYPNEXIS ’26 at Manipal University Jaipur.**  
> Analyzes suspicious URLs, SMS, WhatsApp messages, fake job offers, phishing campaigns, APK scams, and UPI reverse-payment traps to protect students, senior citizens, online shoppers, and digital payment users across India.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Hackathon](https://img.shields.io/badge/Hackathon-HYPNEXIS%20’26%20MUJ-cyan.svg)]()
[![Status](https://img.shields.io/badge/Build-46%2F46%20Tests%20Passing-brightgreen.svg)]()

---

## 1. Project Overview & Mission

In 2024 alone, Indian citizens lost over **₹7,000 Crores** to cyber financial crimes and digital extortion. Traditional English spam filters and generic antivirus tools fail because cybercriminals in India exploit:
- **Colloquial Hinglish social engineering:** *"Aapka bijli connection aaj raat 9:30 baje kat diya jayega"*
- **UPI reverse-payment traps:** *"Scan this QR code and enter UPI PIN to receive cashback"*
- **Fake authority coercion:** *"You are under Digital Arrest by CBI Cyber Crime Cell for an illegal narcotics parcel"*
- **Pre-paid Telegram tasks:** *"Work from home, earn Rs. 5,000 daily by liking YouTube videos"*
- **Lookalike banking domains:** `http://sbi-kyc-verification-portal.xyz/login`

**ScamShield AI** bridges this critical defense gap. It delivers a fast, transparent, and **100% offline-first heuristic rule engine** that identifies suspicious indicators, calculates a balanced risk score (0-100), highlights dangerous phrases in real-time, and recommends concrete next steps without requiring paid external APIs.

---

## 2. Technology Stack

* **Frontend:** HTML5, CSS3 (Cyber Dark Navy Theme with Neon Green `#00ff88` & Electric Blue `#00e5ff` accents), Vanilla JavaScript
* **Backend:** Python 3.10+ with [Flask](https://flask.palletsprojects.com/)
* **Database:** SQLite with parameterized SQL, deduplication hashing, and automatic PII masking
* **Detection Engine:** Python-based rule engine with modular architecture (`detection/scanner.py`)
* **Zero Paid API Requirement:** Works locally without an API key or internet connection
* **Testing:** Python `unittest` test suite with 46 automated test cases

---

## 3. Project Structure

```
StudySaathiAI/ (ScamShield AI)
├── app.py                     # Main Flask web application & REST API routes
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive setup & architecture documentation
├── config.py                  # Environment & Flask app configuration
├── scamshield.db              # Local SQLite database
├── seed_data.py               # Database seeder for sample audit records & quizzes
│
├── detection/                 # Detection engine package
│   ├── __init__.py            # Package initialization and exports
│   └── scanner.py             # URLScanner, MessageScanner, AIExplainer, detect_scam()
│
├── database/                  # Persistence layer package
│   ├── __init__.py            # Package initialization and exports
│   └── db.py                  # SQLite initialization, parameterized CRUD, PII masking
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Master layout with cyber sidebar, header, and pitch modal
│   ├── index.html             # Home / Dashboard with embedded live Scam Scanner
│   ├── dashboard.html         # Cybersecurity telemetry & Chart.js visualizations
│   ├── scanner.html           # Dedicated URL threat inspector
│   ├── analyzer.html          # Deep-dive multilingual message & Hinglish analyzer
│   ├── result.html            # Individual audit report viewer
│   ├── history.html           # Scan audit history with search, filter, and CSV/JSON export
│   ├── reports.html           # Community Scam Radar with deduplication & upvoting
│   ├── learn.html             # Safety Education & 6 Scam Vectors Encyclopedia + Quizzes
│   ├── about.html             # Project mission for HYPNEXIS ’26, architecture & ethics
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css          # Cyber dark navy theme, radar animations, risk meters
│   └── js/
│       ├── app.js             # Global navigation, toast alerts, clipboard helpers
│       ├── scanner.js         # Dedicated URL scanner interactions
│       ├── analyzer.js        # Dedicated message analyzer interactions
│       ├── dashboard.js       # Chart.js telemetry charts & metric counters
│       └── quiz.js            # Interactive cyber quiz engine
│
└── tests/                     # Automated unit test suite (46 tests)
    ├── __init__.py
    ├── test_scanner.py        # Detection engine unit tests (URLs, messages, scoring)
    ├── test_detector.py       # Heuristic regression tests
    └── test_api.py            # Flask REST API endpoints & CRUD tests
```

---

## 4. Beginner-Friendly Windows 11 Setup Guide (VS Code)

Follow these step-by-step instructions in the Visual Studio Code terminal on Windows 11.

### Step 1: Install Python (If Not Already Installed)
1. Download Python 3.10+ from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **Crucial:** During installation, check the box that says **"Add Python to PATH"**.
3. Open PowerShell or Windows Terminal and verify:
   ```powershell
   python --version
   ```

### Step 2: Open the Project Folder in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File ➔ Open Folder...** and select:
   `c:\Users\rajsh\Downloads\StudySaathiAI`
3. Open an integrated PowerShell terminal in VS Code:
   Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick) or go to **Terminal ➔ New Terminal**.

### Step 3: Create and Activate a Virtual Environment
In the VS Code terminal, execute:
```powershell
python -m venv venv
```
Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```
> **Tip for Windows 11:** If you see `Execution of scripts is disabled on this system`, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\venv\Scripts\Activate.ps1
> ```
Once activated, your terminal prompt will show `(venv)`.

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run the Automated Unit Tests
Verify that all 46 unit tests pass before launching:
```powershell
python -m unittest discover tests
```
Expected output:
```
..............................................
Ran 46 tests in 0.366s
OK
```

### Step 6: Start the Flask Application
```powershell
python app.py
```
Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 7: Open the Local Website in Your Browser
Open your preferred browser (Chrome, Edge, Firefox) and navigate to:  
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 5. Troubleshooting Common Windows Errors

| Error Symptom | Cause | Solution |
|---|---|---|
| `python : The term 'python' is not recognized` | Python is not added to the system PATH | Re-run Python installer, choose "Modify", and check "Add Python to environment variables". |
| `cannot be loaded because running scripts is disabled` | PowerShell ExecutionPolicy default restriction | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate `venv`. |
| `Address already in use: 5000` | Another process is occupying port 5000 | In PowerShell, find and kill the process: `Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess \| Stop-Process -Force` or edit `.env` to change `PORT=5001`. |
| `OperationalError: database is locked` | An active SQLite transaction did not close | Close any external SQLite viewer GUI and restart `python app.py`. |
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment is not active or dependencies missing | Run `.\venv\Scripts\Activate.ps1` and run `pip install -r requirements.txt`. |

---

## 6. How the Detection Engine Works

### URL Threat Inspection (`URLScanner`)
1. **Scheme Verification:** Evaluates HTTPS vs unencrypted HTTP (weighted as a weak indicator, not proof of scam) and blocks executable protocols (`javascript:`, `data:`).
2. **Raw IP Host Phishing:** Detects numerical IPv4 hosts (`http://192.168.1.100/...`), commonly used in transient phishing setups.
3. **URL Shorteners:** Identifies redirect masking via `bit.ly`, `tinyurl.com`, `t.co`, `cutt.ly`, etc.
4. **Disposable Phishing TLDs:** Flags 25+ high-risk TLDs (.xyz, .top, .icu, .buzz, .rest) frequently registered for cheap throwaway campaigns.
5. **Brand Typosquatting:** Computes Levenshtein edit distance and brand substring matches against 40+ Indian brands (SBI, HDFC, ICICI, Paytm, India Post, Income Tax, UIDAI).
6. **Shannon Entropy:** Measures lexical randomness to detect automated Domain Generation Algorithms (DGAs).
7. **Obfuscation Detection:** Flags `@` characters in URLs, multiple hyphens, and Punycode (`xn--`) homoglyphs.

### Message & Hinglish NLP Analysis (`MessageScanner`)
1. **Credential & OTP Demands:** Flags demands for OTPs, UPI PINs, CVV, NetBanking passwords in English, Hindi (ओटीपी, पिन), and Hinglish (*"OTP share kare"*, *"PIN enter kare"*).
2. **Defensive Negation Check:** Contextual window parsing ensures legitimate security alerts (*"Do not share your OTP with anyone"*) are NOT falsely flagged as scams.
3. **Urgent Utility Cutoffs:** Identifies fake electricity power disconnection threats (*"Aapka bijli connection aaj raat 9:30 baje kat diya jayega"*).
4. **Digital Arrest Extortion:** Detects illegal parcel extortion claims using CBI, Customs, Police, and Skype interrogation threats.
5. **Prepaid WFH Job Scams:** Detects Telegram task lures (*"Earn 5000 daily by liking YouTube videos"*).
6. **UPI Reverse PIN Traps:** Flags deceptive *"Scan this QR to receive cashback"* tactics.
7. **Remote Control & APK Threats:** Flags requests to install AnyDesk, QuickSupport, TeamViewer, or sideload unknown `.apk` packages.
8. **Direct Mobile Sender Callouts:** Detects individual 10-digit mobile numbers embedded in alerts directing victims to contact personal cell phones instead of verified bank IVRs.

---

## 7. REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/scan` | Unified detection endpoint for URLs, SMS, WhatsApp messages (supports auto-detection) |
| `POST` | `/api/scan/url` | Dedicated URL lexical scanner |
| `POST` | `/api/scan/message` | Dedicated message NLP analyzer with span offset highlighting |
| `GET` | `/api/samples` | Returns curated test demonstration samples |
| `GET` | `/api/stats` | Aggregated dashboard telemetry (total scans, threats, risk distribution) |
| `GET` | `/api/history` (or `/api/scans`) | Scan history audit log with search, type, and risk filters |
| `POST` | `/api/history/clear` | Clears all stored scan logs from SQLite |
| `POST` | `/api/reports` | Submits crowdsourced scam reports with SHA-256 deduplication |
| `POST` | `/api/reports/<id>/upvote` | Increments community confirmation votes |

---

## 8. Hackathon 2-Minute Presentation Pitch Script

> **Judge Hook (0:00 - 0:25):**  
> *"Judges, in the last 24 hours alone, thousands of Indian citizens received this message on WhatsApp: 'Dear Consumer, Aapka bijli connection aaj raat 9:30 baje kat diya jayega. Call officer Rahul 9876543210.' Panic strikes, they call the number, download an APK, and lose their life savings. Traditional English antivirus filters completely miss this. We built ScamShield AI for HYPNEXIS ’26 to solve this crisis."*

> **Live Demo 1: URL Scanner (0:25 - 0:55):**  
> *"Let's test this URL: `http://sbi-kyc-verification-portal.xyz/login`. Within 50 milliseconds, ScamShield AI decomposes the URL. Notice: Zero unsafe remote requests or SSRF risk. It detects: (1) Unencrypted HTTP, (2) High-risk disposable `.xyz` TLD, and (3) Spoofed State Bank of India brand using Levenshtein distance. Result: 94/100 High Risk with clear safety steps."*

> **Live Demo 2: Message Analyzer (0:55 - 1:25):**  
> *"Now let's test the electricity scam SMS in Hinglish. ScamShield AI's multilingual NLP identifies the coercion, highlights the exact threatening text span in red, detects the individual 10-digit mobile number, and reminds the user: 'Electricity boards never authorize disconnections via personal WhatsApp messages.' And if an SMS says 'Never share your OTP', our engine recognizes it as defensive advice and doesn't falsely flag it."*

> **Community Impact & Incident Response (1:25 - 1:50):**  
> *"Our platform features a live Community Radar with SHA-256 deduplication, a Scam Academy quiz that trains users through real-world scenarios, and direct integration with India's National Cyber Helpline **1930** and **cybercrime.gov.in**."*

> **Closing (1:50 - 2:00):**  
> *"ScamShield AI is lightweight, 100% offline-ready, privacy-first, and requires zero paid APIs. Thank you!"*

---

## 9. Ethics, Limitations & Official Helplines

1. **Probabilistic Heuristics:** ScamShield AI provides automated heuristic estimations. A low risk score indicates no known red flags were matched; it does not constitute an absolute warranty.
2. **Privacy First:** ScamShield AI never collects or stores passwords, OTPs, or bank card credentials. All phone numbers and emails are masked prior to database storage.
3. **Emergency Cyber Fraud Helpline:** If you or someone you know has been defrauded:
   - 📞 **Dial 1930** (Citizen Financial Cyber Fraud Reporting System) immediately within the 'Golden Hour' to freeze fraudulent transactions.
   - 🌐 **File an official complaint:** [https://cybercrime.gov.in](https://cybercrime.gov.in)

---

## 10. Contributors & License

Developed with ❤️ for **HYPNEXIS ’26 at Manipal University Jaipur**.  
Licensed under the **MIT License**.
