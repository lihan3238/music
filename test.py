import os

# 指定目录路径
directory_path = './musics/'  # 请将路径替换为实际的目录路径
file_path = './'

# 构建URL的基本部分
base_url = 'https://github.com/lihan3238/music/raw/main/musics/'

# 初始化文件内容
file_content = ''

# 获取目录中的所有文件名
file_names = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

# 遍历文件名，并构建文件内容
for file_name in file_names:
    # 提取文件名和后缀名
    name, extension = os.path.splitext(file_name)
    
    # 如果文件名包含 "-" 或 " - "
    if "-" in name:
        # 根据分隔符截取文件名
        parts = name.split("-") 
        # 第一部分作为 "name"，第二部分以后的内容作为 "artists"
        name = parts[0].strip()
        artists = " - ".join(parts[1:]).strip()
    else:
        artists = ''  # 如果没有分隔符，将 "artists" 置为空
    
    # 构建URL
    url = f"{base_url}{file_name}"
    
    # 构建文件内容行
    file_content += f"name: '{name}', url: '{url}', artists: '{artists}', cover: 'https://user-images.githubusercontent.com/140466644/266218167-0a08d24b-2f75-4a6b-9253-227612dffa98.png'\n"

# 将文件内容写入到1.txt文件中
with open(os.path.join(file_path, '1.txt'), 'w', encoding='utf-8') as file:
    file.write(file_content)

print('文件名已写入到1.txt文件中。')
