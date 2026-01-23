'''
    Email Integration using Resend API
    Demonstrates: REST API calls, external service integration.

'''

import requests
from config import RESEND_API_KEY, RESEND_API_URL, FROM_EMAIL

def send_reminder_email(to_email, name, scheduled_for):
    '''
       Send a booking reminder email.
       
       This is external API integration - a key skill for data engineers.
       At Medserv, youd integrate with:
       - Insurance verification APIs.
       - Patient portal systems.
       - Billing services.
       
       Parameters:
       - to_email: Customer's email address
       - name: Customer's name for personalization.
       - scheduled_for: the appointment date/time.
    '''

    # Build the email content.
    subject = "Reminder: Your Consultation is Coming Up!"

    html_content = f"""
    <h2>Hi {name}!</h2>
    <p>This is a friendly reminder that your consultation is scheduled for:</p>
    <p><strong>{scheduled_for}</strong></p>
    <p>If you need to reschedule, please let us know.</p>
    <br>
    <p>Best regards,<br>The Support Team</p>
    """

    # Make the API request.
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            RESEND_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            print(f"Email sent successfully to {to_email}")
            return True
        else:
            print(f'Email failed: {response.status_code} - {response.text}')
            return False
        
    except Exception as e:
        print(f"Email error: {e}")
        return False
    

def send_welcome_email(to_email, name):
    '''
       Send a welcome email when we capture a new load.
       
       This could be triggered when:
       - A new profile is created
       - User books their first consultation
    '''

    subject = "Thanks for Reaching out!"

    html_content = f"""
    <h2>Welcome, {name}!</h2>
    <p>Thank you for contacting us. We've recived your information
    and someone from our team will be in touch soon.</p>
    <p>In the meantime, feel free to reply to this email if you have any questions.</p>
    <br>
    <p>Best regards,<br>The Support Team</p>
    """

    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            RESEND_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        return response.status_code == 200
    
    except Exception as e:
        print(f"Email error: {e}")
        return False
    
