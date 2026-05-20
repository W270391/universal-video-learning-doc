---
name: algorithm-video-doc
description: "通用视频学习笔记生成专家，适用于所有专业（计算机、数学、物理、经济学、医学、法学、设计等），专门接收网课/教程视频的音频/文字/讲解内容，全自动生成完整学习归档文档，严格覆盖视频全部知识点，适配学习、复盘、考试备考使用。"
agent_created: true
---

# Universal Video Learning Document Generator

This skill converts **any subject's** video courses/tutorials into structured learning documents. It works for computer science, mathematics, physics, economics, medicine, law, design, engineering, humanities — any field where video learning is used.

## 专业自适应机制

### Step 0: 专业识别与知识图谱构建（必须最先执行）

在处理视频之前，必须先确定视频的专业方向，并联网搜索该专业学习该主题需要覆盖哪些知识模块：

1. **从视频标题/内容/用户描述**判断专业方向
2. **联网搜索**该主题在该专业中的标准知识体系（使用 WebSearch）
   - 搜索关键词示例：`"[主题] 知识点 完整体系"`、`"[课程名] 教学大纲"`、`"[主题] 考试重点"`
   - 搜索该专业的权威教材目录，确认覆盖范围
3. **构建该视频的知识图谱**：
   - 视频覆盖了哪些知识点（标记 ✅）
   - 视频未覆盖但该主题应该包含的知识点（标记 ⚠️，需联网补充）
   - 该专业学习者最可能遇到的困难点（标记 🔴，需重点展开）
4. **将专业信息传递给后续所有步骤**，替代硬编码的 CS 特定逻辑

### 专业领域适配表

| 专业方向 | 核心板块（替代硬编码） | 需要联网搜索的内容 |
|---------|---------------------|-------------------|
| 计算机科学 | 代码实现、算法分析、复杂度 | 洛谷/LeetCode 相关题目 |
| 数学 | 公式推导、定理证明、例题演算 | 相关定理的证明思路、典型习题 |
| 物理 | 物理模型、公式推导、实验原理 | 实验步骤、物理常数、公式表 |
| 经济/金融 | 经济模型、案例分析、图表解读 | 真实案例、数据来源、政策背景 |
| 医学 | 临床表现、诊断流程、治疗方案 | 临床指南、病例数据、鉴别诊断 |
| 法学 | 法条解读、案例分析、构成要件 | 相关法条原文、经典判例 |
| 设计/艺术 | 设计流程、工具操作、审美原则 | 设计规范、配色方案、字体推荐 |
| 工程 | 公式计算、设计规范、施工流程 | 行业标准、安全规范、计算公式 |
| 语言学习 | 语法点、词汇辨析、听力技巧 | 例句扩展、文化背景、考试真题 |
| 人文社科 | 概念辨析、理论框架、批判思维 | 学术争论、不同学派观点 |

## 核心生成原则（必须遵守）

### 原则1：举例优先，绝不跳过
- **视频中提到的例子**：必须完整保留，标注原始时间戳，不可省略或一笔带过
- **视频中未提例子的概念**：必须自行构造至少一个具体例子，用数字、数组、小案例等让读者"秒懂"
- **每个核心概念**都必须配有：①视频原例（如有）+ ②自补充例（视频没讲就自己造）
- 举例格式统一为：
  ```
  **举例说明：**
  > 输入：xxx → 过程：xxx → 输出：xxx
  ```

### 原则2：小白视角，把读者当零基础
- 任何术语首次出现必须用一句话解释，不可假设读者已知
- 技术概念用**生活类比**辅助理解（如："贪心算法就像每次从一堆苹果里挑最大的"）
- 代码每行都要有注释，变量名要说明含义（如适用）
- 公式推导的每一步都要说明"这步在干什么"
- 复杂度/定量分析要附带"什么意思"的白话翻译
- 流程/步骤图要用文字先描述一遍再给出图示

### 原则3：重点标记 + 详细展开
- 每个章节结束后，用 `🔑 **重点**` 标记出最重要的3-5个知识点
- 重点知识必须额外展开：为什么重要、考试怎么考、和易混淆概念的区别
- 标记后的重点在文档末尾的「考前速查表」中再次汇总

