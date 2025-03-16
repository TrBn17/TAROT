import os
import json
import tiktoken
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Khởi tạo OpenAI API
openai_client = OpenAI(api_key=OPENAI_KEY)

# Khởi tạo ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_or_create_collection(name="tarot_cards")

# Chọn tokenizer cho mô hình embeddings
tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")

# Đọc dữ liệu từ file JSON
with open("tarot_data.json", "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

# Hàm tạo nội dung embeddings từ dữ liệu lá bài
def get_card_content(card):
    return f"""
    {card.get("title_main", "")}
    {card.get("title_secondary", "")}
    Tình yêu: {card.get("title_love", "")}
    Công việc: {card.get("title_work", "")}
    Tiền bạc: {card.get("title_money", "")}
    Sức khỏe: {card.get("title_heath", "")}
    """

# Lưu embeddings vào ChromaDB
total_tokens = 0
for card in tarot_cards:
    if isinstance(card, dict):
        card_id = card.get("id", "unknown")
        card_name = card.get("name", "Không có tên")
        image_url = card.get("image_url", "")
        content = get_card_content(card)

        # Đếm token để kiểm soát chi phí
        num_tokens = len(tokenizer.encode(content))
        total_tokens += num_tokens

        # Tạo embeddings (ĐÃ FIX LỖI)
        response = openai_client.embeddings.create(
            input=content, model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding  # Truy xuất đúng cách

        # Lưu vào ChromaDB
        collection.add(
            ids=[card_id],
            embeddings=[embedding],
            metadatas=[{
                "name": card_name,
                "description": content,
                "image_url": image_url
            }]
        )

        print(f"✅ Đã lưu {card_name}: {num_tokens} tokens")

# In tổng số token đã sử dụng
print(f"\n🔥 Tổng số token đã dùng: {total_tokens}")
print("🎉 Dữ liệu đã được lưu vào ChromaDB thành công!")
