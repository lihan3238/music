# 基于github的自动化音乐仓库

本仓库作为个人音乐仓库，能够生成包含 `歌名` `链接` `歌手` `图片` `歌词`的歌曲列表，方便在线播放与存储分享。

## 支持：

`mp3` `m4a` `flac` `lrc`等格式

## 使用：

创建公开仓库后，在根目录下创建`musics`、`Baks`目录，`musicList.md`文件，复制本仓库的[test.py](/test.py)到根目录下,并将`base_url = 'https://github.com/<GitHub用户名>/<仓库名>/raw/main/musics/'`即可完成仓库基础配置
将音乐文件直接复制到[musics](/musics/)目录下，然后运行主目录下的[test.py](/test.py)即可更新包含 `歌名` `链接` `歌手` `图片` (可以通过修改`file_content`变量自定义)`歌词`的[歌曲列表]到[musicList.md](/musicList.md)文档中
Baks目录用于存放音乐列表的备份,在意外修改时便于恢复.
每次新增音乐,直接放在`musics`目录下,运行`test.py`即可更新`musicList.md`文件

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
        var ap = new APlayer
            ({
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
                music: [
                    {
                        name: 'catallena', url: 'https://github.com/lihan3238/music/raw/main/musics/catallena-橘子焦糖.mp3', artist: '橘子焦糖', cover: 'https://user-images.githubusercontent.com/140466644/266218167-0a08d24b-2f75-4a6b-9253-227612dffa98.png'
                    },
                    {
                        name: 'Escape(ThePinaColadaSong)', url: 'https://github.com/lihan3238/music/raw/main/musics/Escape(ThePinaColadaSong)-RupertHolmes.mp3', artist: 'RupertHolmes', cover: 'https://user-images.githubusercontent.com/140466644/266218167-0a08d24b-2f75-4a6b-9253-227612dffa98.png'
                    },
                ]
            });
        //ap.init();
    </script>
</body>

```

通过修改代码中的：
- `file_content`    # 自定义每一条音乐的信息
- `base_url`        # 根据个人github仓库名修改