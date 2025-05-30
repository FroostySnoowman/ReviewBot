import discord
import aiosqlite
import yaml
from discord.ext import commands
from discord import app_commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
review_channel_id = data["Review"]["REVIEW_CHANNEL_ID"]

class ReviewModal(discord.ui.Modal, title='Submit a Review'):
    def __init__(self):
        super().__init__(timeout=None)

    rating = discord.ui.TextInput(
        label='Rating',
        placeholder='Rate from 1 to 5',
        style=discord.TextStyle.short,
        required=True,
    )

    review = discord.ui.TextInput(
        label='Review',
        placeholder='Write your review here',
        style=discord.TextStyle.paragraph,
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Submitting Review", description="Please wait while we process your review...", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        try:
            rating_value = int(self.rating.value)
        except ValueError:
            embed = discord.Embed(title="Invalid Rating", description="Rating must be a whole number between 1 and 5.", color=discord.Color.red())
            await interaction.edit_original_response(embed=embed)
            return
        
        if rating_value < 1 or rating_value > 5:
            embed = discord.Embed(title="Invalid Rating", description="Rating must be a whole number between 1 and 5.", color=discord.Color.red())
            await interaction.edit_original_response(embed=embed)
            return
        
        rating_stars = "⭐" * rating_value + "☆" * (5 - rating_value)

        embed = discord.Embed(title="New Review Submitted", description=f"""
New review submitted by {interaction.user.mention}!
""", color=discord.Color.from_str(embed_color))
        
        embed.timestamp = datetime.now()
        
        embed.add_field(name="Reviewer", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="Review", value=self.review.value or "No review provided.", inline=True)
        embed.add_field(name="Rating", value=f"{rating_stars}", inline=True)
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        review_channel = interaction.client.get_channel(review_channel_id)

        if review_channel:
            async with aiosqlite.connect('database.db') as db:
                await db.execute('INSERT INTO reviews (member_id, rating, review, created_at) VALUES (?,?,?,?)', (interaction.user.id, rating_value, self.review.value, int(datetime.now().timestamp())))
                await db.commit()

                await review_channel.send(embed=embed)

                embed = discord.Embed(title="Review Submitted", description="Your review has been successfully submitted!", color=discord.Color.green())
                await interaction.edit_original_response(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Review channel not found. Please contact an admin.", color=discord.Color.red())
            await interaction.edit_original_response(embed=embed)

class ReviewCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="review", description="Submits a review")
    async def review(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ReviewModal())

async def setup(bot: commands.Bot):
    await bot.add_cog(ReviewCog(bot))