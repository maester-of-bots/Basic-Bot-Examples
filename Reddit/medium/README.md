# Summary

This is a Python-based Reddit bot which is configured to crawl comments on r/hotfuzz and r/hotfuzzgifs, detect users who post profanity, calculate how much they owe based on the Hot Fuzz Swear Jar, then calculate the user's total and posts a reply comment thanking the user for their donation to the church roof.

All comment IDs are stored in a local database, and the bot refers back to them to avoid double-commenting.

Should probably make that a dictionary / json...

## Reddit Bot Setup
1. Log into Reddit and navigate to https://old.reddit.com/prefs/apps/
2. Click "are you a developer?  create an app..." to open the New App screen.
   1. Name
      1. General app name.  Ex: "Nicholas Angel Bot"
   2. App Type (Web, installed, script)
      1. Select "Script"
   3. Description
      1. Brief description of what your bot does
   4. About URL: 
      1. Your own website or 127.0.0.1
   5. Redirect URI:
      1. Your own website or 127.0.0.1
3. Once the app is created, copy the following details to their appropriate variable in .env
    1. client_id
        1. Bold string of random text underneath "Personal use script"
    2. client_secret
        1. Labeled "Secret"
4. Add an identifier to .env under "user_agent".  This can be the bot's username, or something else.
5. Add the credentials to the Reddit account that created the bot to .env under username / password