# Zero-budget Cartoon Gym Shorts Automation

A starter GitHub Actions project that creates one minimalist cartoon gym Short per day, then waits for your manual approval before creating the final export.

## Important reality check
- This starter uses procedural 2D drawings and simple animation, not a generative video model. It is free and repeatable, but the visuals are simpler than a hand-animated reference video.
- GitHub Actions runs on a schedule, subject to GitHub's usage limits and scheduled-job delays.
- The daily workflow creates a **preview MP4** and a `script.json` artifact. You review it, then manually run the approval workflow to create the final MP4.
- It does **not** automatically upload to YouTube.
- The repository should be public if you want to minimize GitHub Actions costs. Check current GitHub plan limits before enabling frequent workflows.

## 1. Create the repository
1. On GitHub, create a repository named `gym-shorts-automation`.
2. For a zero-cost setup, choose **Public** (do not upload secrets or private material).
3. Add these files from this project, preserving the folder structure.
4. Commit to the `main` branch.

## 2. Enable Actions
Open **Settings → Actions → General** and allow GitHub Actions to run. The workflows need only repository read/write access for uploading artifacts; they do not need a personal access token.

## 3. Daily preview
The workflow `Daily Preview` runs every day at 08:00 UTC (13:30 IST) and can also be started manually:
- Open **Actions → Daily Preview → Run workflow**.
- After it completes, open the run and download the `daily-preview` artifact.
- Watch `preview.mp4` and inspect `script.json`.

## 4. Approve and export
When you are happy with the preview:
1. Open **Actions → Approve & Export → Run workflow**.
2. Enter the exact run ID of the Daily Preview run in `source_run_id`.
3. Set `approve` to `true`.
4. Run it. The workflow downloads that preview's `script.json`, then renders a clean final `final.mp4` artifact.

This is a lightweight approval gate, not an enterprise security boundary. Do not put sensitive content in the repository.

## 5. Customize
- Edit `scripts/story.py` to add or change categories, story templates, dialogue, or captions. It currently rotates across everyday life, school, office/money, relationships, friends, gaming/tech, family, gym, food, social awkwardness, online shopping, and pets.
- Edit `scripts/render.py` to change colors, dimensions, character shapes, timing, or animation.
- Default output is 720×1280 at 12 fps for faster free cloud rendering. Change `W`, `H`, `FPS`, and `DURATION` in `scripts/render.py` if needed.
- Add only audio you own or have permission to use. This starter intentionally uses no copyrighted music.

## Troubleshooting
- If a scheduled run does not start exactly on time, that is normal for GitHub Actions schedules.
- If the export workflow cannot find an artifact, verify that `source_run_id` is the numeric run ID of a successful `Daily Preview` run and that the artifact has not expired.
- If a job fails, open the run → failed job → logs.
