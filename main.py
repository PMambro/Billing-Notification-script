import os
import smtplib
import requests
import json
from datetime import datetime
from calendario import mes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
'''from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build'''
from dotenv import load_dotenv

load_dotenv()

# Config variables
sheet_id = "google_sheet_id"
sheet_range = "Sheet1!A1"
iof = 1.0338
bill_value_usd = 20.00

# Get the exchange rate through the awesomeAPI
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


# Send the email with the R$value converted to US$
def send_email(subject, body):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASSWORD']
    receivers = os.environ['EMAIL_TO'].split(',')
    host = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('EMAIL_PORT', 587))

    msg = MIMEMultipart()
    msg['from'] = sender
    msg['to'] = ','.join(receivers)
    msg['subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())



def main():
    date = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    month = datetime.now().month
    year = datetime.now().year
    rate = fetch_ptax_rate()
    bill_value_brl = round(bill_value_usd * rate, 2)
    bill_value_per_person = round(bill_value_brl * iof / 4, 2)
    pix_key = os.environ['PIX_KEY']


    service = os.environ['SERVICE']

    body = f"Data da cobrança: {date}. \nCotação PTAX (Banco Central) + 4% de spread: {rate:.4f}.\nMensalidade: US$ {bill_value_usd}.\
          \nMensalidade convertida em Reais: {bill_value_brl} \nIOF: 3.38% sobre o valor total da transação \
          \nValor a ser pago: {bill_value_per_person} \nChave pix: {pix_key}"
    print(body)

    send_email(f"Mensalidade {service} {mes[month]} de {year}", body)

if __name__ == "__main__":
    main()


