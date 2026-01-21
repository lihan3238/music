# 基于github的自动化音乐仓库

本仓库作为个人音乐仓库，能够生成包含 `歌名` `链接` `歌手` `图片` `歌词`的歌曲列表（JSON 格式），方便在线播放与存储分享。

## 支持：

`mp3` `m4a` `flac` `lrc`等格式

## 使用：

创建公开仓库后，在根目录下创建`musics`、`Baks`、`lrc`目录，复制本仓库的[test.py](/test.py)到根目录下,并将`base_url`等变量修改为你的仓库路径即可完成仓库基础配置。

将音乐文件直接复制到[musics](/musics/)目录下，将歌词文本文件（.txt）复制到`lrc`目录下（文件名需与音乐文件同名），然后运行主目录下的[test.py](/test.py)即可：
1. 更新[musicList.json](/musicList.json)文件，其中包含所有音乐的元数据。
2. 自动检查是否有对应的 `.lrc` 文件。如果没有，且在 `lrc/` 目录下存在对应的 `.txt` 歌词文本，脚本将调用 `lrcgen` 自动生成对应的 `.lrc` 文件并保存到 `musics/` 目录。
3. `Baks`目录用于存放音乐列表的备份,在意外修改时便于恢复.

每次新增音乐,直接放在`musics`目录下,运行`test.py`即可更新。

## 环境要求

- Python 3
- `lrcgen` (如果需要自动生成歌词): `pip install lrcgen` 以及 `ffmpeg` 环境。

## 音乐文件格式：

<音乐名>-<歌手>.<后缀名>
<音乐名>-<歌手>.lrc

- 不含有空格

## 配置：

- aplayer 基础配置

```html
<!DOCTYPE html>
<html>

<head>
    <!-- require APlayer -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.css">
    <script src="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.js"></script>
    <!-- require MetingJS -->
    <script src="https://cdn.jsdelivr.net/npm/meting@2.0.1/dist/Meting.min.js"></script>
</head>

<body>
    <div class="demo">
        <div id="player1">
        </div>
    </div>
    <script>
        // 示例：使用 fetch 加载 musicList.json
        fetch('https://raw.githubusercontent.com/<GitHub用户名>/<仓库名>/main/musicList.json')
            .then(response => response.json())
            .then(data => {
                var ap = new APlayer({
                    element: document.getElementById('player1'),
                    fixed: true,
                    autoplay: false,
                    mini: true,
                    theme: '#f8f4fc',
                    loop: 'all',
                    order: 'random',
                    preload: 'auto',
                    volume: 0.4,
                    mutex: true,
                    listFolded: true,
                    listMaxHeight: '500px',
                    lrcType: 3,
                    music: data // 直接使用加载的 json 数据
                });
            });
    </script>
</body>

```

通过修改代码中的：
- `directory_path`  # 音乐文件目录
- `lrc_txt_path`    # 歌词文本目录
- `base_url`        # 音乐文件 URL 前缀
- `base_lrc_url`    # 歌词文件 URL 前缀