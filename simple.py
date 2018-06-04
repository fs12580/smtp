#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter13/simple.py

import sys, smtplib, email.message, email.policy, email.utils, socket, ssl

text = """Hello,
This is a test message from Chapter 1a3
选择性使用TLS
 - Anonymous"""


def main():

    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("usage: {} server fromaddr toaddr [toaddr...]".format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    password = "cqxxhs1997" #163邮箱授权密码
    
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = "260042229@qq.com"
    message['From'] = "15277141174@163.com"
    message['Subject'] = 'Test Message, Chapter 13'
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()
    message.set_content(text)

    try:
        connection = smtplib.SMTP(server, 25)
        connection.login(fromaddr, password)#登录
        send_message_securely(connection, fromaddr, toaddrs, message)
       # report_on_message_size(connection, fromaddr, toaddrs, message)
       #connection.sendmail(fromaddr, toaddrs, str(message))
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException)as e:
        print("your message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print("Message sent to {} recipient{}".format(len(toaddrs), s))
        connection.quit()


def send_message_securely(connection, fromaddr, toaddrs, message):
    code = connection.ehlo()[0]
    uses_esmtp = (200 <= code <= 299)
    if not uses_esmtp:
        code = connection.helo()[0]
        if not (200<= code <= 299):
            print("Remote server refused HELO; code:", code)
            sys.exit(1)
    
    if uses_esmtp and connection.has_extn('starttls'):
        print("Negotiating TLS....")
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.set_default_verify_paths()
        context.verify_mode = ssl.CERT_REQUIRED
        connection.starttls(context=context)
        code = connection.ehlo()[0]
        if not (200 <= code <= 299):
            print("Couldn't EHLO after STARTTLS")
            sys.exit(5)
        print("Using TLS connection.")
    else :
        print("Server does not support TLS; using normal connection.")

    connection.sendmail(fromaddr, toaddrs, str(message))
if __name__ == '__main__':
    main()

