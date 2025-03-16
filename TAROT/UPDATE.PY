import json
import os
# Load danh sách link ảnh đã upload
with open("image_links.json", "r", encoding="utf-8") as f:
    image_links = json.load(f)

# Load tarot data
with open("tarot_data.json", "r", encoding="utf-8") as f:
    tarot_data = json.load(f)

# Cập nhật URL ảnh trong tarot_data
for card in tarot_data:
    file_name = os.path.basename(card["image_url"])  # Lấy tên file ảnh
    if file_name in image_links:
        card["image_url"] = image_links[file_name]  # Cập nhật URL mới

# Lưu lại dữ liệu Tarot
with open("tarot_data.json", "w", encoding="utf-8") as f:
    json.dump(tarot_data, f, indent=4)

print("✅ Đã cập nhật URL ảnh trong `tarot_data.json`!")
