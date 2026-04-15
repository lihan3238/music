# 基于 GitHub 的自动化音乐仓库

本仓库用于维护博客播放器歌曲资源，并自动生成 APlayer 可直接使用的 `musicList.json`。

当前已支持两种工作模式：

1. 本地脚本模式：手动运行 `test.py`。
2. GitHub Actions 模式：上传音乐后自动更新 `musicList.json`，并可触发博客仓库同步。

## 支持格式

- 音频：`mp3`、`m4a`、`flac`、`wav`、`ogg`、`aac`
- 歌词：同名 `.lrc`

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
2. 若缺失 `.lrc`，会尝试调用 `lrcgen` 自动生成（本地模式）。
3. 生成 JSON 备份到 `Baks/`。

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
2. 若 `musicList.json` 有变化，自动提交并推送。
3. 若配置了 `BLOG_REPO_DISPATCH_TOKEN`，自动向博客仓库发送 `repository_dispatch`（事件：`music_list_updated`）。

## 与博客仓库联动

本仓库已提供博客侧模板文件：

- `integration/blog/blog-sync-workflow.yml`
- `integration/blog/update_aplayer_music.py`

详细改造步骤见：`AUTOMATION_SETUP.md` 和 `integration/blog/BLOG_INTEGRATION_GUIDE_ZH.md`。

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
                music: data
            });
        });
</script>
```