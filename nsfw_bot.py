import discord
import aiohttp
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.messages = True  # This is crucial for receiving message content
intents.message_content = True  # Make sure this is enabled if using discord.py version 2.x

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - Ready to monitor for images.')

@bot.event
async def on_message(message):
    # Debug: Check if the bot is reading messages
    print(f"Received message from {message.author}: {message.content[:20]}...")

    if not message.content and not message.attachments:
        print("The message has no text or attachments.")
        return

    if message.author == bot.user or message.author.bot:
        print("Message is from the bot itself or another bot, ignoring.")
        return

    if message.attachments:
        print(f"Message has {len(message.attachments)} attachment(s). Checking for images...")
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                print(f'Found image attachment: {attachment.filename}. Analyzing for NSFW content...')
                custom_api_url = f"http://checker.blueline-rp.com:8086/?url={attachment.url}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(custom_api_url) as api_response:
                        if api_response.status == 200:
                            analysis = await api_response.json()
                            print(f'Custom API Response: {analysis}')
                            if analysis.get('data', {}).get('porn') > 98 or analysis.get('data', {}).get('sexy') > 98:
                                print(f"NSFW content detected in image posted by {message.author} in {message.channel.name}.")
                                log_guild_id = GUILDID
                                log_channel_id = LOG CHANNEL ID
                                log_guild = bot.get_guild(log_guild_id)
                                if log_guild:
                                    log_channel = log_guild.get_channel(log_channel_id)
                                    if log_channel:
                                        await log_channel.send(
                                            f"Member {message.author.mention} posted an NSFW image: {attachment.url} in {message.channel.name}."
                                        )
                                        print("Logged NSFW content to specified channel.")
                                await message.delete()
                                warning_msg = "Warning: Posting NSFW images is not allowed. Please adhere to the server rules."
                                await message.channel.send(warning_msg)
                                print("Original NSFW message deleted and warning issued.")
                            else:
                                print("Image analyzed and found to be safe.")
                        else:
                            print(f"Error fetching analysis from custom NSFW detection API: Status {api_response.status}")
    else:
        print("No attachments found in message.")

    await bot.process_commands(message)

bot.run('TOKEN')
