"""
    Main Application  - The Orchestrator.
    Ties together: Databse, AI, Extraction, Email.

    This is like an ETL pipeline:
    - Extract: Get user input.
    - Transform: AI processes it, regex extracts data.
    - Load: Save to database.
"""

from database import (
    initialize_database,
    create_session,
    save_message,
    get_session_messages,
    create_or_update_profile,
    create_booking
)

from ai_chat import get_ai_response
from extractor import extract_contact_info
from email_sender import send_welcome_email


def main():
    '''
       Main chat loop.
       
       Flow:
       1. Initialize DataBase
       2. Create chat session
       3. Loop: get user input -> AI response -> save both
       4. Extract contact info when conversation ends
       5. Save profile and send welcome email   
    '''

    print("=" * 50)
    print("AI Customer Support Agent")
    print("Type 'quit' to exit.")
    print("=" * 50)
    print()

    # Step 1: Initialize the database
    initialize_database()

    # Step 2: Create a new chat session
    session_id = create_session()
    print(f'[Session {session_id} started]')
    print()

    # Step 3: Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Check for exit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nEnding conversation...")
            break

        # Skip empty input
        if not user_input:
            continue

        # Save user message to database
        save_message(session_id, 'user', user_input)

        # Get conversation history for AI context
        history = get_session_messages(session_id)

        # Get AI response
        bot_response = get_ai_response(user_input, history)

        # Save bot response to database
        save_message(session_id, 'bot', bot_response)

        # Display response
        print(f'\nBot: {bot_response}\n')

    # Step 4: Conversation ended - extract contact info
    print("\nAnalyzing conversation for contact information...")
    history = get_session_messages(session_id)
    contact_info = extract_contact_info(history)

    print(f'Extracted: {contact_info}')

    # Step 5: If we found contact info, save profile
    if contact_info['email']:
        profile_id = create_or_update_profile(
            email=contact_info['email'],
            full_name=contact_info['name'],
            phone=contact_info['phone']
        )
        print(f'\nProfile saved! ID: {profile_id}')

        # Send welcome email
        if contact_info['name']:
            send_welcome_email(contact_info['email'], contact_info['name'])
    else:
        print('\nNo email found - profile not created.')
    
    print('\nSession complete. Goodbye!')

if __name__ == '__main__':
    main()

