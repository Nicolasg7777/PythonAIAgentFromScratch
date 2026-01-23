'''
    Automated reminder job
    Demonstrates: Scheduled tasks, batch processing, automation.

    This would typically run on a schedule (daily via cron, Windows Task Scheduler,
    or a cloud service like AWS Lambda).
    
    Medserv equivalent:
    - Daily Job to process unpaid claims.
    - Weekly report generation
    - Automated data validation checks.
'''

from datetime import datetime, timedelta
from database import get_pending_reminders, mark_reminder_sent
from email_sender import send_reminder_email


def run_reminder_job():
    '''
       Find all bookings that need reminders and send emails.
       
       This is BATCH PROCESSING:
       1. Query all records that need action.
       2. Process each one
       3. Mark as processed
       
       same pattern used for:
       - Processing insurance claims.
       - Generating monthly statements
       - Data migration jobs
    '''

    print("=" * 50)
    print("Running Reminder Job")
    print(f'Time: {datetime.now()}')
    print("=" * 50)

    # Get all bookings that need reminders
    pending = get_pending_reminders()

    if not pending:
        print("No pending reminders found.")
        return
    
    print(f'Found {len(pending)} pending reminders.')

    # Process each one.
    success_count = 0
    fail_count = 0

    for booking_id, scheduled_for, name, email in pending:
        print(f'\nProcessing: {name} ({email})')
        print(f' Scheduled for: {scheduled_for}')

        # Send the reminder email
        if send_reminder_email(email, name, scheduled_for):
            # Mark as sent in database
            mark_reminder_sent(booking_id)
            success_count += 1
            print(" Status: SENT")
        else:
            fail_count += 1
            print(" Status: FAILED")

    # Summary
    print("\n" + "=" * 50)
    print("Job Complete")
    print(f' Successful: {success_count}')
    print(f' Failed: {fail_count}')
    print("=" * 50)

if __name__ == "__main__":
    run_reminder_job()
    