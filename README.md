# 基于 GitHub 的自动化音乐仓库

本仓库用于维护博客播放器歌曲资源，并自动生成 APlayer 可直接使用的 `musicList.json`。

当前已支持两种工作模式：

1. 本地脚本模式：手动运行 `test.py`。
2. GitHub Actions 模式：上传音乐后自动更新 `musicList.json`。

## 支持格式

- 音频：`mp3`、`m4a`、`flac`、`wav`、`ogg`、`aac`
- 歌词：同名 `.lrc`
- LRC 时间戳：生成脚本会自动规范化为 APlayer 兼容格式
  `[mm:ss]`、`[mm:ss.xx]` 或 `[mm:ss.xxx]`。例如
  `[02:54.4]` 会写回为 `[02:54.400]`，`[01:15.979996]`
  会写回为 `[01:15.980]`。

## 目录结构

```text
.
├─ musics/               # 音频 + 同名 .lrc
├─ lrc/                  # 可选：原始歌词 .txt（仅本地生成 lrc 时使用）
├─ Baks/                 # 本地备份目录
├─ musicList.json        # 生成结果
├─ test.py               # 生成脚本
└─ .github/workflows/
     └─ music-sync.yml     # 自动化 workflow
```

## 音乐命名规范

```text
<音乐名>-<歌手>.<后缀名>
<音乐名>-<歌手>.lrc
```

建议与脚本保持一致：

- 一个音频文件对应一个同名 `.lrc`
- 避免特殊命名导致浏览器 URL 编码混乱

## 本地使用

将音频和同名歌词放入 `musics/` 后，运行：

```bash
python test.py
```

默认行为：

1. 扫描 `musics/` 音频文件，生成 `musicList.json`。
2. 规范化已有或新生成 `.lrc` 的时间戳，避免 APlayer 跳过歌词行。
3. 若缺失 `.lrc`，会尝试调用 `lrcgen` 自动生成（本地模式）。
4. 生成 JSON 备份到 `Baks/`。

### 可选环境变量

`test.py` 支持以下开关：

- `CI=true`：启用 CI 友好默认值。
- `SKIP_LRC_GENERATION=true`：跳过自动生成歌词。
- `REQUIRE_LRC=true`：若存在缺失同名 `.lrc`，脚本失败退出。
- `DISABLE_BAK=true`：不写入 `Baks/`。

CI 中建议使用：

```bash
CI=true SKIP_LRC_GENERATION=true REQUIRE_LRC=true DISABLE_BAK=true python test.py
```

## GitHub Actions 自动化（已实现）

workflow 文件：`.github/workflows/music-sync.yml`

触发条件：

- push 到 `main` 且涉及以下路径：
    - `musics/**`
    - `lrc/**`
    - `test.py`
    - `.github/workflows/music-sync.yml`
- 手动触发 `workflow_dispatch`

执行流程：

1. 使用 CI 参数运行 `test.py`。
2. 若 `musicList.json` 或 `musics/` 下规范化后的歌词有变化，自动提交并推送。

## 与博客仓库联动

无需任何同步 workflow：博客播放器在页面运行时直接 fetch 本仓库的
`musicList.json`（raw URL 开放 CORS，CDN 缓存约 5 分钟），所以新歌入库后
几分钟内自动出现在博客上，博客侧零构建、零提交。博客侧实现见
`lihan3238.github.io` 仓库的 `layouts/_partials/music.html`，形状与下方
示例一致。

## APlayer 基础配置示例（直接读取 JSON）

```html
<script>
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
                audio: data
            });
        });
</script>
```
