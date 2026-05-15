from flask import Flask, jsonify
from flask_cors import CORS
from email_service import MockEmailService
from agent import EmailAgent

app = Flask(__name__)
CORS(app) # Allow frontend to communicate with backend

email_service = MockEmailService()
agent = EmailAgent()

# In-memory database of processed emails
processed_emails_db = []

@app.route('/api/scan', methods=['POST'])
def scan_emails():
    """Fetches new emails and processes them through the agent."""
    global processed_emails_db
    
    # Fetch 5-10 new mock emails
    new_emails = email_service.fetch_recent_emails()
    
    results = []
    for email in new_emails:
        # Run agent on email
        analysis = agent.analyze_email(email)
        
        # Merge analysis back into email record
        processed_record = {**email, **analysis, "processed": True}
        results.append(processed_record)
        
        # Apply action
        email_service.apply_action(email['id'], analysis['action'])
        
    # Prepend new results to our in-memory DB
    processed_emails_db = results + processed_emails_db
    
    return jsonify({"message": f"Successfully scanned {len(results)} emails.", "count": len(results)})

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Returns the list of processed emails."""
    return jsonify(processed_emails_db)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Returns aggregated stats for the dashboard."""
    total = len(processed_emails_db)
    if total == 0:
        return jsonify({
            "total": 0,
            "spam": 0,
            "ham": 0,
            "spam_rate": 0.0
        })
        
    spam_count = sum(1 for e in processed_emails_db if e['classification'] == 'Spam')
    ham_count = total - spam_count
    
    return jsonify({
        "total": total,
        "spam": spam_count,
        "ham": ham_count,
        "spam_rate": round((spam_count / total) * 100, 1)
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
