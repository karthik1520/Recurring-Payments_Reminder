# 📬 Recurring Payments Reminder — Automated Monthly Email (Python)

This project sends a **beautiful, HTML-styled monthly reminder email** listing all your recurring payments—complete with:

- ✨ Positive Money Affirmations  
- 🧾 Clean bullet-style payment list  
- 💳 Due dates, amounts, notes  
- 💰 Total monthly outgoing  
- 🎨 Emojis & visually appealing formatting  

The script can run automatically every month using **Windows Task Scheduler**.

Perfect for maintaining financial awareness without stress.

---

## ✨ Features

- 🔔 **Automatic Monthly Email Reminder**
- 💌 **Beautiful HTML-formatted email** (affirmations + emojis)
- 📋 **Recurring payments list from JSON**
- 💳 **Due dates + notes + monthly totals**
- 🔐 **Secure credential handling via env file**
- 🧠 **Script loads files relative to itself** (safe for Task Scheduler)
- 🖥️ Can be extended into a **Windows GUI or cloud service**

---

## 📂 Project Structure

```text
Recurring-Payments-Reminder/
│
├── reminder.py         # Main Python script (email builder + sender)
├── payments.json       # Recurring payments (editable)
├── config.env          # Email credentials (NOT tracked by Git)
├── .gitignore          # Ensures config.env is not committed
└── README.md           # Documentation
🧾 Example payments.json (Your Real Data)
json
Copy code
[
  {
    "name": "Apple Storage",
    "amount": 10,
    "currency": "EUR",
    "day": 27,
    "notes": "iCloud monthly storage subscription"
  },
  {
    "name": "Adobe Creative Cloud",
    "amount": 25,
    "currency": "EUR",
    "day": 24,
    "notes": "Creative Cloud monthly subscription"
  },
  {
    "name": "Mutual Fund",
    "amount": 60,
    "currency": "EUR",
    "day": 2,
    "notes": "Monthly SIP contribution"
  },
  {
    "name": "Gold + Education Loan",
    "amount": 390,
    "currency": "EUR",
    "day": 2,
    "notes": "Loan + gold saving scheme combined payment"
  },
  {
    "name": "ChatGPT Plus",
    "amount": 23,
    "currency": "EUR",
    "day": 8,
    "notes": "Subscription fee"
  }
]
🔐 Configuration — config.env
Create a file named config.env:

text
Copy code
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
TO_EMAIL=your_email@gmail.com
⚠️ Never commit this file.
It is automatically ignored via .gitignore.

Creating a Gmail App Password
Go to Google Account → Security

Enable 2-Step Verification

Go to App Passwords → choose Mail

Copy the generated App Password into config.env as EMAIL_PASSWORD

▶️ Run the Script Manually
Make sure you're inside your project folder, then run:

bash
Copy code
python reminder.py
You should receive an HTML email with:

✨ Affirmations

💳 Your payment list

💰 Total monthly amount

🎨 Emojis

🖥️ Automating with Windows Task Scheduler
Open Task Scheduler

Create Basic Task → Trigger: Monthly

Set Program/script to:

text
Copy code
"C:\Path\To\Python\python.exe"
Set Add arguments to:

text
Copy code
"C:\Path\To\Recurring-Payments-Reminder\reminder.py"
Start in: (leave empty)

Save → Right-click task → Run

Check your email 🎉

The script works from Task Scheduler because it loads files relative to its own directory using __file__.

🔧 How It Works (Technical Overview)
Email formatting is done using HTML + inline CSS

Script pulls payments from payments.json

Builds affirmations + bullet list dynamically

Calculates total outgoing

Sends email using Gmail SMTP (smtplib + SSL)

File paths are resolved via:

python
Copy code
base_dir = os.path.dirname(os.path.abspath(__file__))
so Task Scheduler can’t break it by changing the working directory.

🚀 Future Enhancements
🪟 Full Windows Desktop App (Tkinter / PyQt)

☁️ Cloud Scheduler (Google/AWS) — run even when PC is off

📊 Expense dashboard UI

🔔 Push / Telegram / WhatsApp notifications

🔐 Encrypted password storage