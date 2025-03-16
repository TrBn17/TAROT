import json

# Load dữ liệu Tarot
with open("tarot_data.json", "r", encoding="utf-8") as f:
    tarot_data = json.load(f)

print("🔍 Kiểm tra URL ảnh trong dữ liệu Tarot...")

for card in tarot_data:
    if not card["image_url"].startswith("http"):
        print(f"❌ URL không hợp lệ: {card['image_url']} ({card['name']})")
    else:
        print(f"✅ Ảnh hợp lệ: {card['image_url']} ({card['name']})")
