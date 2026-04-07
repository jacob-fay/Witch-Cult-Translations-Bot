# Witch-Cult-Translations-Bot
Uses github actions to periodically check the website https://witchculttranslation.com/ and then sends a discord message to your account to notify you if new chapters are released 
Currently it checks twice daily, once at 10am est and once at 7pm est
If you want to use this yourself do the following steps:
- fork the repo
- Create a Discord bot in discord's developer portal and copy the bots token 
- Add a secret called "BOT_TOKEN" with the token id you just copied
- Add a secret called "DISCORD_ID" with the acount id that you want DMed