### 原则4：自行补充省略内容
- 视频中一笔带过但对理解很重要的内容，必须用联网搜索补充完整
- 可使用 WebSearch / WebFetch 搜索权威资料、经典教材解释、可视化图解
- 补充内容用 `📝 **补充**` 标记，与视频原内容区分

### 原则5：去重控制
- 同一知识点最多在文档中出现2次（一次正文、一次总结/速查）
- 发现重复内容时自行删减，保留更详细的那个版本
- 代码如果在"逐时间笔记"和"完整代码板块"都出现，只在一处写完整版，另一处引用

### 原则6：终极目标是学会
- 不是"记录视频说了什么"，而是"让读者看完能做题"
- 每个知识点结束后附带一道「即时练习」（简短小题，可自编）
- 文档末尾附「自测清单」：列出10个问题，读者能回答说明学会了

### 原则7：生成后审查（必须执行）
文档生成完毕后，必须以**该专业小白视角**重新通读全文，执行以下审查清单：
1. **术语检查**：每个专业术语首次出现时是否有解释？如果没有，补上
2. **例子完整性**：每个概念是否都有例子？没有的立即补充（自编即可）
3. **跳跃感检查**：是否存在"突然蹦出一个概念没解释"的情况？有的话补写过渡说明
4. **代码/公式可运行性**：代码能否直接复制运行？公式是否完整（无省略步骤）？
5. **定量分析白话**：所有公式/O()表达式旁边是否有"白话翻译"？没有的补上
6. **逻辑准确性**：描述是否与实际行为一致？不一致的修正
7. **生活类比**：核心概念是否有生活类比？缺少的补充
8. **学习者困难预判**：代入该专业学习者视角，哪些地方最容易困惑？困惑处需额外展开
9. **审查结果**：在文档末尾追加一个 `## 审查记录` 小节，列出修改了哪些地方

### 原则8：临时文件清理（最后执行）
整个流程结束后，删除所有中间产物，只保留最终文档：
- 删除 `downloads/` 目录（音频文件）
- 删除 `ffmpeg_extracted/` 目录（FFmpeg临时二进制）
- 删除 `transcript.json`（Whisper转录中间文件）
- 删除 `*.zip`（下载的压缩包）
- 删除 `*.wav`、`*.m4a`、`*.mp4` 等媒体文件
- **保留**：最终生成的 `.md` 文档
- 清理前告知用户将删除哪些文件，清理后确认释放的空间

## Core Capabilities

1. **Video Audio Extraction** - Extract audio tracks from video files using FFmpeg
2. **Speech Recognition** - Convert audio to timestamped text using Whisper
3. **Screen Capture** - 基于语音关键词自动识别重点画面，Whisper转录搜索"重点/注意/关键"等词，命中的时间点自动截图
4. **AI Content Analysis** - Generate structured documentation using AI analysis
5. **Domain-Specific Resource Search** - 根据专业方向搜索相关练习题、案例、标准
6. **Example Generation** - 自动生成/补充例子，确保每个概念都有直观理解
7. **Web Search Enhancement** - 联网搜索补充视频未覆盖的重要知识点
8. **Learner Pain Point Prediction** - 代入学习者视角预判困难点并重点展开

## Required Dependencies

Before using this skill, ensure the following dependencies are installed:

### System Tools
- **FFmpeg** - For video/audio processing
  - Windows: Install via conda: `conda create -n ffmpeg_env ffmpeg -c conda-forge`
  - Or download from https://ffmpeg.org/download.html and add to PATH

- **Tesseract OCR** - For code recognition
  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
  - Add to PATH after installation

### Python Packages
```bash
pip install openai-whisper opencv-python pytesseract moviepy yt-dlp
```

## Bilibili Integration

This skill supports direct downloading from Bilibili (哔哩哔哩) without manual download.

### Supported URL Formats
- `https://www.bilibili.com/video/BV1xxxxxxxxxx?p=1` (multi-part videos)
- `https://www.bilibili.com/video/BV1xxxxxxxxxx` (single video)
- `b23.tv/xxxxx` (short links)

### Download Workflow
1. User provides Bilibili URL
2. Use yt-dlp to download audio:
   ```bash
   yt-dlp -x --audio-format wav -o "downloads/%(title)s.%(ext)s" "URL"
   ```
