"""Email Notificaton code"""
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the email details - sender, subject
sender = 'compsci532@gmail.com'
subject = 'Flash Feed'

# Email HTML Template
html_template = """
<html>
<head>
    <style>
        body {{
          font-family: Arial, sans-serif;
          padding: 20px;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
      }}
        .content {{
          max-width: 600px;
          width: 100%;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          background-color: #ffffff;}}
        h2 {{ color: #2c3e50; }}
        h3 {{ color: #2980b9; }}
        p {{ color: #34495e; }}
        a {{ color: #e74c3c; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="content">
    <h2><center><b>Daily News Digest</center></b></h2>
    {articles}
    </div>
</body>
</html>
"""

def send_email(file_name: str, user_preferences_file : str):
  """Email sender function

  Args:
    file_name (str) : JSON file path containing the news articles data along with summary
    user_preferences_file (str) : JSON file path containing UserData
  """
  #Load the json data file 
  with open(file_name, 'r') as f:
    news_items = json.load(f)

  # Load the user preferences data file
  with open(user_preferences_file, 'r') as s:
    user_preferences_data = json.load(s)
  user_emails= [entry['email'] for entry in user_preferences_data]
  user_preferences= [entry['preferences'] for entry in  user_preferences_data]
  user_preferences[0].append('top') # Just in case there API isn't premium one

  # Retrieve Title , URL, SUMMARY based on user preferences
  number_of_users=len(user_emails)
  for i in range(number_of_users):
    articles_html = ''
    receiver= user_emails[i]

    for item in news_items:
      
      category= item.get('category','No category')
      if (category[0] in user_preferences[i]):
        title = item.get('title', 'No Title')
        url = item.get('link', '#')
        summary = item.get('summary', 'No Summary')
        articles_html += f"""
          <h3><a href="{url}">{title}</a></h3>
          <p>{summary}</p>
        """
    if articles_html:
        # Insert articles HTML into the template
        html = html_template.format(articles=articles_html)

        # Create the email message
        message = MIMEMultipart("alternative")
        msg = MIMEText(html, "html")
        message.attach(msg)
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receiver

        # Send the email using credentials 
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('compsci532@gmail.com', 'vcyh dkvd cujm qbmc')
            smtp.send_message(message)

if __name__ == "__main__":
    send_email("sample_data.json", "user_details.json")

