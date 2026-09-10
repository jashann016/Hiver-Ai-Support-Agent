"""
Intent taxonomy, keyword lexicons, and escalation policy definitions for @SpotifyCares support.
"""

INTENTS = [
    "SUBSCRIPTION_BILLING",
    "PLAYBACK_CRASH_BUG",
    "ACCOUNT_ACCESS_SECURITY",
    "PLAYLIST_LIBRARY_LOSS",
    "HARDWARE_CONNECTIVITY",
    "FEATURE_REQUEST_FEEDBACK",
    "CHURN_CANCELLATION"
]

INTENT_DESCRIPTIONS = {
    "SUBSCRIPTION_BILLING": "Questions or disputes about charges, subscription tiers, renewal, payment methods, student discounts, and invoices.",
    "PLAYBACK_CRASH_BUG": "Technical glitches, songs skipping/stopping, app crashing, error codes, audio distortion, or offline sync failure.",
    "ACCOUNT_ACCESS_SECURITY": "Hacked accounts, password resets, 2FA issues, unauthorized email changes, disabled accounts, login failures.",
    "PLAYLIST_LIBRARY_LOSS": "Accidental deletion of playlists, missing liked songs, library synchronization discrepancies across devices.",
    "HARDWARE_CONNECTIVITY": "Issues linking Spotify to external hardware such as Bluetooth speakers, Sonos, CarPlay, Android Auto, or gaming consoles.",
    "FEATURE_REQUEST_FEEDBACK": "Suggestions for new features, requests for UI rollbacks, lossless audio inquiries, or general product feedback.",
    "CHURN_CANCELLATION": "Requests to cancel subscriptions, account deletion requests under GDPR/CCPA, or complaints leading to switching services."
}

ESCALATION_KEYWORDS = [
    "hacked", "stolen", "unauthorized", "chargeback", "lawsuit", "refund", 
    "fraud", "double charge", "charged twice", "gdpr", "delete my data", 
    "disabled my account", "2fa", "two-factor", "bank", "credit card", "dispute"
]
