from transformers import pipeline
import re

class EmailAgent:
    def __init__(self):
        # Load the pre-trained model for spam detection
        print("Loading pre-trained spam detection model...")
        self.classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
        print("Model loaded successfully.")

    def analyze_email(self, email_data):
        """
        Analyzes an email to determine if it's spam and decides on an action.
        """
        text_to_analyze = f"{email_data['subject']} {email_data['body']}"
        
        # Max length for BERT tiny is usually 512 tokens. We'll truncate characters as a crude approximation.
        text_to_analyze = text_to_analyze[:2000] 

        try:
            prediction = self.classifier(text_to_analyze)[0]
            label = prediction['label'].lower()
            score = prediction['score']
            
            # Usually label is 'spam' or 'ham', or 'LABEL_1'/'LABEL_0'
            if label == 'spam' or label == 'label_1':
                spam_probability = score
            else:
                spam_probability = 1.0 - score
        except Exception as e:
            print(f"Error classifying email: {e}")
            spam_probability = 0.0

        # Decision Engine
        if spam_probability > 0.8:
            classification = "Spam"
            action = "Block"
            explanation = self._generate_explanation(text_to_analyze, spam_probability, "high")
        elif spam_probability >= 0.5:
            classification = "Spam"
            action = "Flag"
            explanation = self._generate_explanation(text_to_analyze, spam_probability, "medium")
        else:
            classification = "Ham"
            action = "Allow"
            explanation = self._generate_explanation(text_to_analyze, spam_probability, "low")

        return {
            "email_id": email_data["id"],
            "subject": email_data["subject"],
            "spam_probability": float(spam_probability),
            "classification": classification,
            "action": action,
            "explanation": explanation
        }

    def _generate_explanation(self, text, probability, risk_level):
        """Generates a human-readable explanation based on text heuristics and the model's score."""
        text_lower = text.lower()
        reasons = []
        
        if risk_level == "low":
            return "Email content appears to be standard communication."
            
        urgent_keywords = ['urgent', 'immediate', 'hurry', 'alert', 'compromised', 'locked']
        money_keywords = ['guaranteed', 'winner', 'prize', 'gift card', 'discount', 'free', 'investment', 'returns']
        
        has_urgent = any(word in text_lower for word in urgent_keywords)
        has_money = any(word in text_lower for word in money_keywords)
        
        if has_urgent:
            reasons.append("contains artificial urgency cues")
        if has_money:
            reasons.append("contains promotional or financial incentives")
            
        if not reasons:
            reasons.append("model detected underlying spam-like linguistic patterns")
            
        explanation = f"Flagged as Spam ({probability:.1%} certainty) because it " + " and ".join(reasons) + "."
        return explanation
