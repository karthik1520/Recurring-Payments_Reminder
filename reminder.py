import json
import smtplib
import ssl
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Load environment variables from config.env (next to this script)
def load_config(filename="config.env"):
    # Folder where reminder.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"{full_path} not found")

    config = {}
    with open(full_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


# 2. Load recurring payments from JSON file (next to this script)
def load_payments(filename="payments.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"{full_path} not found")

    with open(full_path, "r") as f:
        return json.load(f)

# 3. Filter payments by month start (for now, just return all)
def get_monthly_payments(payments):
    # In future, you can filter by date range (e.g., only payments within first 10 days).
    return payments

# 4. Build the email body text
def build_email_body(payments):
    # Start HTML email
    parts = []

    parts.append("""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        <h2 style="margin-bottom: 4px;">✨ Monthly Money Check-In</h2>
        <p style="margin-top: 0;">Hi,</p>
        <p>
          Money flows to me in expected and unexpected ways 💸.<br>
          I manage it wisely, and every payment I make keeps my life running smoothly,
          supports my goals, and creates more space for abundance in my future 🌱.
        </p>
    """)

    if not payments:
        parts.append("""
        <p>You currently have no recurring payments configured.</p>
        <p>
          I am grateful that my finances are simple and easy to manage right now 🙏.
        </p>
        <p>
          Every month, my relationship with money becomes calmer, clearer, and more abundant ✨.
        </p>
      </body>
    </html>
        """)
        return "".join(parts)

    # We have payments
    parts.append("""
        <h3 style="margin-bottom: 4px;">📋 My recurring payments for this month</h3>
        <ul style="padding-left: 20px; margin-top: 8px;">
    """)

    total = 0.0
    first_currency = payments[0].get("currency", "").strip()

    for p in payments:
        name = p["name"]
        amount = float(p["amount"])
        currency = p.get("currency", "").strip()
        day = p["day"]
        notes = p.get("notes", "")

        total += amount

        # Build each bullet point with a little gap (margin-bottom)
        line = f"💳 <strong>{name}</strong> – {amount:.2f}"
        if currency:
            line += f" {currency}"
        line += f" – due on day <strong>{day}</strong>"

        if notes:
            line += f" <em>({notes})</em>"

        parts.append(f"""
          <li style="margin-bottom: 10px;">
            {line}
          </li>
        """)

    parts.append("</ul>")

    # Total + closing affirmations
    if first_currency:
        parts.append(f"""
        <p style="margin-top: 12px;">
          💰 <strong>Total for these payments:</strong> {total:.2f} {first_currency}
        </p>
        """)
    else:
        parts.append(f"""
        <p style="margin-top: 12px;">
          💰 <strong>Total for these payments:</strong> {total:.2f}
        </p>
        """)

    parts.append("""
        <p>
          I choose to pay these consciously and feel grateful that I can cover them 🙌.<br>
          Every month, my relationship with money becomes calmer, clearer, and more abundant ✨.
        </p>
        <p style="margin-top: 12px;">
          With clarity and abundance,<br>
          <strong>Future Me</strong> 💫
        </p>
      </body>
    </html>
    """)

    return "".join(parts)



# 5. Send the email using Gmail SMTP
def send_email(config, subject, body):
    email_address = config["EMAIL_ADDRESS"]
    email_password = config["EMAIL_PASSWORD"]
    to_email = config["TO_EMAIL"]

    msg = MIMEMultipart()
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    # Gmail SMTP server details
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

# 6. Main function that ties everything together
def main():
    # Get current date info
    today = datetime.now()
    month_name = today.strftime("%B")  # e.g. "March"
    year = today.year

    # Load config and payments
    config = load_config()
    payments = load_payments()

    # Decide which payments to include (for now: all)
    monthly_payments = get_monthly_payments(payments)

    # Build email content
    subject = f"Monthly Payments Reminder – {month_name} {year}"
    body = build_email_body(monthly_payments)

    # Send the email
    send_email(config, subject, body)
    print("Reminder email sent!")

if __name__ == "__main__":
    main()
