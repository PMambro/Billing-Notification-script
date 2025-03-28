import os
import smtplib
import requests
import json
from datetime import datetime
from calendario import mes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Config variables
sheet_id = "1FJOimQV0qHXdD76HGpDSqUsQhh80v-fikERzcGCCkWE"                # ID of the google sheets you are going to insert the data into
sheet_id_test = "14AiRvaYRDmols7VXmKY7VE_Zq3fM631lIPopst0Iowg"           # Just another ID
sheet_range = "Página1!A1:F100"                                              # Defines the range of the sheet
iof = 1.0338
bill_value_usd = 20.00

# Get the PTAX exchange rate from the Banco Central 
def fetch_ptax_rate():
    from datetime import date, timedelta

    today = date.today()
    start_date = (today - timedelta(days=7)).strftime("%m-%d-%Y")
    end_date = today.strftime("%m-%d-%Y")

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
        f"@dataInicial='{start_date}'&@dataFinalCotacao='{end_date}'"
        "&$top=1&$orderby=dataHoraCotacao desc&$format=json"
    )

    response = requests.get(url)
    data = response.json()

    if not data['value']:
        raise Exception("No PTAX rate found in the last 7 days.")

    ptax = float(data['value'][0]['cotacaoVenda'])
    return ptax * 1.04  # Apply 4% spread


 google-sheet-branch
# Send the email with the billing info converted to R$

# Send the email with the billing info converted to R$
 main
def send_email(subject, html_path, date, rate, usd, brl, bill, pix):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASSWORD']
    receivers = os.environ['EMAIL_TO'].split(',')
    host = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('EMAIL_PORT', 587))

    msg = MIMEMultipart("alternative")
    msg['from'] = sender
    msg['to'] = ','.join(receivers)
    msg['subject'] = subject

    text = "Your email client does not support"

    with open(html_path, "r", encoding="utf-8") as f:
        html_template = f.read()
        html = html_template.format(date=date, rate=rate, usd=usd, brl=brl, bill=bill, pix=pix)
    
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

# Write the billing info in a Google Sheet
def write_to_google_sheet(month, usd_value, rate, brl_value, iof, bill):
    creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = Credentials.from_service_account_info(creds_json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build('sheets', 'v4', credentials=creds)

    values = [[month, usd_value, rate, brl_value, iof, bill]]
    body = {"values": values}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id_test,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()


def main():
    date = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    month = mes[datetime.now().month]
    year = datetime.now().year
    rate = fetch_ptax_rate()
    bill_value_brl = round(bill_value_usd * rate, 2)
    bill_value_per_person = round(bill_value_brl * iof / 4, 2)
    pix_key = os.environ['PIX_KEY']


    service = os.environ['SERVICE']

    '''body = f"Data da cobrança: {date}. \nCotação PTAX (Banco Central) + 4% de spread: {rate:.4f}.\nMensalidade: US$ {bill_value_usd}.\
          \nMensalidade convertida em Reais: R${bill_value_brl} \nIOF: 3.38% sobre o valor total da transação \
          \nValor a ser pago: R${bill_value_per_person} \nChave pix: {pix_key}"
    print(body)'''

 google-sheet-branch
    send_email(f"Mensalidade {service} {month} de {year}", "email_template.html", date, rate, bill_value_usd, bill_value_brl, bill_value_per_person, pix_key)
    write_to_google_sheet(month, bill_value_usd, round(rate, 4), bill_value_brl, iof, bill_value_per_person)

    print('Riiight')

    send_email(f"Mensalidade {service} {month} de {year}", "email_template.html", date, rate, bill_value_usd, bill_value_brl, bill_value_per_person, pix_key)
    write_to_google_sheet(month, bill_value_usd, round(rate, 4), bill_value_brl, iof, bill_value_per_person)

    print('Riiight')
 main

if __name__ == "__main__":
    main()


