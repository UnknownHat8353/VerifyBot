import os
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from server import server_on
from config import *

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all(), case_insensitive=True)

@bot.event
async def on_ready():
    print(f"{bot.user.name} Ready to use!")
    await bot.change_presence(
        activity=nextcord.Streaming(name="Developer men0name", url="https://www.twitch.tv/")
    )
    bot.add_view(RoleView())


class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="กดเพื่อรับยศ", emoji="🥵", style=nextcord.ButtonStyle.blurple, custom_id="verify_role"
    )
    async def give_role(self, button: nextcord.Button, interaction: nextcord.Interaction):
        role_id = RoleID  
        role = nextcord.utils.get(interaction.guild.roles, id=role_id)

       
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message(
                "> ❌ บอทไม่มีสิทธิ์ในการจัดการยศ!", ephemeral=True
            )
            return

       
        if role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message(
                "> ❌ ยศที่ต้องการเพิ่มสูงกว่ายศของบอท!", ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "> ⚠️ คุณมียศนี้อยู่แล้ว!", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "> ✅ เพิ่มยศให้คุณเรียบร้อยแล้ว!", ephemeral=True
            )



@bot.slash_command(name="setup_role", description="[admin] ตั้งค่าหน้ารับยศ")
async def setup_role(interaction: nextcord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "> ❌ คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้!", ephemeral=True
        )
        return

    embed = nextcord.Embed(
        title="📋 __**ระบบยืนยันตัวตน**__",
        description="กดปุ่มด้านล่างเพื่อรับยศเข้าสู่เซิร์ฟเวอร์!",
        color=nextcord.Color.blue(),
    )
    embed.set_image(url="https://c.tenor.com/JbnLKar05tAAAAAC/tenor.gif") # ใส่รูปเอา

    await interaction.response.send_message("✅ ตั้งค่าหน้ารับยศเรียบร้อยแล้ว!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=RoleView())

server_on()

bot.run(os.getenv('TOKEN'))