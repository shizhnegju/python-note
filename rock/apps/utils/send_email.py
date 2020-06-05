import smtplib

# Import the email modules
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template, render_to_string


def send_email(to, sender='Tools Notice<tools_notice@za.group>', cc="", bcc=None, subject="", template="default",
               data="", zip_file_path="", file_list=None):
    server = smtplib.SMTP('172.16.6.14', 25)

    # Next, log in to the server
    server.login("tools_notice@za.group", "iyR2LqjSQUlhr6rI")

    # Send the mail
    if type(to) is not list:
        to = to.split()
    if type(cc) is not list:
        cc = cc.split()
    to_list = to + cc
    # print(to_list)
    to_list = list(filter(None, to_list))  # remove null emails
    # print(to_list)
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['Subject'] = subject
    msg['To'] = ','.join(to)
    msg['Cc'] = ','.join(cc)
    msg['Bcc'] = bcc
    if zip_file_path:
        zipApart = MIMEApplication(open(zip_file_path, 'rb').read())
        zipApart.add_header('Content-Disposition', 'attachment', filename=zip_file_path.split("/")[-1])
        msg.attach(zipApart)
    if file_list:
        for file in file_list:
            file_att = MIMEApplication(open(file, 'rb').read())
            file_att.add_header("Content-Disposition", "attachment", filename=file.split("/")[-1])
            msg.attach(file_att)
    # msg.attach(MIMEText(body, 'html'))
    html_content = render_to_string("{}.html".format(template), data)
    msg.attach(MIMEText(html_content, "html"))
    try:
        server.sendmail(sender, to_list, msg.as_string())
    except Exception as e:
        raise ValueError("邮件发送失败，", str(e))
    finally:
        server.quit()
