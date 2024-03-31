import os
import datetime
import shutil

# 指定目录路径
directory_path = "./musics/"  # 请将路径替换为实际的目录路径

# 指定备份目录
bak_path = "./Baks/"  # 请将路径替换为实际的目录路径

# 构建URL的基本部分
base_url = "https://github.com/lihan3238/music/raw/main/musics/"  # 请将路径替换为实际的目录路径
base_lrc_url = "https://raw.githubusercontent.com/lihan3238/music/main/musics/"  # 请将路径替换为实际的目录路径
# 获取目录中的所有文件名
file_names = [
    file
    for file in os.listdir(directory_path)
    if os.path.isfile(os.path.join(directory_path, file))
]

# 初始化文件内容
file_content = ""

# 遍历文件名，并构建文件内容
for file_name in file_names:
    # 如果文件后缀为.lrc，则跳过
    if file_name.endswith(".lrc"):
        continue

    # 构建.lrc文件名
    lrc_file_name = os.path.splitext(file_name)[0] + ".lrc"

    # 如果存在对应的.lrc文件，则构建lrc_url
    lrc_url = base_lrc_url + lrc_file_name if lrc_file_name in file_names else ""

    # 提取文件名和后缀名
    name, extension = os.path.splitext(file_name)

    # 如果文件名包含 "-" 或 " - "
    if "-" in name:
        # 根据分隔符截取文件名
        parts = name.split("-")
        # 第一部分作为 "name"，第二部分以后的内容作为 "artists"
        name = parts[0].strip()
        artists = "-".join(parts[1:]).strip()
    else:
        artists = ""  # 如果没有分隔符，将 "artists" 置为空

    # 构建URL
    url = f"{base_url}{file_name}"

    # 构建文件内容行
    file_content += f"{{\nname: '{name}', url: '{url}', artist: '{artists}', cover: 'https://user-images.githubusercontent.com/140466644/266218167-0a08d24b-2f75-4a6b-9253-227612dffa98.png'"

    # 如果存在对应的.lrc文件，则添加lrc_url
    if lrc_url:
        file_content += f", lrc: '{lrc_url}'"

    file_content += "\n},\n"

# 读取musicList.md文件内容
with open("musicList.md", "r", encoding="utf-8") as musicList_file:
    musicList_content = musicList_file.read()

# 获取当前日期
current_date = datetime.date.today().strftime("%Y.%m.%d")

# 构建要写入的内容
new_content = f"# music\nmy favorate musics\n{current_date} 更新\n\n## 列表\n```js\n{file_content}\n```"


# 如果备份文件超过6个，找到最旧的备份文件并删除
bak_files = os.listdir(bak_path)
if len(bak_files) > 5:
    print("备份文件超过6个，正在删除最旧的备份文件...")
    oldest_file = min(
        bak_files, key=lambda x: os.path.getctime(os.path.join(bak_path, x))
    )
    os.remove(os.path.join(bak_path, oldest_file))

current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
backup_file = f"musicList_{current_date_time}.md"
shutil.copy("musicList.md", os.path.join(bak_path, backup_file))
print(f"已备份为 {backup_file}")


# 将更新后的内容写回到musicList.md文件中
with open("musicList.md", "w", encoding="utf-8") as musicList_file:
    musicList_file.write(new_content)

print("文件名已写入到musicList.md文件中。")
