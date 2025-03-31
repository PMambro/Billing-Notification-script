# Monthly R$ to US$ Tracker 🏦💸

This Python script fetches the official **PTAX exchange rate** from Banco Central do Brasil, adds a 4% spread, converts a fixed BRL amount to USD, stores the result in a **Google Sheet**, and sends an **email notification** with the details.

It runs automatically every month using **GitHub Actions**, without requiring a server or local machine to stay on.

---

## 🧠 What It Does
- 📥 Fetches the latest **PTAX (BCB)** BRL → USD rate
- ➕ Applies a **4% spread** to simulate commercial exchange rates
- 💱 Converts a fixed value in USD (editable in the script)
- 📊 Logs date, USD amount, BRL result in **Google Sheets**
- 📩 Sends an **email** with the result to a list of addresses
- 🔁 Runs **automatically on the 26th of every month** via GitHub Actions

---

## 📂 Files
- `main.py`: The main script that does everything
- `.github/workflows/monthly.yml`: GitHub Actions workflow

---

## 🔐 Required GitHub Secrets
Go to your GitHub repo → Settings → Secrets → Actions → Add the following:

| Secret Name         | Description                              |
|---------------------|------------------------------------------|
| `EMAIL_USER`        | Your Gmail address                       |
| `EMAIL_PASS`        | Your Gmail **App Password** (no spaces)  |
| `EMAIL_TO`          | Comma-separated emails                   |
| `EMAIL_HOST`        | `smtp.gmail.com`                         |
| `EMAIL_PORT`        | `587`                                    |
| `GOOGLE_CREDENTIALS`| JSON string of your Google Sheets API key |

---

## 📅 Cron Schedule
This line in `monthly.yml`:
```yaml
cron: '0 17 26 * *'
```
Means the script runs:
- **17:00 UTC on the 1st of each month**
- That’s **14:00 Brasília time** (adjust if needed)

To test manually, go to **Actions > Run workflow**.

---

## ✏️ Customization
- To change the US$ value, edit `bill_value_usd` in `main.py`
- To change spreadsheet range or layout, edit the `sheet_range`

---

## 💌 Example Output (email & sheet)
```
On 2025-04-01 11:00:00, R$ 1000.00 = US$ 192.31 (Rate: 5.2000)
```

