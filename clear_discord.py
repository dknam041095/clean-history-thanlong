import discord
import asyncio
import os
import sys

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID"))

async def clear_channel():
    if not TOKEN or not CHANNEL_ID:
        print("ERROR: Missing DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID")
        sys.exit(1)

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    async with client:
        await client.login(TOKEN)
        channel = await client.fetch_channel(CHANNEL_ID)

        print(f"Clearing channel: #{channel.name}")

        # Bulk delete messages <= 14 days (nhanh)
        deleted = await channel.purge(limit=None)
        print(f"Bulk deleted: {len(deleted)} messages")

        # Xóa message cũ hơn 14 ngày (nếu có) — từng cái một
        old_count = 0
        async for message in channel.history(limit=None):
            try:
                await message.delete()
                old_count += 1
                await asyncio.sleep(1)  # tránh rate limit
            except discord.errors.NotFound:
                pass

        print(f"Old messages deleted: {old_count}")
        print("Done!")

asyncio.run(clear_channel())
