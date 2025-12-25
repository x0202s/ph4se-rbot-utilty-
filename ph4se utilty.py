# khs x lone
import discord
from discord.ext import commands, tasks
import secrets
import time

pene_token = "" # pon el token entre las comillas 
pene_intents = discord.Intents.default()
pene_intents.members = True
pene_intents.message_content = True
pene_bot = commands.Bot(command_prefix=".", intents=pene_intents)

pene_getbot_channel = 1453857900157210664 # siii chatgpt 
pene_claims_channel = 1453857842456039506 # sii chatgpt 
pene_boost_role_1 = 1453857802903617576 # sii chatgpt 
pene_boost_role_2 = 1453858262892941545 # sii chatgpt 
pene_claim_role = 1453858235806122108 # sii chatgpt 

pene_keys_store = {}

def pene_generate_key():
    while True:
        key = f"KHS-{secrets.randbelow(10**8):08d}"
        if key not in pene_keys_store:
            return key

def pene_now_ts():
    return int(time.time())

class GetBotView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="bot here", style=discord.ButtonStyle.danger, custom_id="pene_getbot_button")
    async def pene_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        dm_embed = discord.Embed(title="tutorial: soon", description="```click the button below to get the r-bot```", color=0x111111)
        author_name = f"{interaction.user.name}#{interaction.user.discriminator}"
        author_icon = interaction.user.display_avatar.url if interaction.user.display_avatar else None
        dm_embed.set_author(name=author_name, icon_url=author_icon)
        dm_view = discord.ui.View()
        dm_view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="get-rbot", url="https://guns.lol/x0202s")) # best gunslol
        try:
            await interaction.user.send(embed=dm_embed, view=dm_view)
        except:
            pass
        await interaction.followup.send("check your dm", ephemeral=True)

class ClaimModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Claim Key")
        self.key_input = discord.ui.TextInput(label="Key", placeholder="put the key here") # si te da error al momento de claimear una key fue porque me dió pereza corregir eso
        self.add_item(self.key_input)

    async def callback(self, interaction: discord.Interaction):
        submitted = self.key_input.value.strip()
        entry = pene_keys_store.get(submitted)
        if not entry:
            await interaction.response.send_message("invalid' key", ephemeral=True)
            return
        if entry["expires_at"] < pene_now_ts():
            pene_keys_store.pop(submitted, None)
            await interaction.response.send_message("invalid' key", ephemeral=True)
            return
        if entry["claimed"]:
            await interaction.response.send_message("invalid' key", ephemeral=True)
            return
        entry["claimed"] = True
        member = interaction.guild.get_member(interaction.user.id) if interaction.guild else None
        try:
            role = interaction.guild.get_role(pene_claim_role) if interaction.guild else None
            if member and role:
                await member.add_roles(role)
        except:
            pass
        await interaction.response.send_message("congrats! you now have premium", ephemeral=True)
        channel = interaction.client.get_channel(pene_claims_channel)
        if channel:
            try:
                await channel.send(f"{interaction.user.mention} claimed a key")
            except:
                pass

class ClaimView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim a key", style=discord.ButtonStyle.success, custom_id="pene_claim_button")
    async def pene_claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ClaimModal()
        await interaction.response.send_modal(modal)

@pene_bot.event
async def on_ready():
    await pene_bot.change_presence(activity=discord.Game(name="khs x lone"))
    pene_cleanup_keys.start()
    try:
        pene_bot.add_view(GetBotView())
    except:
        pass
    try:
        pene_bot.add_view(ClaimView())
    except:
        pass
    try:
        channel_get = pene_bot.get_channel(pene_getbot_channel)
        if channel_get:
            embed_get = discord.Embed(title="Get invite", description="`click the button below to get the r-bot`", color=0x992d22)
            if pene_bot.user and pene_bot.user.display_avatar:
                embed_get.set_author(name=pene_bot.user.name, icon_url=pene_bot.user.display_avatar.url)
            try:
                await channel_get.send(embed=embed_get, view=GetBotView())
            except:
                pass
    except:
        pass
    try:
        channel_claims = pene_bot.get_channel(pene_claims_channel)
        if channel_claims:
            embed_claim = discord.Embed(title="Key System", description="Click the button below to claim your premium key. If you don't have one, check prices in idk", color=0x2fdf4f)
            embed_claim.add_field(name="Note", value="Keys expire 1 hour after generation if not claimed", inline=False)
            try:
                await channel_claims.send(embed=embed_claim, view=ClaimView())
            except:
                pass
    except:
        pass

@pene_bot.command()
async def key(ctx):
    if ctx.author.bot:
        return
    new_key = pene_generate_key()
    pene_keys_store[new_key] = {"generated_at": pene_now_ts(), "expires_at": pene_now_ts() + 3600, "claimed": False, "generated_by": ctx.author.id}
    try:
        await ctx.author.send(f"Key creada: {new_key}")
    except:
        pass
    await ctx.send("check your dm", delete_after=10)

@pene_bot.event
async def on_member_update(before, after):
    try:
        if getattr(before, "premium_since", None) is None and getattr(after, "premium_since", None) is not None:
            channel = after.guild.get_channel(pene_getbot_channel)
            if channel:
                try:
                    await channel.send(f"{after.mention}")
                except:
                    pass
                embed = discord.Embed(title="🚀 New Booster", description=f"{after.mention} is now boosting and has VIP commands.", color=0x2fdf4f)
                embed.add_field(name="Booster Role", value=f"<@&{pene_boost_role_1}>", inline=True)
                embed.add_field(name="VIP Role", value=f"<@&{pene_boost_role_2}>", inline=True)
                embed.add_field(name="User ID", value=str(after.id), inline=False)
                try:
                    embed.set_thumbnail(url=after.display_avatar.url)
                except:
                    pass
                try:
                    await channel.send(embed=embed)
                except:
                    pass
            try:
                role_a = after.guild.get_role(pene_boost_role_1)
                role_b = after.guild.get_role(pene_boost_role_2)
                if role_a:
                    await after.add_roles(role_a)
                if role_b:
                    await after.add_roles(role_b)
            except:
                pass
    except:
        pass

@tasks.loop(minutes=5)
async def pene_cleanup_keys():
    to_delete = []
    for k, v in list(pene_keys_store.items()):
        if v["expires_at"] < pene_now_ts() or v.get("claimed"):
            to_delete.append(k)
    for k in to_delete:
        pene_keys_store.pop(k, None)

pene_bot.run(pene_token)
# khs x lone
# sii chatgpt 