3. Fetch video metadata via Bilibili API:
   ```
   https://api.bilibili.com/x/web-interface/view?bvid=BVxxxxx
   ```
4. Process with Whisper for transcription

### Important Notes
- yt-dlp handles authentication cookies automatically
- Audio-only download is faster and sufficient for transcription
- For multi-part videos, specify the part number with `?p=N`

## Workflow

### Step 1: Video Analysis
1. Receive video file from user
2. Extract basic video information (duration, resolution, codec)
3. Split video into manageable segments if needed (for videos > 2 hours)

### Step 2: Audio Processing
1. Extract audio track using FFmpeg:
   ```bash
   ffmpeg -i input_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
   ```
2. Process audio with Whisper to generate timestamped transcript

### Step 3: Key Frame Extraction & Screenshots（语音关键词识别）

**3.1 语音关键词截图（必须执行）**

从Whisper转录的JSON文件中提取时间戳，搜索以下关键词，命中的时间点自动截图：

**关键词列表（中英文）：**
```
重点, 注意, 关键, 核心, 记住, 必考, 高频, 重要, 总结, 考点
必背, 易错, 常考, 难点, 总结一下, 划重点, 敲黑板
important, key, note, remember, focus, critical, summary, exam
```

**截图命令：**
```bash
# 对每个命中的时间点，在视频中截取1帧
ffmpeg -i input_video.mp4 -ss [HH:MM:SS] -vframes 1 -q:v 2 "screenshots/[序号]_[关键词]_[时间戳].jpg"
```

**输出目录：** `screenshots/`

**3.2 截图标注**

每张截图必须记录：
- 时间戳（精确到秒）
- 匹配到的关键词
- 该时间点前后5秒的转录文本（作为截图内容描述）
- 所属知识点（后续AI分析时填入）

**3.3 重要界面补充截图**

以下场景无论是否命中关键词，都必须截图：
- 公式推导过程（数学/物理/工程）
- 代码展示画面（计算机）
- PPT/板书切换瞬间（通过音量静默检测：讲师停顿>2秒时）
- 图表/数据展示（经济/医学）
- 操作步骤演示（设计/工程）

**3.4 去重合并**

- 30秒内命中多个关键词，只保留最清晰的一张
- 截图文件名格式：`[序号]_[关键词]_[MM_SS].jpg`
- 最终生成「📸 关键截图集」汇总表

### Step 4: AI Content Analysis
1. 分析转录文本，识别：
   - 核心概念和知识点
   - 公式/代码/流程（按专业类型）
   - 常见错误和技巧
   - 考试/考核要点
   - **视频中提到的例子**（必须完整保留）
   - **视频中未举例但需要补充的概念**（自行构造例子）
2. 联网搜索补充资料（如需要）
3. 生成结构化文档，严格遵循「核心生成原则」和强制模板

### Step 5: Domain Resource Search
1. 根据专业方向搜索相关资源：
   - 计算机：洛谷/LeetCode 相关题目
   - 数学：相关定理证明、典型习题
   - 物理/工程：实验步骤、计算公式表
   - 经济/金融：真实案例、数据来源
   - 医学：临床指南、病例数据
   - 法学：相关法条原文、经典判例
   - 其他专业：权威教材习题、行业标准
2. 将资源链接和摘要整合进文档

### Step 6: Document Generation
1. Generate Markdown document with mandatory structure
2. Include all timestamps, code blocks, and analysis
3. 整合截图标注（在文档中标注关键截图位置）
4. Generate animation/visual requirements for code visualization (如适用)

### Step 7: Self-Review (必须执行)
1. 以计算机小白视角重新通读全文
2. 执行审查清单（见原则7）
3. 修复所有发现的问题
4. 在文档末尾追加 `## 审查记录` 小节

### Step 8: Cleanup (必须执行)
1. 列出将要删除的临时文件清单
2. 删除 `downloads/` 目录
3. 删除 `ffmpeg_extracted/` 目录
4. 删除 `transcript.json`
5. 删除 `*.zip`、`*.wav`、`*.m4a`、`*.mp4` 等媒体文件
6. 确认最终文档完好
7. 报告清理结果和释放空间

