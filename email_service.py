from schemas import Booking_Base, Hotel_Base
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from db import models

def send_confirmation_email(email: str, booking_info: Booking_Base):
    
    # email settings for sender and receiver
    sender_email = "hotel_booking@mail.com"
    receiver_email = email

    # create MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Booking Confirmation"

    # content of the email
    body = f"Dear {booking_info.guest_name},\n\n" \
           f"Your booking has been confirmed.\n\n" \
           f"Booking details:\n" \
           f"   Name: {booking_info.guest_name}\n" \
           f"   Email: {booking_info.guest_email}\n" \
           f"   Check-in Date: {booking_info.check_in_date}\n" \
           f"   Check-out Date: {booking_info.check_out_date}\n\n" \
           f"Thank you for choosing our hotel!\n\n" \
           f"Best regards,\n" \
           f"The Easy Hotel Booking Team"
    message.attach(MIMEText(body, "plain"))

    # setp up SMTP server and send the email
    with smtplib.SMTP("localhost", 1025) as server: # MailHog's default SMTP server address and port
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

    print("Confirmation email sent successfully!")

