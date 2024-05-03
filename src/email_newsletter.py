import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(file_name: str) -> str:

  #Load the json data file 
  with open(file_name, 'r') as f:
    data = json.load(f)

  # Extract information from the JSON data
  news_items = data.get('results', [])
    
  # Set up the email details - sender, receiver 
  sender= 'compsci532@gmail.com'
  receiver = 'ppenta@umass.edu'
  subject = 'Flash Feed'

  #HTML Template
  html_template = """
  <html>
  <head>
      <style>
          body {{ font-family: Arial, sans-serif; }}
          h2 {{ color: #2c3e50; }}
          h3 {{ color: #2980b9; }}
          p {{ color: #34495e; }}
          a {{ color: #e74c3c; text-decoration: none; }}
          hr {{ border: 0; height: 1px; background: #ccc; }}
      </style>
  </head>
  <body>
      <h2><center>Daily News Digest</center></h2>
      <hr>
      {articles}
  </body>
  </html>
  """

  #Retrieve Title , URL, SUMMARY
  articles_html = ''
  for item in news_items:
      title = item.get('title', 'No Title')
      url = item.get('link', '#')
      content = item.get('content', 'No Content')
        
      articles_html += f"""
          <h3><a href="{url}">{title}</a></h3>
          <p>{content}</p>
          <hr>
      """
  # Insert articles HTML into the template
  html = html_template.format(articles=articles_html)

  # Create the email message
  message = MIMEMultipart("alternative")
  msg = MIMEText(html, "html")
  message.attach(msg)
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = receiver

  # Send the email using credentials 
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
      smtp.starttls()
      smtp.login('compsci532@gmail.com', 'vcyh dkvd cujm qbmc')
      smtp.send_message(msg)
      #print('Email sent!')


        
send_email("sample_data.json")

