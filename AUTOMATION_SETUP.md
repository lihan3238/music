# Music to Blog Automation Setup

This repository now includes the first implementation for automatic sync.

## What Is Implemented

1. Music-side workflow: `.github/workflows/music-sync.yml`
   - Trigger: pushes to `musics/**`, `lrc/**`, `test.py`, or manual run.
   - Action: run `python test.py` in CI mode.
   - CI mode behavior:
     - Do not auto-generate `.lrc` files.
     - Require matching `.lrc` for each audio file.
     - Disable backup writes to `Baks/`.
   - If `musicList.json` changed:
     - Commit and push the new JSON.
     - Send `repository_dispatch` event to blog repo.

2. Blog-side templates (copy these into your blog repo):
   - `integration/blog/blog-sync-workflow.yml`
   - `integration/blog/update_aplayer_music.py`

## One-Time Setup

### 1) Configure secret in the `music` repository

Create repository secret in `lihan3238/music`:

- Name: `BLOG_REPO_DISPATCH_TOKEN`
- Value: a PAT that can trigger dispatch on `lihan3238/lihan3238.github.io`

Recommended PAT permissions (fine-grained):
- Repository access: `lihan3238/lihan3238.github.io`
- Permissions:
  - Actions: Read and write
  - Contents: Read-only

### 2) Add blog-side workflow and script

In the blog repository (`lihan3238/lihan3238.github.io`):

1. Copy `integration/blog/blog-sync-workflow.yml` to:
   - `.github/workflows/blog-sync-music.yml`
2. Copy `integration/blog/update_aplayer_music.py` to:
   - `scripts/update_aplayer_music.py`

### 3) Add markers in blog partial

In `layouts/partials/music.html`, wrap your `music: [...]` block with markers:

```javascript
// MUSIC_LIST_START
music: [
  ... existing list ...
]
// MUSIC_LIST_END
```

The updater script replaces only the content between these two markers.

## How It Works End-to-End

1. You push new files to `musics/` and matching `.lrc` to `musics/`.
2. `music-sync.yml` regenerates `musicList.json`.
3. If changed, it commits JSON and dispatches event `music_list_updated`.
4. Blog workflow receives event, updates `layouts/partials/music.html`, and creates a PR to `main`.

## Manual Recovery

- In `music` repo: run workflow `Music List Sync` manually from Actions tab.
- In blog repo: run `Sync Music Player List` manually from Actions tab.

## Notes

- If any audio file has no matching `.lrc`, CI fails by design.
- If you want to allow missing `.lrc`, set `REQUIRE_LRC=false` in workflow env.
- If your blog target path changes, set `TARGET_FILE` in blog workflow env.
