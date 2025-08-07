import discord
from discord import app_commands
from discord.ext import commands

import json

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
GUILD_ID = config["GUILD_ID"]  # Tu servidor de Discord (int)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔁 Sincronizados {len(synced)} comandos slash")
    except Exception as e:
        print(e)

# Comando solo para STAFF (Admins o Mods)
@bot.tree.command(name="anuncio", description="📢 Enviar un anuncio embed al canal")
@app_commands.checks.has_any_role("Admin", "Moderador")
@app_commands.describe(titulo="Título del anuncio", mensaje="Contenido del mensaje")
async def anuncio(interaction: discord.Interaction, titulo: str, mensaje: str):
    embed = discord.Embed(title=titulo, description=mensaje, color=0x00ffcc)
    embed.set_footer(text="Anuncio del Staff")
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Anuncio enviado", ephemeral=True)

# Comando de ejemplo para packs por niveles
@bot.tree.command(name="packs", description="🎁 Ver recompensas por niveles")
async def packs(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**🎚️ Recompensas por Nivel:**\n"
        "🥉 Nivel 5: 5 mashups exclusivos\n"
        "🥈 Nivel 10: 10 extended edits + PDF\n"
        "🥇 Nivel 20: Pack de intros + eventos\n"
        "🏆 Nivel 30+: Packs mensuales exclusivos\n"
        "⭐ Y más... ¡Sigue participando!", ephemeral=True
    )

bot.run(TOKEN)