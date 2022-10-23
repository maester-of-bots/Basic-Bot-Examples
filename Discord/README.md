# Discord Bots

## Starting Out - Creating Bot Account and Getting Authentication Information

1. Navigate to the Discord Developers portal - https://discord.com/developers/applications

2. Click "Create Application" at the top right

3. Give your application a descriptive name, agree to the terms of service, and click "Create"

4. This takes you to the Application screen.  Now, click "Bot" on the left side to create the bot.  Click "Add", then "Yes, do it!"

5. Here, you can configure your bot's icon, username, token, and intents.  Click "Reset Token" to get a new token, and update your code with it.  Then, change the "Message Content Intent" option to "Enabled".

6. From there, click "OAuth2" from the left side and then "URL Generator".  Select "Bot" for the first scope, then whatever permissions your bot needs under the second scope.  If this is your first bot, you can start out with "Read Messages/View Channels" and "Send Messages".

7. Click "Copy" after selecting the necessary permissions to copy the bot's invitation URL.  This URL allows anyone to invite the bot to their server, as long as they have the permission to invite bots on that server.  Open it in a web browser and you'll be able to add your bot to your server.