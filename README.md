# Universal Video Learning Document Generator

A powerful AI skill that converts **any subject's** video courses/tutorials into comprehensive, structured learning documents. Works for Computer Science, Mathematics, Physics, Economics, Medicine, Law, Design, Engineering, Humanities — any field where video learning is used.

## Features

- **Multi-Subject Support** - Automatically adapts to CS, Math, Physics, Medicine, Law, Design, and more
- **Speech Recognition** - Whisper-based transcription with timestamps
- **OCR Code Recognition** - Extract code from video frames
- **AI Content Analysis** - Generate structured documentation with examples
- **Domain Resource Search** - Find relevant practice problems and references
- **Bilibili Integration** - Direct download from Bilibili (哔哩哔哩)
- **Screenshot Generation** - Auto-capture key frames based on speech keywords

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/universal-video-learning-doc.git
cd universal-video-learning-doc

# Install dependencies
pip install -r requirements.txt

# Run dependency check
python scripts/check_dependencies.py
```

### Usage

#### As a WorkBuddy Skill
```bash
# Copy to WorkBuddy skills directory
cp -r . ~/.workbuddy/skills/universal-video-doc

# Then use in WorkBuddy
# User: "帮我处理这个动态规划教程视频"
# Agent will load this skill and process the video
```

#### Standalone Usage
```bash
# Process a local video
python scripts/algorithm_video_processor.py video.mp4

# Process with custom output directory
python scripts/algorithm_video_processor.py video.mp4 -o ./output/

# Process from Bilibili
python scripts/algorithm_video_processor.py "https://www.bilibili.com/video/BV1xxxxxx?p=1"
```

## Supported Subjects

| Subject | Features |
|---------|----------|
| Computer Science | Code analysis, algorithm complexity, LeetCode problems |
| Mathematics | Formula derivation, theorem proofs, practice problems |
| Physics | Physical models, experimental principles, formula tables |
| Economics | Case analysis, data interpretation, policy background |
| Medicine | Clinical guidelines, diagnosis workflows, case studies |
| Law | Legal interpretation, case analysis, statute references |
| Design | Design workflow, tool operations, aesthetic principles |
| Engineering | Calculations, standards, construction procedures |
| Language Learning | Grammar, vocabulary, listening techniques |
| Humanities | Conceptual analysis, theoretical frameworks |

## Output Structure

The generated document includes:

1. **Video Metadata** - Course name, duration, lecturer, BV number
2. **Knowledge Graph** - What's covered vs. what's missing
3. **Timeline Index** - Chapter navigation by timestamp
4. **Core Concepts** - Detailed explanations with examples
5. **Step-by-Step Notes** - Timestamped detailed notes
6. **Code Implementation** - Complete code with line-by-line comments
7. **Problem-Solving Analysis** - General thinking process
8. **Common Mistakes** - Error patterns and how to avoid them
9. **Exam Points** - High-frequency topics and key takeaways
10. **Key Screenshots** - Auto-captured important frames
11. **Practice Resources** - Related problems from LeetCode/Luogu/etc.

## Example Output

```markdown
# Dynamic Programming Tutorial - Chapter 3: 01 Knapsack

## Video Info
- Course: ACM Programming Contest Training
- Duration: 45:23
- Lecturer: Professor Wang

## Core Concepts

### 01 Knapsack Problem
**Definition**: Given n items, each with weight w[i] and value v[i], 
find the maximum value that fits in a knapsack of capacity W.

**Life Analogy**: Like packing for a trip with limited luggage space — 
you need to choose which items give you the most value.

**Example**:
> Items: [(w:2,v:3), (w:3,v:4), (w:4,v:5)]
> Capacity: W = 5
> Optimal: Take items 1 and 2 → Total value = 7

### State Transition Equation
dp[i][w] = max(dp[i-1][w], dp[i-1][w-w[i]] + v[i])

**Line-by-line explanation**:
- `dp[i][w]`: Maximum value using first i items with capacity w
- `dp[i-1][w]`: Don't take item i (carry over previous result)
- `dp[i-1][w-w[i]] + v[i]`: Take item i (add its value)
```

## Dependencies

### System Tools
- **FFmpeg** - Video/audio processing
- **Tesseract OCR** - Code recognition (optional)
- **yt-dlp** - Bilibili video download

### Python Packages
```txt
openai-whisper>=20231117
opencv-python>=4.8.0
pytesseract>=0.3.10
moviepy>=1.0.3
Pillow>=10.0.0
yt-dlp>=2024.1.1
```

## Performance

| Metric | Value |
|--------|-------|
| Processing Time | 2-hour video ≈ 40-80 minutes |
| Output Size | 50-100 pages Markdown |
| Temp Files | 3-5 GB (auto-cleaned) |
| Min RAM | 8 GB (16 GB recommended) |

## Troubleshooting

### FFmpeg not found
```bash
# Windows: Add to PATH
set PATH=%PATH%;C:\ffmpeg\bin

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Whisper model download slow
```bash
# Use Chinese mirror
export HF_ENDPOINT=https://hf-mirror.com
```

### OCR inaccurate
- Ensure video resolution is at least 720p
- Use `--no-ocr` to skip code recognition
- Manually correct recognition results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for [WorkBuddy](https://codebuddy.cn) AI assistant platform
- Uses OpenAI Whisper for speech recognition
- Uses FFmpeg for video processing
- Inspired by the need for better video-to-document conversion
