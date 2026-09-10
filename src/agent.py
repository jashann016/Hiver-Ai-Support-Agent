"""
Core Customer Support AI Agent for @SpotifyCares:
1. Intent Classification
2. Historical RAG Grounded Reply Synthesis
3. Escalation Decision & Justification Engine
"""

import re
from typing import Dict, Any, Tuple
from src.taxonomy import INTENTS, INTENT_DESCRIPTIONS, ESCALATION_KEYWORDS
from src.historical_kb import HISTORICAL_RESOLUTIONS


class SpotifySupportAgent:
    def __init__(self, mode: str = "production"):
        self.mode = mode

    def classify_intent(self, text: str) -> Tuple[str, float]:
        """
        Classifies incoming customer tweet into one of the grounded taxonomy intents.
        Returns (predicted_intent, confidence_score).
        """
        t = text.lower()

        # Intent heuristic & lexical feature extraction
        scores = {intent: 0.0 for intent in INTENTS}

        if any(w in t for w in ["charge", "billed", "billing", "payment", "card", "discount", "family plan", "duo", "student", "sheerid", "receipt"]):
            scores["SUBSCRIPTION_BILLING"] += 3.5

        if any(w in t for w in ["crash", "freeze", "stops", "pause", "skipping", "playback", "bug", "glitch", "error", "static", "offline", "download"]):
            scores["PLAYBACK_CRASH_BUG"] += 3.2

        if any(w in t for w in ["hacked", "stolen", "password", "login", "2fa", "two-factor", "email changed", "disabled", "security", "compromised"]):
            scores["ACCOUNT_ACCESS_SECURITY"] += 4.0

        if any(w in t for w in ["playlist", "playlists", "liked songs", "deleted", "library", "disappeared", "recover"]):
            scores["PLAYLIST_LIBRARY_LOSS"] += 3.8

        if any(w in t for w in ["sonos", "bluetooth", "carplay", "android auto", "speaker", "connect", "apple watch", "ps5", "xbox"]):
            scores["HARDWARE_CONNECTIVITY"] += 3.5

        if any(w in t for w in ["cancel", "cancellation", "quitting", "switching to", "gdpr", "delete my account", "refund"]):
            scores["CHURN_CANCELLATION"] += 3.0

        if any(w in t for w in ["feature", "bring back", "hifi", "lossless", "update ui", "suggestion", "wish"]):
            scores["FEATURE_REQUEST_FEEDBACK"] += 3.0

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]

        if max_score == 0:
            best_intent = "PLAYBACK_CRASH_BUG"  # Default majority fallback
            confidence = 0.45
        else:
            confidence = min(0.95, 0.55 + (max_score * 0.1))

        return best_intent, confidence

    def evaluate_escalation(self, text: str, intent: str, confidence: float) -> Tuple[bool, str]:
        """
        Determines whether message must be escalated to human agent.
        Rules:
        - Financial transactions / refund disputes / PII exposure
        - Account security takeover / 2FA issues / GDPR deletion
        - Extremely low confidence on intent
        """
        t = text.lower()

        # Rule 1: Security Takeover & PII
        if intent == "ACCOUNT_ACCESS_SECURITY" and any(k in t for k in ["hacked", "stolen", "2fa", "disabled", "changed"]):
            return True, "Security compromise / identity verification requires private authenticated channel and human safety intervention."

        # Rule 2: Monetary disputes & refund claims
        if intent == "SUBSCRIPTION_BILLING" and any(k in t for k in ["refund", "double charge", "charged twice", "theft", "unauthorized", "dispute"]):
            return True, "Monetary dispute / refund processing requires account billing PII and direct human review."

        # Rule 3: Compliance & Legal
        if any(k in t for k in ["gdpr", "delete my data", "lawyer", "legal", "sue"]):
            return True, "Legal / GDPR compliance request requires human regulatory processing."

        # Rule 4: Model Confidence Threshold
        if confidence < 0.50:
            return True, "Low intent classification confidence; safeguarding against erroneous automated guidance."

        return False, "Standard troubleshooting issue resolvable via grounded self-service guidance."

    def generate_reply(self, text: str, intent: str, escalate: bool, escalation_reason: str) -> str:
        """
        Synthesizes brand-aligned, grounded response based on historical @SpotifyCares behavior.
        """
        if escalate:
            return (
                "Hey there! We want to help look into this securely. "
                "Please send us a Direct Message with your account email address and details so our team can assist: "
                "https://t.co/dm_spotify"
            )

        # Match with historical KB for grounded answer
        for item in HISTORICAL_RESOLUTIONS:
            if item["intent"] == intent:
                return item["reply_template"]

        # Default fallback
        return (
            "Hey! We'd love to help out. Could you let us know your exact device model and Spotify version? "
            "In the meantime, you can check our troubleshooting guides at https://support.spotify.com"
        )

    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        """
        End-to-end tri-task pipeline execution.
        """
        intent, confidence = self.classify_intent(tweet_text)
        escalate, reason = self.evaluate_escalation(tweet_text, intent, confidence)
        reply = self.generate_reply(tweet_text, intent, escalate, reason)

        return {
            "input_text": tweet_text,
            "predicted_intent": intent,
            "confidence": round(confidence, 3),
            "escalate_to_human": escalate,
            "escalation_reason": reason,
            "draft_reply": reply
        }
