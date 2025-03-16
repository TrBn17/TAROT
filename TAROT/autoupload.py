import os
import requests
import json

# Webhook URL của bạn
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1350845526580662282/MicC5CZCC6Ex9HBKDhni2RLcRWWxiO1wo-35S0t-jXsadp4OwvH6wlYvj0xWeOQqLNQk"

# Thư mục chứa ảnh Tarot (cả forward và reverse)
IMAGE_FOLDERS = ["forward", "reverse"]

# Lấy danh sách ảnh từ cả hai thư mục
image_files = []
for folder in IMAGE_FOLDERS:
    folder_path = os.path.join(os.getcwd(), folder)  # Đảm bảo đường dẫn tuyệt đối
    if os.path.exists(folder_path):  # Kiểm tra nếu thư mục tồn tại
        for file in os.listdir(folder_path):
            if file.endswith((".png", ".jpg", ".jpeg")):
                image_files.append((folder, os.path.join(folder_path, file)))

# Upload ảnh lên Discord Webhook
uploaded_urls = {}

for folder, file_path in image_files:
    with open(file_path, "rb") as file:
        response = requests.post(
            WEBHOOK_URL,
            files={"file": file},
            data={"content": f"🔮 Lá bài từ `{folder}`: {os.path.basename(file_path)}"}
        )

    if response.status_code == 200:
        uploaded_url = response.json()["attachments"][0]["url"]
        uploaded_urls[os.path.basename(file_path)] = uploaded_url
        print(f"✅ Đã upload: {file_path} → {uploaded_url}")
    else:
        print(f"❌ Lỗi khi upload: {file_path} → {response.status_code} - {response.text}")

# Lưu URL vào file JSON để dùng sau
with open("image_links.json", "w", encoding="utf-8") as f:
    json.dump(uploaded_urls, f, indent=4)

print("✅ Hoàn tất upload! Link ảnh đã lưu vào `image_links.json`.")
