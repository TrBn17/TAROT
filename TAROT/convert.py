import json

#đọc dữ liệu từ txt
with open("data.txt","r",encoding="utf-8") as f:
    data=f.read()
#tách json riêng lẻ
json_objects= data.strip().split("\n") #nếu mỗi dòng là 1json

parse_data = []
for obj in json_objects:
    try:
        parse_data.append(json.loads(obj))
    except json.JSONDecodeError as e:
        print(f"Lỗi ở dòng:{obj}, Error={e}")

with open("data.json","w",encoding="utf-8") as f:
    json.dump(parse_data,f, ensure_ascii=False, indent=4)
print("success tranf")