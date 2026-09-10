"""
Baseline implementations for comparative evaluation:
- Baseline 0 (Trivial): Majority-class intent + Static template + Naive keyword escalation
- Baseline 1 (Simple): Zero-shot ungrounded heuristic rule without confidence gating
"""

from typing import Dict, Any


class Baseline0TrivialAgent:
    """
    Baseline 0: Most basic heuristic rule engine.
    Always predicts majority intent 'PLAYBACK_CRASH_BUG' unless exact keyword match,
    and uses fixed generic macro response.
    """
    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        t = tweet_text.lower()
        
        # Simple keyword matching for intent
        if "bill" in t or "charge" in t:
            intent = "SUBSCRIPTION_BILLING"
        elif "hack" in t or "password" in t:
            intent = "ACCOUNT_ACCESS_SECURITY"
        else:
            intent = "PLAYBACK_CRASH_BUG"  # Majority class fallback

        # Naive escalation: escalate if text contains 'refund' or 'urgent'
        escalate = "refund" in t or "urgent" in t or "hack" in t
        reason = "Escalated by naive keyword trigger" if escalate else "Auto-handled by default"

        reply = (
            "Hi there, please visit https://support.spotify.com for help with your issue."
            if not escalate else
            "Please DM us your email address."
        )

        return {
            "predicted_intent": intent,
            "confidence": 0.50,
            "escalate_to_human": escalate,
            "escalation_reason": reason,
            "draft_reply": reply
        }


class Baseline1SimpleAgent:
    """
    Baseline 1: Standard ungrounded heuristic with broad rules, but lacks RAG grounding and confidence scoring.
    """
    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        t = tweet_text.lower()

        if "pay" in t or "charge" in t or "sub" in t or "card" in t:
            intent = "SUBSCRIPTION_BILLING"
        elif "login" in t or "hacked" in t or "password" in t or "2fa" in t:
            intent = "ACCOUNT_ACCESS_SECURITY"
        elif "playlist" in t or "song" in t:
            intent = "PLAYLIST_LIBRARY_LOSS"
        elif "bluetooth" in t or "sonos" in t or "car" in t:
            intent = "HARDWARE_CONNECTIVITY"
        elif "feature" in t or "wish" in t:
            intent = "FEATURE_REQUEST_FEEDBACK"
        elif "cancel" in t:
            intent = "CHURN_CANCELLATION"
        else:
            intent = "PLAYBACK_CRASH_BUG"

        # Broad escalation rules without context verification
        escalate = any(k in t for k in ["hack", "refund", "charged", "cancel", "stolen", "law"])
        reason = "Keyword match in escalation lexicon" if escalate else "Generic self-serve"

        reply = (
            "Hey! Try restarting your device or reinstalling the app from our support portal."
            if not escalate else
            "Hey, send us a DM with your username and we can look into this."
        )

        return {
            "predicted_intent": intent,
            "confidence": 0.70,
            "escalate_to_human": escalate,
            "escalation_reason": reason,
            "draft_reply": reply
        }
