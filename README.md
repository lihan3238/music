# 基于github的自动化音乐仓库
本仓库作为个人音乐仓库，能够生成包含 `歌名` `链接` `歌手` `图片` 的歌曲列表，方便在线播放与存储分享。
## 支持：
`mp3` `m4a` `flac`等格式
## 使用：
创建公开仓库后，在根目录下创建`musics`、`Baks`目录，`musicList.md`文件，复制本仓库的[test.py](/test.py)到根目录下,并将`base_url = 'https://github.com/<GitHub用户名>/<仓库名>/raw/main/musics/'`即可完成仓库基础配置
将音乐文件直接复制到[musics](/musics/)目录下，然后运行主目录下的[test.py](/test.py)即可更新包含 `歌名` `链接` `歌手` `图片` (可以通过修改`file_content`变量自定义)的[歌曲列表]到[musicList.md](/musicList.md)文档中
Baks目录用于存放音乐列表的备份,在意外修改时便于恢复.
每次新增音乐,直接放在`musics`目录下,运行`test.py`即可更新`musicList.md`文件
## 音乐文件格式：
<音乐名>-<歌手>.<后缀名>
- 不得含有空格
## 配置：
通过修改代码中的：
- `file_content`    # 自定义每一条音乐的信息
- `base_url`        # 根据个人github仓库名修改