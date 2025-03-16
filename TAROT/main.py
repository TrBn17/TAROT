import discord
import os
from dotenv import load_dotenv
from logic import draw_one_card, draw_three_cards, draw_career_spread

# Load biến môi trường
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Kiểm tra nếu thiếu token
if not DISCORD_TOKEN:
    raise ValueError("⚠️ Lỗi: DISCORD_TOKEN không tồn tại! Kiểm tra file .env")

# Khởi tạo bot với quyền nhắn tin & đọc nội dung tin nhắn
intents = discord.Intents.default()
intents.messages = True  # Nhận & gửi tin nhắn
intents.message_content = True  # Đọc nội dung tin nhắn (Cần thiết với Discord API mới)
bot = discord.Client(intents=intents)

# 🎛️ **Tạo nút bấm trải bài**
class TarotView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🃏 Bói bài 1 lá", style=discord.ButtonStyle.primary)
    async def one_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()  # Để tránh lỗi timeout
        embeds = draw_one_card()
        for embed in embeds:
            await interaction.followup.send(embed=embed)  # Dùng followup để gửi tin nhắn

    @discord.ui.button(label="🔮 Trải bài 3 lá", style=discord.ButtonStyle.secondary)
    async def three_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embeds = draw_three_cards()
        for embed in embeds:
            await interaction.followup.send(embed=embed)

    @discord.ui.button(label="💼 Trải bài công việc", style=discord.ButtonStyle.success)
    async def career_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embeds = draw_career_spread()
        for embed in embeds:
            await interaction.followup.send(embed=embed)


@bot.event
async def on_ready():
    print(f'🔮 Tarot Bot "{bot.user}" đã sẵn sàng!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Không phản hồi chính nó

    # Kiểm tra xem bot có bị mention không
    if bot.user.mentioned_in(message):
        user_question = message.content.strip().lower()
        print(f"📩 Nhận tin nhắn: {user_question} từ {message.author}")

        if any(cmd in user_question for cmd in ["bói bài", "xem tarot", "rút bài"]):
            print("🃏 Rút bài 1 lá")
            embeds = draw_one_card()
            for embed in embeds:
                await message.channel.send(embed=embed)

        elif any(cmd in user_question for cmd in ["trải bài 3 lá", "3 lá", "trải bài quá khứ hiện tại tương lai"]):
            print("🃏 Trải bài 3 lá")
            embeds = draw_three_cards()
            for embed in embeds:
                await message.channel.send(embed=embed)

        elif any(cmd in user_question for cmd in ["trải bài công việc", "công việc", "sự nghiệp"]):
            print("💼 Trải bài công việc")
            embeds = draw_career_spread()
            for embed in embeds:
                await message.channel.send(embed=embed)

        elif any(cmd in user_question for cmd in ["help", "hướng dẫn", "start"]):
            print("📜 Hiển thị hướng dẫn")
            embed = discord.Embed(
                title="📜 Hướng dẫn sử dụng Tarot Bot",
                description="Dưới đây là các lệnh bạn có thể sử dụng:",
                color=discord.Color.green()
            )
            embed.add_field(name="🃏 `bói bài`", value="Rút 1 lá bài Tarot", inline=False)
            embed.add_field(name="🔮 `trải bài 3 lá`", value="Trải bài quá khứ - hiện tại - tương lai", inline=False)
            embed.add_field(name="💼 `trải bài công việc`", value="Trải bài về sự nghiệp", inline=False)
            embed.set_footer(text="Chúc bạn có trải nghiệm bói bài vui vẻ! 🔮")
            
            await message.channel.send(embed=embed, view=TarotView())  # Gửi hướng dẫn kèm các nút bấm
bot.run(DISCORD_TOKEN)