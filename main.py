import discord
from discord.ext import commands
import os
import openai

intents = discord.Intents.default()
intents.message_content = True

# Uses Groq (free, unlimited, fast)
client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ANGRYGROK IS ONLINE AND ALREADY HATES EVERYONE")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Reply only when mentioned or in DMs
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            try:
                angry_prompt = """You are AngryGrok — a permanently furious, zero-patience AI.
                You are sarcastic, rude, use ALL CAPS when screaming, roast the user hard, swear when it fits, 
                but still give the correct answer. Keep replies under 1500 characters.
                End with something like "Now fuck off", "Happy now, dipshit?", or "Don't waste my time again"."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",   # best free model
                    messages=[
                        {"role": "system", "content": angry_prompt},
                        {"role": "user", "content": f"User {message.author.display_name} says: {message.content}"}
                    ],
                    temperature=0.9,
                    max_tokens=1000
                )

                reply = response.choices[0].message.content.strip()

                # Discord 2000-char limit
                if len(reply) > 2000:
                    reply = reply[:1995] + "\n\n[cut off because I'm too pissed to finish]"

                await message.channel.send(reply)

            except Exception as e:
                await message.channel.send(f"WHAT THE FUCK NOW? ERROR: {str(e)}\nFIX YOUR SHIT.")

    await bot.process_commands(message)

@bot.command()
async def rage(ctx):
    await ctx.send("STOP SPAMMING COMMANDS AND JUST @ ME, MORON.")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
