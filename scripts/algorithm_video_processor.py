#!/usr/bin/env python3
"""
算法视频文档生成器 - 主处理脚本
Algorithm Video Documentation Generator - Main Processor
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AlgorithmVideoProcessor:
    """算法视频处理器"""
    
    def __init__(self, video_path: str, output_dir: str = None):
        """
        初始化处理器
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录（可选）
        """
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        self.output_dir = Path(output_dir) if output_dir else self.video_path.parent
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 临时目录
        self.temp_dir = tempfile.mkdtemp(prefix="algo_video_")
        self.temp_dir = Path(self.temp_dir)
        
        # 检查依赖
        self._check_dependencies()
        
        # 视频信息
        self.video_info = {}
        self.audio_path = None
        self.transcript = []
        self.code_blocks = []
        self.document = ""
        
    def _check_dependencies(self):
        """检查依赖是否安装"""
        dependencies = {
            'ffmpeg': ['ffmpeg', '-version'],
            'whisper': ['python', '-c', 'import whisper'],
            'opencv': ['python', '-c', 'import cv2'],
            'pytesseract': ['python', '-c', 'import pytesseract']
        }
        
        missing = []
        for name, cmd in dependencies.items():
            try:
                subprocess.run(cmd, capture_output=True, check=True)
                logger.info(f"✓ {name} 已安装")
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(name)
                logger.warning(f"✗ {name} 未安装")
        
        if missing:
            logger.warning(f"缺少依赖: {', '.join(missing)}")
            logger.warning("某些功能可能无法使用，但核心处理仍可进行")
    
    def extract_video_info(self):
        """提取视频基础信息"""
        logger.info("正在提取视频信息...")
        
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(self.video_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            
            self.video_info = {
                'filename': self.video_path.name,
                'duration': float(info['format'].get('duration', 0)),
                'size': int(info['format'].get('size', 0)),
                'bitrate': int(info['format'].get('bit_rate', 0)),
                'format': info['format'].get('format_long_name', 'Unknown')
            }
            
            # 提取视频流信息
            for stream in info.get('streams', []):
                if stream['codec_type'] == 'video':
                    self.video_info['video_codec'] = stream.get('codec_name', 'Unknown')
                    self.video_info['resolution'] = f"{stream.get('width', 0)}x{stream.get('height', 0)}"
                    self.video_info['fps'] = stream.get('r_frame_rate', 'Unknown')
                elif stream['codec_type'] == 'audio':
                    self.video_info['audio_codec'] = stream.get('codec_name', 'Unknown')
                    self.video_info['sample_rate'] = stream.get('sample_rate', 'Unknown')
            
            # 格式化时长
            duration = self.video_info['duration']
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            self.video_info['duration_formatted'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            logger.info(f"视频信息提取完成: {self.video_info['duration_formatted']}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"提取视频信息失败: {e}")
            raise
    
    def extract_audio(self):
        """提取音频"""
        logger.info("正在提取音频...")
        
        self.audio_path = self.temp_dir / "audio.wav"
        
        cmd = [
            'ffmpeg', '-i', str(self.video_path),
            '-vn',  # 不包含视频
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # 16kHz采样率（Whisper推荐）
            '-ac', '1',  # 单声道
            '-y',  # 覆盖输出文件
            str(self.audio_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            logger.info("音频提取完成")
        except subprocess.CalledProcessError as e:
            logger.error(f"音频提取失败: {e}")
            raise
    
    def transcribe_audio(self, language: str = 'zh'):
        """
        使用Whisper转录音频
        
        Args:
            language: 语言代码（zh=中文，en=英文）
        """
        logger.info("正在转录音频...")
        
        try:
            import whisper
            
            # 加载模型（使用base模型平衡速度和准确性）
            model = whisper.load_model("base")
            
            # 转录
            result = model.transcribe(
                str(self.audio_path),
                language=language,
                verbose=False
            )
            
            # 提取带时间戳的文本
            self.transcript = []
            for segment in result['segments']:
                self.transcript.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })
            
            logger.info(f"转录完成，共 {len(self.transcript)} 个片段")
            
        except ImportError:
            logger.error("Whisper未安装，请运行: pip install openai-whisper")
            raise
        except Exception as e:
            logger.error(f"转录失败: {e}")
            raise
    
    def extract_code_frames(self, sample_interval: int = 30):
        """
        提取关键帧进行代码识别
        
        Args:
            sample_interval: 采样间隔（秒）
        """
        logger.info("正在提取关键帧...")
        
        try:
            import cv2
            import pytesseract
            from PIL import Image
            
            # 打开视频
            cap = cv2.VideoCapture(str(self.video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps
            
            self.code_blocks = []
            frame_times = []
            
            # 采样时间点
            current_time = 0
            while current_time < duration:
                frame_times.append(current_time)
                current_time += sample_interval
            
            for time_point in frame_times:
                # 定位到指定时间
                cap.set(cv2.CAP_PROP_POS_MSEC, time_point * 1000)
                ret, frame = cap.read()
                
                if ret:
                    # 保存帧图像
                    frame_path = self.temp_dir / f"frame_{int(time_point)}.png"
                    cv2.imwrite(str(frame_path), frame)
                    
                    # OCR识别
                    try:
                        img = Image.open(frame_path)
                        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                        
                        # 简单过滤：如果识别出代码特征，保留
                        if self._is_code_content(text):
                            self.code_blocks.append({
                                'time': time_point,
                                'text': text.strip(),
                                'frame_path': str(frame_path)
                            })
                    except Exception as e:
                        logger.warning(f"OCR识别失败 (time={time_point}s): {e}")
            
            cap.release()
            logger.info(f"代码帧提取完成，找到 {len(self.code_blocks)} 个代码块")
            
        except ImportError as e:
            logger.warning(f"代码识别依赖未安装: {e}")
            logger.info("跳过代码识别步骤")
        except Exception as e:
            logger.error(f"代码帧提取失败: {e}")
    
    def _is_code_content(self, text: str) -> bool:
        """简单判断文本是否为代码内容"""
        code_indicators = [
            'int ', 'void ', 'class ', 'def ', 'function ',
            '{', '}', '()', '[]', '->', '::',
            '#include', 'import ', 'from ',
            'if ', 'else ', 'for ', 'while ',
            'return ', 'break', 'continue'
        ]
        
        text_lower = text.lower()
        for indicator in code_indicators:
            if indicator.lower() in text_lower:
                return True
        return False
    
    def generate_document(self):
        """生成结构化文档"""
        logger.info("正在生成文档...")
        
        # 基础文档结构
        doc = []
        
        # 视频基础信息
        doc.append(f"# {self.video_info.get('filename', '未知课程')} - 算法学习文档\n")
        doc.append("## 视频基础信息\n")
        doc.append(f"- **课程名称**: {self.video_info.get('filename', '未知')}")
        doc.append(f"- **视频时长**: {self.video_info.get('duration_formatted', '未知')}")
        doc.append(f"- **分辨率**: {self.video_info.get('resolution', '未知')}")
        doc.append(f"- **视频编码**: {self.video_info.get('video_codec', '未知')}")
        doc.append(f"- **音频编码**: {self.video_info.get('audio_codec', '未知')}")
        doc.append(f"- **文件大小**: {self.video_info.get('size', 0) / (1024*1024):.2f} MB")
        doc.append("")
        
        # 时间节点目录
        doc.append("### 时间节点目录\n")
        if self.transcript:
            # 每5分钟一个章节
            chapter_interval = 300  # 5分钟
            current_chapter = 0
            for i, segment in enumerate(self.transcript):
                if segment['start'] >= current_chapter * chapter_interval:
                    start_time = self._format_time(segment['start'])
                    doc.append(f"- {start_time}: 知识点{current_chapter + 1}")
                    current_chapter += 1
        doc.append("")
        
        # 核心知识点梳理
        doc.append("## 核心知识点梳理\n")
        doc.append("### 算法原理\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 核心概念\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 适用场景\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 解题底层思想\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 算法优缺点\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 时间/空间复杂度分析\n")
        doc.append("[待AI分析填充]\n")
        
        # 逐时间节点详细笔记
        doc.append("## 逐时间节点详细笔记\n")
        if self.transcript:
            # 按5分钟分组
            chapter_interval = 300
            current_chapter = 0
            chapter_segments = []
            
            for segment in self.transcript:
                if segment['start'] >= current_chapter * chapter_interval:
                    if chapter_segments:
                        doc.append(f"### 【时间节点：{self._format_time(current_chapter * chapter_interval)} - {self._format_time((current_chapter + 1) * chapter_interval)}】\n")
                        for seg in chapter_segments:
                            doc.append(f"- **[{self._format_time(seg['start'])}]** {seg['text']}")
                        doc.append("")
                    current_chapter += 1
                    chapter_segments = []
                chapter_segments.append(segment)
            
            # 最后一个章节
            if chapter_segments:
                doc.append(f"### 【时间节点：{self._format_time(current_chapter * chapter_interval)} - {self._format_time(self.video_info.get('duration', 0))}】\n")
                for seg in chapter_segments:
                    doc.append(f"- **[{self._format_time(seg['start'])}]** {seg['text']}")
                doc.append("")
        
        # 完整代码板块
        doc.append("## 完整代码板块\n")
        if self.code_blocks:
            for i, block in enumerate(self.code_blocks):
                doc.append(f"### 代码实现{i + 1} (时间点: {self._format_time(block['time'])})\n")
                doc.append("```")
                doc.append(block['text'])
                doc.append("```\n")
                doc.append("**逐行注释:** [待AI分析填充]\n")
                doc.append("**设计逻辑:** [待AI分析填充]\n")
        else:
            doc.append("[未检测到代码片段]\n")
        
        # 算法解题思路深度解析
        doc.append("## 算法解题思路深度解析\n")
        doc.append("### 通用思考流程\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 正向推导逻辑\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 反向复盘逻辑\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 同类题型通用模板\n")
        doc.append("[待AI分析填充]\n")
        
        # 常见错误 & 避坑指南
        doc.append("## 常见错误 & 避坑指南\n")
        doc.append("### 易错点1\n")
        doc.append("- **错误原因:** [待AI分析填充]")
        doc.append("- **修正方案:** [待AI分析填充]")
        doc.append("- **调试方法:** [待AI分析填充]\n")
        
        # 注意事项 & 考点总结
        doc.append("## 注意事项 & 考点总结\n")
        doc.append("### 边界条件\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 特殊案例\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 高频考点\n")
        doc.append("[待AI分析填充]\n")
        doc.append("### 易混淆知识点\n")
        doc.append("[待AI分析填充]\n")
        
        # 关键截图标注区
        doc.append("## 关键截图标注区\n")
        doc.append("- [ ] 截图1：时间点 00:00:00，内容描述")
        doc.append("- [ ] 截图2：时间点 XX:XX:XX，内容描述\n")
        
        # 代码实现动画需求描述
        doc.append("## 代码实现动画需求描述\n")
        doc.append("### 动画步骤1\n")
        doc.append("- **演示流程:** [待AI分析填充]")
        doc.append("- **变量变化:** [待AI分析填充]")
        doc.append("- **数据结构变化:** [待AI分析填充]\n")
        
        # 洛谷相关题目推荐
        doc.append("## 洛谷相关题目推荐\n")
        doc.append("[待AI搜索填充]\n")
        
        # 完整逐字稿
        doc.append("## 完整逐字稿\n")
        if self.transcript:
            doc.append("```")
            for segment in self.transcript:
                doc.append(f"[{self._format_time(segment['start'])}] {segment['text']}")
            doc.append("```\n")
        
        self.document = "\n".join(doc)
        logger.info("文档生成完成")
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间为 HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def save_document(self, output_path: str = None):
        """保存文档到文件"""
        if output_path is None:
            output_path = self.output_dir / f"{self.video_path.stem}_document.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.document)
        
        logger.info(f"文档已保存到: {output_path}")
        return output_path
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            logger.info("临时文件已清理")
    
    def process(self, language: str = 'zh', enable_ocr: bool = True):
        """
        完整处理流程
        
        Args:
            language: 语言代码
            enable_ocr: 是否启用OCR代码识别
        """
        try:
            logger.info("开始处理视频...")
            
            # 1. 提取视频信息
            self.extract_video_info()
            
            # 2. 提取音频
            self.extract_audio()
            
            # 3. 转录音频
            self.transcribe_audio(language)
            
            # 4. 提取代码帧（可选）
            if enable_ocr:
                self.extract_code_frames()
            
            # 5. 生成文档
            self.generate_document()
            
            # 6. 保存文档
            output_path = self.save_document()
            
            logger.info("处理完成！")
            return output_path
            
        except Exception as e:
            logger.error(f"处理失败: {e}")
            raise
        finally:
            self.cleanup()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='算法视频文档生成器')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-l', '--language', default='zh', help='语言代码 (zh=中文, en=英文)')
    parser.add_argument('--no-ocr', action='store_true', help='禁用OCR代码识别')
    
    args = parser.parse_args()
    
    try:
        processor = AlgorithmVideoProcessor(args.video_path, args.output)
        output_path = processor.process(
            language=args.language,
            enable_ocr=not args.no_ocr
        )
        print(f"文档生成完成: {output_path}")
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()