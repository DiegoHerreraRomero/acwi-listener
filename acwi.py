import datetime
import csv
import requests
import smtplib, ssl

#email credentials
username = ""
password = ""

#date range
today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
five_days = today - datetime.timedelta(days=5)
range_end = int(today.timestamp())
range_start = int(five_days.timestamp())

#read csv
before_day = ""
after_day = ""
before_value = 0
after_value = 0
url = "https://query1.finance.yahoo.com/v7/finance/download/ACWI?period1="+str(range_start)+"&period2="+str(range_end)+"&interval=1d&events=history&includeAdjustedClose=true"
with requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}) as r:
  lines = (line.decode('utf-8') for line in r.iter_lines())
  csv = csv.reader(lines)
  next(csv, None)
  for line in csv:
    before_day = after_day
    before_value = after_value
    after_day = line[0]
    after_value = round(float(line[4]),2)

#validate amounts and send email
down = round((after_value - before_value),2)
if down < 0:
  print("Alerta caída: "+str(down));

  day_1 = before_day+": "+str(before_value)
  day_2 = after_day+": "+str(after_value)
  message = """Subject: ALERTA CAÍDA DE INVERSIÓN


  Hola, el fondo de inversión ACWI ha tenido una caída de {down}%, 
  por favor revisa en la página https://finance.yahoo.com/quote/ACWI/chart?p=ACWI para confirmar la información.

  {day_1}
  {day_2}""".format(down=str(down), day_1=day_1, day_2=day_2)


  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login(username, password)
    server.sendmail(username, username, message.encode('utf-8'))