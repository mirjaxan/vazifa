import random,string

from django.core.mail import EmailMultiAlternatives,send_mail
from config.settings import DEFAULT_FROM_EMAIL
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import re


def send_code(email:str, code:str):

	subject="Vertification codes",
	html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>X Security</title>
</head>
<body style="margin:0; padding:0; background:#000; font-family:Arial, Helvetica, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center">

<table width="600" style="background:#000; margin-top:40px; border-radius:12px; border:1px solid #1d1f23;">
    
    <!-- Header -->
    <tr>
        <td style="padding:30px; text-align:center; border-bottom:1px solid #1d1f23;">
            <h1 style="color:white; margin:0; font-size:28px;">𝕏</h1>
            <p style="margin:6px 0 0; color:#1d9bf0; font-size:14px;">Security Notification</p>
        </td>
    </tr>

    <!-- Body -->
    <tr>
        <td style="padding:40px;">
            <h2 style="color:white; font-size:22px;">Hello User</h2>

            <p style="color:#aaa; font-size:15px; line-height:1.6;">
                We received a request to access your X account.  
                Use the verification password below:
            </p>

            <div style="text-align:center; margin:35px 0;">
                <div style="
                    display:inline-block;
                    background:#1d9bf0;
                    color:white;
                    padding:18px 50px;
                    font-size:30px;
                    letter-spacing:4px;
                    font-weight:700;
                    border-radius:10px;
                ">
                    { code }
                </div>
            </div>

            <p style="color:#777; font-size:14px;">
                This code will expire in 2 minutes.  
                If this wasn’t you, please ignore this message.
            </p>

            <p style="margin-top:30px; color:#888;">
                X Security Team
            </p>
        </td>
    </tr>

    <!-- Footer -->
    <tr>
        <td style="border-top:1px solid #1d1f23; padding:15px; text-align:center; color:#555; font-size:12px;">
            © 2026 X Corp. All rights reserved.
        </td>
    </tr>

</table>

</td>
</tr>
</table>
</body>
</html>
"""	
	msg = EmailMultiAlternatives(
		subject, 
		"Your vertification code is inside this email",
		 settings.DEFAULT_FROM_EMAIL,
		 [email]
	)

	msg.attach_alternative(html, 'text/html')
	msg.send()


def generate_pin(size=6, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


class CustomResponse:
	
    @staticmethod
    def succes(message, data=None):
        response = { 
            "status": True,
            "message": message,
            "data": data
        }

        return Response(data=response, status=status.HTTP_200_OK)
    
    @staticmethod
    def error(message, data=None):
        response = { 
            "status": False,
            "message": message,
            "data": data
        }

        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    

def is_email(email): 
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)