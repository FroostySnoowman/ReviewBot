# ReviewBot

## Setup
0. Rename `example-config.yml` to `config.yml`
1. Head to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a "New Application"
3. Name the application whatever you want, agree to the Terms of Service, and click "Create".
4. Click "Bot" on the left navigation bar
5. Enable "Presence Intent", "Server Members Intent", and "Message Content Intent"
6. Scroll up and "Reset Token". Paste the copied token in `config.yml` file under `TOKEN`
7. Click "OAuth2" on the left navigation bar
8. Choose "bot" and "applications.commands" under "Scope"
9. Scroll down and select the "Administrator" permission under "Bot Permissions"
10. Copy the "Generated URL" towards the bottom and paste it in your browser
11. Invite the bot to your server
12. Setup the bot on a server/host of your choice and run `pip install -r requirements.txt` (Pterodactyl does this for you when you run it)
13. Run the bot using `python3 main.py`
14. Use the `/review` command and have fun!
15. OPTIONAL: If you would like to disable the "Add App" button when you click on the bot in a server, choose "Installation" in [Discord Developer Portal](https://discord.com/developers/applications) and under "Install Link", choose "None".

## Support
As part of every FroostySnoowman (someone0171) bot, I gaurentee a 3 month support period. If you have any issues, need minor tweaks, or have minor adjustments please contact me and I'll be more than happy to help. After the 3 month period, I cannot gaurentee I will be available, but please reach out.

Gaurenteed support commences on 6/1/25 and ends on 9/1/25.