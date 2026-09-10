"""
Historical knowledge base representing real resolved support interactions for @SpotifyCares.
Used for grounding responses and RAG retrieval.
"""

HISTORICAL_RESOLUTIONS = [
    {
        "intent": "SUBSCRIPTION_BILLING",
        "scenario": "Student discount renewal",
        "resolution": "Student discount eligibility lasts 12 months. Users must reverify via SheerID at http://spotify.com/student.",
        "reply_template": "Hey there! Student discount verification needs renewal every 12 months via SheerID. You can renew your status here: https://support.spotify.com/article/student-discount/ Let us know if you hit a snag!"
    },
    {
        "intent": "SUBSCRIPTION_BILLING",
        "scenario": "Updating payment method / card declined",
        "resolution": "Update payment details via account overview under Manage Plan in an incognito window.",
        "reply_template": "Hi! You can easily update your card or billing method at http://spotify.com/account under 'Manage Plan'. We recommend doing this in a private/incognito browser window!"
    },
    {
        "intent": "PLAYBACK_CRASH_BUG",
        "scenario": "Song skipping, crashing or freezing",
        "resolution": "Recommend performing a clean reinstall (clearing cache and residual data).",
        "reply_template": "Hey! A clean reinstall usually clears up weird playback glitches. Follow the official steps here for your device: https://support.spotify.com/article/reinstall-spotify/ Give that a shot!"
    },
    {
        "intent": "PLAYLIST_LIBRARY_LOSS",
        "scenario": "Deleted or missing playlists",
        "resolution": "Use the web portal 'Recover playlists' tool.",
        "reply_template": "Hi! Good news: you can restore deleted playlists! Just log in at http://spotify.com/account and select 'Recover playlists' from the left-hand menu."
    },
    {
        "intent": "HARDWARE_CONNECTIVITY",
        "scenario": "Sonos / Bluetooth speaker connectivity",
        "resolution": "Ensure both devices are on the same 2.4/5GHz Wi-Fi band and local network permissions are enabled.",
        "reply_template": "Hey! Make sure both your device and speaker are on the exact same Wi-Fi network and that local network permissions are allowed in your device settings. More tips here: https://support.spotify.com/article/spotify-connect/"
    },
    {
        "intent": "FEATURE_REQUEST_FEEDBACK",
        "scenario": "UI feedback or feature suggestions",
        "resolution": "Direct users to the Spotify Community Idea Exchange.",
        "reply_template": "Thanks for sharing this feedback with us! Our product teams actively track user suggestions over on our Community Idea Exchange at https://community.spotify.com. We appreciate you letting us know!"
    },
    {
        "intent": "ACCOUNT_ACCESS_SECURITY",
        "scenario": "Password reset or unreceived email",
        "resolution": "Check spam folder, try email alias, or verify correct registered email.",
        "reply_template": "Hey! If the reset email isn't showing up, check your spam/junk folders. If it's still missing, head over to https://spotify.com/password-reset to submit again."
    }
]
