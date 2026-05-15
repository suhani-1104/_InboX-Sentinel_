import random
import uuid
from datetime import datetime, timedelta

class MockEmailService:
    def __init__(self):
        self.mock_spam_templates = [
            ("WINNER!!", "As a valued network customer you have been selected to receivea £900 prize reward! To claim call 09061701461. Claim code KL341."),
            ("Free entry", "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"),
            ("URGENT!", "You have won a 1 week FREE membership in our £100,000 Prize Jackpot! Txt the word: CLAIM to No: 81010 T&C www.dbuk.net LCCLTD POBOX 4403LDNW1A7RW18"),
            ("XXX MobileMovieClub", "To use your credit, click the WAP link in the next txt message or click here>> http://wap. xxxmobilemovieclub.com?n=QJKGIGHIGGKE"),
            ("England v Macedonia", "dont miss the goals/team news. Txt ur national team to 87077 eg ENGLAND to 87077 Try:WALES, SCOTLAND 4txt/ú1.20 POBOXox36504W45WQ 16+")
        ]
        
        self.mock_ham_templates = [
            ("Project update meeting tomorrow", "Hi team, let's catch up tomorrow at 10 AM to discuss the new feature rollout. Please review the attached doc."),
            ("Your recent Amazon order", "Your order #12345 has been shipped. Track your package using the link provided."),
            ("Coffee later?", "Hey! It's been a while. Are you free for coffee this Thursday afternoon?"),
            ("Invoice for Q3 consulting services", "Please find attached the invoice for my consulting hours in Q3. Let me know if you have any questions."),
            ("Reminder: Dentist appointment", "This is an automated reminder of your upcoming dentist appointment on Friday at 2:00 PM.")
        ]

    def fetch_recent_emails(self, count=10):
        """Generates a random batch of mock emails."""
        emails = []
        for _ in range(count):
            is_spam = random.choice([True, False])
            template_pool = self.mock_spam_templates if is_spam else self.mock_ham_templates
            subject, body = random.choice(template_pool)
            
            # Generate a somewhat recent timestamp
            minutes_ago = random.randint(1, 1440)
            timestamp = (datetime.now() - timedelta(minutes=minutes_ago)).isoformat()
            
            sender = "unknown@spam.com" if is_spam else "colleague@company.com"
            
            emails.append({
                "id": str(uuid.uuid4()),
                "sender": sender,
                "subject": subject,
                "body": body,
                "timestamp": timestamp,
                "processed": False
            })
            
        # Sort by timestamp descending
        emails.sort(key=lambda x: x['timestamp'], reverse=True)
        return emails

    def apply_action(self, email_id, action):
        """Mock applying an action to an email (e.g., move to spam, flag)."""
        # In a real app, this would call Gmail API to apply/remove labels
        pass
