import chromadb

# Kết nối với ChromaDB
client = chromadb.PersistentClient(path="./chromadb")
# Lấy collection
collection = client.get_collection(name="tarot_cards")

# Kiểm tra số lượng vector trong collection
count = collection.count()
print(f"📊 Số lượng vector trong collection `tarot_cards`: {count}")