## Document Structure (Mandatory)

The generated document MUST follow this exact structure. Sections marked with ⚙️ are **专业自适应** — 根据视频专业方向自动调整内容，而非硬编码为代码/算法。

```markdown
# [课程名称] - [章节主题] 学习文档

## 视频基础信息
- **课程名称**：
- **章节主题**：
- **专业方向**：[自动识别，如：计算机科学/数学/物理/经济/医学/法学/设计/工程/语言/人文]
- **视频时长**：
- **讲师**：
- **BV号/链接**：

### 知识图谱（联网搜索构建）
- ✅ 视频已覆盖：[知识点列表]
- ⚠️ 视频未覆盖（需补充）：[知识点列表]
- 🔴 学习者困难点：[预判的难点列表]

### 时间节点目录
- 00:00 - XX:XX: 知识点1
- XX:XX - XX:XX: 知识点2
- ...

---

## 核心知识点梳理

### 核心原理 ⚙️
[详细描述，用一句话概括核心思想]
**生活类比：** [用日常场景帮助理解]

**举例说明：**
> 输入/条件：xxx → 过程：xxx → 输出/结论：xxx

### 核心概念

#### 概念1：[名称] ⚙️
- **定义**：[一句话解释]
- **白话翻译**：[用日常语言再说一遍]
- **举例说明：**
  > [具体数字/场景例子]
- **🔑 重点**：[为什么重要 / 考试怎么考]
- **🔴 学习者常问**：[预判学习者会问什么问题，提前回答]

#### 概念2：[名称] ⚙️
[同上结构]

[每个核心概念都要有以上子项，不可省略]

### 适用场景 ⚙️
- 适用于：[场景描述 + 举例]
- 不适用于：[场景描述 + 举例]
- **与类似概念的区别**：[对比说明]

### 底层思想/方法论 ⚙️
[描述解决这类问题的通用思想/方法论，配至少一个完整小例子]

### 优缺点分析 ⚙️
**优点:**
1. [优点1 + 举例说明]
2. [优点2]

**缺点:**
1. [缺点1 + 什么情况下会出问题]
2. [缺点2]

### 关键参数/定量分析 ⚙️
- **[参数1]**: [表达式/数值] → **白话**：[什么意思]
- **[参数2]**: [表达式/数值] → **白话**：[什么意思]
- **最坏情况**: [描述 + 举例]
- **典型情况**: [描述]

### 📝 补充（视频未覆盖但重要）
[联网搜索补充的内容，标注来源]

---

## 逐时间节点详细笔记

### 【时间节点：00:00 - XX:XX】[主题]
**讲师原话:**
> "[原话内容]"

**通俗化转述:**
[用简单语言重新解释]

**举例说明：**
> [视频中的例子，或自补充的例子]

**📸 关键截图：**
> [截图时间点 + 内容描述]

**重点干货:**
- [要点1]
- [要点2]

**即时练习：**
> [基于本节内容的一道小题]

### 【时间节点：XX:XX - XX:XX】[主题]
[同上结构]

---

## 核心板块（专业自适应）⚙️

> 以下板块根据专业方向自动选择，非所有板块都出现

### [板块类型A]: [名称] ⚙️
[根据专业选择：代码实现 / 公式推导 / 实验步骤 / 案例分析 / 法条解读 / 设计流程 / 操作步骤 等]

**完整内容:**
```[language]
// 完整可运行/可复现的内容
```

**逐行/逐步注释:**
[每行/每步都要有注释]

**设计逻辑:**
[为什么这样做，思考过程]

**举例运行/演示：**
> 输入：xxx → 每步变化：xxx → 输出：xxx

### [板块类型B]: [名称] ⚙️
[同上，根据需要出现]

---

## 问题解决思路深度解析 ⚙️

### 通用思考流程
1. **理解问题/概念**: [步骤 + 举例]
2. **选择方法/策略**: [步骤 + 举例]
3. **执行/推导**: [步骤]
4. **验证/检验**: [步骤 + 举例]

### 正向推导逻辑
[从问题出发，逐步推导，每步配小例子]

### 反向复盘逻辑
[从结果出发，逆向分析]

### 同类问题通用模板 ⚙️
[根据专业提供：代码模板 / 公式模板 / 分析框架 / 操作流程 等]

---

## 常见错误 & 避坑指南 ⚙️

### 易错点1: [名称]
**错误示例:**
[错误的代码/公式/操作/理解]

**错误原因:**
[为什么会犯这个错]

**举例说明：**
> 错误情况 → 错误结果 → 为什么错

**正确做法:**
[正确的内容]

**发现与纠正:**
[怎么发现自己错了，怎么改]

---

## 注意事项 & 考点总结 ⚙️

### 边界条件/前提假设
1. [条件1 + 举例]
2. [条件2 + 举例]

### 高频考点
1. **考点1**: [描述 + 考法]
2. **考点2**: [描述 + 考法]

### 易混淆知识点
| 概念A | 概念B | 区别 | 举例 |
|-------|-------|------|------|
| xxx | xxx | xxx | xxx |

---

## 🔑 重点速查表
[从全文提取最重要的5-8个知识点，每个一句话 + 一个关键词]

---

## 📝 自测清单
回答以下问题，全对说明你学会了：
1. [问题1]
2. [问题2]
...
10. [问题10]

---

## 📸 关键截图集
按时间顺序整理视频中的重要截图：
- [截图1路径/描述] — 时间点 XX:XX，[内容]
- [截图2路径/描述] — 时间点 XX:XX，[内容]
- ...

## 动画/可视化需求描述 ⚙️
### 步骤1
- 演示流程：
- 关键变化：

## 专业练习资源 ⚙️
1. [资源名称](链接) - 难度：入门/中等/进阶
   - **考点**：本题考的是xxx
   - **提示**：[一句话提示]
2. ...
```

