## Reddit Bot Setup
1. Log into Reddit and navigate to https://old.reddit.com/prefs/apps/
2. Click "are you a developer?  create an app..." to open the New App screen.
   1. Name
      1. General app name.  Ex: "Nicholas Angel Bot".  It can also be the same as the bot's username.
   2. App Type (Web, installed, script)
      1. Select "Script"
   3. Description
      1. Brief description of what your bot does
   4. About URL: 
      1. Your own website or "localhost"
   5. Redirect URI:
      1. Your own website or "localhost:8080"
3. Once the app is created, copy the following details to their appropriate variable in .env
    1. client_id
        1. Bold string of random text underneath "Personal use script"
    2. client_secret
        1. Labeled "Secret"
4. Add an identifier to .env under "user_agent".  This can be the bot's username, or something else.
5. Add the credentials to the Reddit account that created the bot to .env under username / password