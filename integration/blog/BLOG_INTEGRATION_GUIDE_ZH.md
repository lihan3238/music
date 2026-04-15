# 博客仓库改造指南（详细版）

本文说明如何把 `lihan3238/music` 的自动生成结果，自动同步到博客仓库 `lihan3238/lihan3238.github.io` 的 `layouts/partials/music.html`。

## 目标

当 `music` 仓库新增或更新音乐后：

1. `music` 仓库自动更新 `musicList.json`
2. 自动向博客仓库发送 `repository_dispatch`
3. 博客仓库自动拉取最新 `musicList.json`
4. 只替换 `layouts/partials/music.html` 中音乐数组
5. 自动创建 PR 到 `main`

## 你需要在博客仓库做的改动

### 第 1 步：添加 workflow

把 `music` 仓库中的文件复制到博客仓库：

- 来源：`integration/blog/blog-sync-workflow.yml`
- 目标：`.github/workflows/blog-sync-music.yml`

这个 workflow 负责监听 `music_list_updated` 事件并发起更新 PR。

### 第 2 步：添加更新脚本

把 `music` 仓库中的文件复制到博客仓库：

- 来源：`integration/blog/update_aplayer_music.py`
- 目标：`scripts/update_aplayer_music.py`

这个脚本会：

1. 下载 `https://raw.githubusercontent.com/lihan3238/music/main/musicList.json`
2. 在目标文件中寻找标记区域
3. 只替换标记区域内的 `music: [...]`

### 第 3 步：给 music partial 增加替换标记

编辑博客仓库 `layouts/partials/music.html`，在当前 `music: [...]` 的位置加上两个标记。

必须是以下两行（大小写一致）：

- `// MUSIC_LIST_START`
- `// MUSIC_LIST_END`

示例（结构示意）：

```javascript
var ap = new APlayer({
    element: document.getElementById('player1'),
    fixed: true,
    autoplay: false,
    mini: true,
    // ... 你的其它配置
    lrcType: 3,
    // MUSIC_LIST_START
    music: [
      {
        "name": "demo",
        "url": "https://example.com/demo.mp3",
        "artist": "demo"
      }
    ]
    // MUSIC_LIST_END
});
```

注意：

1. 只在 `music` 数组区域加标记，不要包住整个脚本。
2. 标记必须唯一，文件里只出现一组。

### 第 4 步：确认 workflow 中目标路径

在 `.github/workflows/blog-sync-music.yml` 中默认是：

- `TARGET_FILE: layouts/partials/music.html`

如果你后续改了 partial 路径，记得同步修改 `TARGET_FILE`。

## 事件与权限

博客 workflow 监听：

- `repository_dispatch`（type: `music_list_updated`）
- `workflow_dispatch`（手动补跑）

博客仓库不需要额外 PAT 才能创建 PR，因为 workflow 使用仓库默认 `GITHUB_TOKEN`，并已声明：

- `contents: write`
- `pull-requests: write`

## 验证流程（建议按顺序）

1. 在博客仓库先手动运行一次 `Sync Music Player List`（Actions 页）
2. 确认能成功创建 PR
3. 检查 PR diff：仅 `layouts/partials/music.html` 的音乐数组变更
4. 合并 PR，确认页面播放器工作正常
5. 再去 `music` 仓库提交一首新歌 + 同名 lrc
6. 观察是否自动触发博客仓库 PR

## 常见问题

### 1) 报错 Markers not found

原因：`layouts/partials/music.html` 缺少以下标记：

- `// MUSIC_LIST_START`
- `// MUSIC_LIST_END`

处理：按上面第 3 步加上即可。

### 2) 没有收到 dispatch

在 `music` 仓库检查 secret：

- 名称：`BLOG_REPO_DISPATCH_TOKEN`

若未配置，`music` workflow 会跳过 dispatch。

### 3) PR 没创建

检查博客 workflow 日志是否显示：

- `No changes detected in target file.`

这代表音乐列表内容一致，无需新 PR。

## 可选增强

1. 将 PR 标题加上日期或 source sha，便于审计。
2. 在博客 workflow 增加标签，如 `music-sync`。
3. 如需避免大文件差异，可将播放器改为前端 fetch `musicList.json`（不再内嵌超长数组）。
