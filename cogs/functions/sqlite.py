import discord
import aiosqlite
import sqlite3
import yaml
from discord.ext import commands
from discord import app_commands
from typing import Literal

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

async def check_tables():
    await reviews()

async def refresh_table(table: str):
    if table == "Reviews":
        await reviews(True)

async def reviews(delete: bool = False):
    async with aiosqlite.connect('database.db') as db:
        if delete:
            try:
                await db.execute('DROP TABLE reviews')
                await db.commit()
            except sqlite3.OperationalError:
                pass

        try:
            await db.execute('SELECT * FROM reviews')
        except sqlite3.OperationalError:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,
                    rating INTEGER,
                    review TEXT,
                    created_at INTEGER
                )
            """)
            await db.commit()

class SQLiteCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="refreshtable", description="Refreshes a SQLite table!")
    @app_commands.describe(table="What table should be refreshed?")
    @app_commands.default_permissions(administrator=True)
    async def refreshtable(self, interaction: discord.Interaction, table: Literal["Review"]) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)

        if await self.bot.is_owner(interaction.user):
            await refresh_table(table)
            embed = discord.Embed(description=f"Successfully refreshed the table **{table}**!", color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed("You do not have permission to use this command!", color=discord.Color.red())
        
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(SQLiteCog(bot))