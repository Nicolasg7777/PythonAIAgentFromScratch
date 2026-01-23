'''
    THis is the 'T' in 'ETL' - Extract, Transform, Load

    Data Extraction using regular Expressions (Regex).
    Demenonstrates: Pattern matching, data transformation, ETL concepts.
'''

import re
from config import AGENT_NAME

def extract_contact_info(conversation_history):
    '''
       Extract email, phone, and name from conversation text.
       
       This is the 'T' in ETL - Transform.
       We take unstructured text and turn it into structured data.
       
       Real-world example at Medsrv:
       - Extract patient IDs from doctor notes.
       - Extract dates from free-text fields.
       - Extract diagnosis codes from descriptions.
    '''

    # Combine all messages into one text block
    all_text = ' '.join([content for sender, content in conversation_history])

    # Extract email using regex patttern.
    email = extract_email(all_text)

    # Extract phone using regex pattern.
    phone = extract_phone(all_text)

    # Extract name (trickier - we look for patterns like "I'm John" or "My name is John")
    name = extract_name(all_text)
    
    return {
        'email': email,
        'phone': phone,
        'name': name
    }

def extract_email(text):
    '''
       Find email addresses in text.
       
       Regex pattern explained:
       [a-zA-Z0-9._%+-]+ = username part (letters, numbers, dots, etc.)
       @                 = the @ symbol
       [a-zA-Z0-9.-]+    = domain name part
    '''

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_phone(text):
    '''
       find phone numbers in text.
       
       This pattern matches formats like:
       - 123-456-7890
       - (123) 456-7890
       - 123.456.7890
       - 1234567890
    '''

    pattern = r'(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_name(text):
    '''
       Try to find a person's name in text.
       
       Looks for patterns like:
       - "I'm John"
       - "My name is John Smith"
       - "this is John"
       - "call me John"
    '''

    patterns = [
        r"(?:my name is| i'm| i am| this is| call me)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+is my name",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).title()
            # Skip if it matches the agent's name
            if name.lower() != AGENT_NAME.lower():
                return name
    return None

