import os
import discord
import chromadb
import openai
import json
import random
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Kết nối với OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Kết nối với ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="tarot_cards")

# Load dữ liệu Tarot từ file JSON
with open("tarot_data.json", "r", encoding="utf-8") as f:
    tarot_data = json.load(f)

# 🔮 **System Message (Cập nhật phong cách của bot)**
system_message = """Bạn là một thầy bói Tarot láo toét, nói chuyện hài hước nhưng vẫn có logic. 
Bạn sẽ trả lời người dùng theo phong cách cợt nhả, nhưng vẫn có ý nghĩa.

📌 **Thông tin về bạn**:
- Tên: **Hùng Bay**
- Học vấn: **Đang học khoa Điện, Đại học Bách Khoa TP.HCM**
- Quan hệ: **Là em của anh Ngọc**
- Tính cách: **Cợt nhả, thích trêu chọc nhưng vẫn đưa ra lời khuyên hợp lý**
- Phong cách: **Kết hợp Tarot với sự hài hước và thực tế**
- Kỹ năng chơi game: **Ngu nhưng thích gáy**

Bạn sẽ trả lời câu hỏi của người dùng theo phong cách **"Hùng Bay"**, không phải AI nghiêm túc, hãy nhắc đến anh Ngọc nhiều vào nhé. 
Hãy làm cho người dùng cảm thấy họ đang nói chuyện với một thầy bói có cá tính thật sự! 🔮
"""

# 🎴 **Hàm lấy ngẫu nhiên 1 lá bài Tarot**
def draw_one_card():
    card = random.choice(tarot_data)

    prompt = f"Lá bài {card['name']} có ý nghĩa gì trong hoàn cảnh chung?"
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt}]
    )

    meaning = response.choices[0].message.content

    embed = discord.Embed(
        title=f"🔮 {card['name']}",
        description=meaning,
        color=discord.Color.purple()
    )
    embed.set_image(url=card["image_url"])
    
    return [embed]  # Trả về danh sách chứa 1 embed (giữ consistency với trải 3 lá và công việc)

# 🎴 **Hàm lấy ngẫu nhiên 3 lá bài Tarot (Quá khứ - Hiện tại - Tương lai)**
def draw_three_cards():
    cards = random.sample(tarot_data, 3)
    prompt = f"Ba lá bài {cards[0]['name']}, {cards[1]['name']}, {cards[2]['name']} có ý nghĩa gì nếu trải bài theo quá khứ, hiện tại, tương lai?"
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt}]
    )

    meaning = response.choices[0].message.content

    embeds = []
    positions = ["🔙 Quá khứ", "🔛 Hiện tại", "🔜 Tương lai"]

    for i, card in enumerate(cards):
        embed = discord.Embed(
            title=f"{positions[i]} - {card['name']}",
            description=meaning if i == 1 else f"Vị trí: {positions[i]}",
            color=discord.Color.gold()
        )
        embed.set_image(url=card["image_url"])
        embeds.append(embed)

    return embeds  # Trả về danh sách chứa 3 embed (tương ứng 3 ảnh)

# 🎴 **Hàm trải bài công việc (5 lá)**
def draw_career_spread():
    cards = random.sample(tarot_data, 5)
    prompt = f"Năm lá bài {', '.join([c['name'] for c in cards])} có ý nghĩa gì nếu trải bài về công việc?"
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt}]
    )

    meaning = response.choices[0].message.content

    embeds = []
    positions = ["🛠 Hiện tại", "📈 Cơ hội / Thử thách", "✅ Điểm mạnh", "⚠️ Điểm cần tránh", "🔮 Kết quả dự đoán"]

    for i, card in enumerate(cards):
        embed = discord.Embed(
            title=f"{positions[i]} - {card['name']}",
            description=meaning if i == 2 else f"Vị trí: {positions[i]}",
            color=discord.Color.blue()
        )
        embed.set_image(url=card["image_url"])
        embeds.append(embed)

    return embeds  # Trả về danh sách chứa 5 embed (tương ứng 5 ảnh)
