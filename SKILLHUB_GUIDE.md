# SkillHub 上传指南

## 上传到 WorkBuddy SkillHub

### 方法1：通过 CLI 安装（推荐）

```bash
# 在 WorkBuddy 中使用 SkillHub CLI
skillhub install universal-video-doc

# 或者从本地文件夹安装
skillhub install ./skill-upload-ready
```

### 方法2：手动安装

1. 将整个文件夹复制到 WorkBuddy 技能目录：
   - Windows: `C:\Users\<用户名>\.workbuddy\skills\`
   - macOS/Linux: `~/.workbuddy/skills/`

2. 在 WorkBuddy 中使用：
   ```
   @skill:universal-video-doc
   ```

### 方法3：发布到 SkillHub 市场

1. 访问 https://skillhub.codebuddy.cn
2. 登录你的 WorkBuddy 账号
3. 点击 "发布技能"
4. 填写技能信息：
   - 技能名称：`universal-video-doc`
   - 技能描述：`通用视频课程学习文档生成器，支持CS/数学/物理/医学等所有专业`
   - 分类：`教育` / `文档生成`
   - 标签：`视频`, `学习`, `文档`, `AI`, `教育`
5. 上传整个 `skill-upload-ready` 文件夹
6. 等待审核通过

---

## 上传到 GitHub

### 步骤1：创建 GitHub 仓库

1. 登录 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - Repository name: `universal-video-learning-doc`
   - Description: `Universal Video Learning Document Generator - Convert any subject's video courses into structured learning documents`
   - 选择 Public（公开）
   - 勾选 "Add a README file"
4. 点击 "Create repository"

### 步骤2：推送代码

```bash
cd D:\workbuddy工作存储\2026-05-17-task-24\skill-upload-ready

# 初始化 Git 仓库
git init
git add .
git commit -m "Initial release: Universal Video Learning Document Generator"

# 连接远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/your-username/universal-video-learning-doc.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤3：添加 GitHub Topics

在仓库页面点击 "⚙️ Settings" → "General" → 添加 Topics：
- `video-processing`
- `learning`
- `document-generation`
- `ai`
- `whisper`
- `bilibili`
- `education`
- `study-notes`

### 步骤4：创建 Release

```bash
# 打标签
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

然后在 GitHub 网页上：
1. 进入仓库 → "Releases" → "Create a new release"
2. 选择 tag: `v1.0.0`
3. 标题：`v1.0.0 - Initial Release`
4. 描述：
   ```
   ## Features
   - Multi-subject support (CS, Math, Physics, Medicine, Law, Design, etc.)
   - Whisper speech recognition
   - OCR code recognition
   - AI content analysis
   - Bilibili integration
   - Auto screenshot generation
   
   ## Installation
   ```bash
   pip install -r requirements.txt
   python scripts/check_dependencies.py
   ```
   ```
5. 点击 "Publish release"

---

## 技能元数据建议

在 SKILL.md 中添加以下 frontmatter，使其更容易被发现：

```yaml
---
name: universal-video-doc
version: 1.0.0
description: 通用视频课程学习文档生成器，支持所有专业
author: Your Name
category: 教育
tags: [视频, 学习, 文档, AI, 教育, 课程]
difficulty: intermediate
platform: [windows, macos, linux]
---
```

---

## 推广建议

1. **写一篇介绍文章** 发布到：
   - 掘金
   - CSDN
   - 知乎
   - 少数派

2. **录制演示视频** 上传到 Bilibili

3. **在 WorkBuddy 社区分享**
   - 发帖介绍这个技能
   - 分享使用案例和效果

4. **收集反馈**
   - 关注 GitHub Issues
   - 根据用户反馈持续改进