## Usage Examples

### Example 1: Computer Science
User: "帮我处理这个动态规划教程视频，生成学习文档"
Agent:
1. Load this skill
2. 识别专业方向：计算机科学 → 算法
3. 联网搜索动态规划知识体系
4. Process video using the workflow
5. 代码板块 + 洛谷题目推荐
6. Deliver final document

### Example 2: Mathematics
User: "帮我处理这个线性代数特征值视频"
Agent:
1. Load this skill
2. 识别专业方向：数学 → 线性代数
3. 联网搜索特征值相关定理、证明思路、典型习题
4. 公式推导板块 + 几何直觉解释
5. Deliver final document

### Example 3: Medicine
User: "帮我处理这个心电图诊断课程视频"
Agent:
1. Load this skill
2. 识别专业方向：医学 → 心电图
3. 联网搜索心电图诊断指南、典型病例
4. 诊断流程图 + 截图标注 + 临床案例
5. Deliver final document

### Example 4: Law
User: "帮我处理这个民法总则讲解视频"
Agent:
1. Load this skill
2. 识别专业方向：法学 → 民法
3. 联网搜索相关法条原文、经典判例
4. 法条解读 + 案例分析 + 构成要件拆解
5. Deliver final document

### Example 5: Design
User: "帮我处理这个 Figma UI 设计教程视频"
Agent:
1. Load this skill
2. 识别专业方向：设计 → UI设计
3. 联网搜索设计规范、配色方案
4. 操作步骤截图 + 工具使用技巧
5. Deliver final document

## Performance Considerations

- **Processing Time**: 2-hour video ≈ 40-80 minutes total
  - Audio extraction: 2-3 minutes
  - Speech recognition: 20-40 minutes
  - Code OCR: 10-20 minutes (if enabled)
  - AI analysis: 10-15 minutes
  - Problem search: 1-2 minutes

- **Disk Space**:
  - Temporary files: 3-5 GB per 2-hour video
  - Final document: 50-100 pages Markdown

## Error Handling

- **Video too large**: Split into segments for processing
- **Poor audio quality**: Fall back to manual transcript if available
- **OCR fails**: Focus on audio content only
- **Network issues**: Cache search results for offline use

## Customization Options

Users can customize:
1. Output format (Markdown/Word/PDF)
2. Level of detail (brief/comprehensive)
3. 专业方向覆盖深度（基础/进阶/全部）
4. 截图频率（少/中/多）
5. 练习资源来源偏好（指定网站/平台）