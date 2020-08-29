import os
import smtplib
import traceback
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtpd import COMMASPACE

import settings

default_server = {
    "host": settings.MAIL_SERVER_HOST,
    'user_name': settings.MAIL_SERVER_USER,
    'password': settings.MAIL_SERVER_PASSWORD
}


def send_mail(mail_server=default_server, mail_from=None, mail_subject=u'', mail_to=[],
              mail_content='', mail_content_images=None, mail_attachments=None):
    """
    发送电子邮件
    :param mail_server: 邮件服务器配置
    :param mail_subject: 邮件主题
    :param mail_from: 发送邮箱地址
    :param mail_to: 目标邮箱地址
    :param mail_content: 邮件内容
    :param mail_content_images: 邮件内容的图片附件 {'Content-ID':'image_path'}
    :param mail_attachments: 邮件附件
    :return:
    """
    try:
        if not mail_from:
            mail_from = default_server['user_name']
        else:
            mail_from += f" <{mail_server['user_name']}>"
        if not mail_to:
            mail_to = settings.mail_to
        mail_mime = MIMEMultipart()
        # 邮件信息
        mail_mime['From'] = mail_from
        mail_mime['To'] = COMMASPACE.join(mail_to)
        mail_mime['Subject'] = Header(mail_subject, 'utf-8')
        mail_mime['Date'] = formatdate(localtime=True)
        # 邮件内容
        html_content = MIMEText(mail_content, 'html', 'utf-8')
        mail_mime.attach(html_content)
        # 邮件内容图片
        if isinstance(mail_content_images, dict):
            for content_id in mail_content_images.keys():
                try:
                    image_path = mail_content_images.get(content_id)
                    if image_path:
                        image = open(image_path, 'rb')
                        image_mime = MIMEImage(image.read())
                        image_mime.add_header('Content-ID', content_id)
                        image.close()
                        mail_mime.attach(image_mime)
                except Exception:
                    pass
        # 邮件附件
        if isinstance(mail_attachments, list):
            for attachment in mail_attachments:
                try:
                    a_mime = MIMEBase('application', 'octet-stream')
                    a_file = open(attachment, 'rb')
                    a_mime.set_payload(open(a_file.read()))
                    # Base64加密成字符串
                    encoders.encode_base64(a_mime)
                    a_mime.add_header('Content-Disposition',
                                      'attachment; filename="%s"' % os.path.basename(attachment))
                    mail_mime.attach(a_mime)
                except Exception:
                    pass
        try:
            smtp = smtplib.SMTP_SSL(mail_server['host'])
            smtp.ehlo()
            smtp.login(mail_server['user_name'], mail_server['password'])
            smtp.sendmail(mail_from, mail_to, mail_mime.as_string())
        except Exception:
            print(traceback.format_exc())
        smtp.close()
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    send_mail(mail_subject=u'test', mail_to=settings.mail_to, mail_content='test content', )
