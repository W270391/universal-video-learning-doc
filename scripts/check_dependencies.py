#!/usr/bin/env python3
"""
依赖检查与安装脚本
Dependency Check and Installation Script
"""

import subprocess
import sys
import platform
import os
from pathlib import Path
import shutil


def check_command(command: str) -> bool:
    """检查命令是否可用"""
    try:
        subprocess.run(
            command if isinstance(command, list) else [command],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_ffmpeg() -> bool:
    """检查FFmpeg是否安装"""
    print("检查 FFmpeg...", end=" ")
    if check_command(['ffmpeg', '-version']):
        print("✓ 已安装")
        return True
    else:
        print("✗ 未安装")
        return False


def check_tesseract() -> bool:
    """检查Tesseract OCR是否安装"""
    print("检查 Tesseract OCR...", end=" ")
    
    # Windows特殊处理
    if platform.system() == 'Windows':
        # 检查常见安装路径
        common_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
        for path in common_paths:
            if Path(path).exists():
                print(f"✓ 已安装 ({path})")
                return True
        print("✗ 未安装")
        return False
    else:
        if check_command(['tesseract', '--version']):
            print("✓ 已安装")
            return True
        else:
            print("✗ 未安装")
            return False


def check_python_package(package: str) -> bool:
    """检查Python包是否安装"""
    print(f"检查 {package}...", end=" ")
    try:
        __import__(package)
        print("✓ 已安装")
        return True
    except ImportError:
        print("✗ 未安装")
        return False


def install_ffmpeg_windows():
    """Windows下安装FFmpeg"""
    print("\n=== 安装 FFmpeg (Windows) ===")
    print("请按以下步骤手动安装:")
    print("1. 访问 https://ffmpeg.org/download.html")
    print("2. 下载 Windows 版本")
    print("3. 解压到 C:\\ffmpeg")
    print("4. 将 C:\\ffmpeg\\bin 添加到系统 PATH 环境变量")
    print("\n或者使用 Chocolatey 包管理器:")
    print("  choco install ffmpeg")
    print("\n或者使用 winget:")
    print("  winget install FFmpeg")


def install_tesseract_windows():
    """Windows下安装Tesseract"""
    print("\n=== 安装 Tesseract OCR (Windows) ===")
    print("请按以下步骤手动安装:")
    print("1. 访问 https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. 下载最新的 Windows 安装包")
    print("3. 运行安装程序")
    print("4. 安装时勾选需要的语言包（如 Chinese Simplified）")
    print("5. 将安装目录添加到系统 PATH 环境变量")
    print("   通常路径为: C:\\Program Files\\Tesseract-OCR")


def install_python_packages():
    """安装Python依赖"""
    print("\n=== 安装 Python 依赖 ===")
    
    packages = [
        'openai-whisper',
        'opencv-python',
        'pytesseract',
        'moviepy',
        'Pillow'
    ]
    
    # 检查哪些需要安装
    to_install = []
    for pkg in packages:
        # 转换包名（pip包名和import名可能不同）
        import_name = pkg.replace('-', '_')
        if import_name == 'opencv_python':
            import_name = 'cv2'
        elif import_name == 'openai_whisper':
            import_name = 'whisper'
        
        try:
            __import__(import_name)
            print(f"✓ {pkg} 已安装")
        except ImportError:
            to_install.append(pkg)
            print(f"✗ {pkg} 需要安装")
    
    if to_install:
        print(f"\n正在安装: {', '.join(to_install)}")
        for pkg in to_install:
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', pkg],
                    check=True,
                    capture_output=True
                )
                print(f"✓ {pkg} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"✗ {pkg} 安装失败: {e}")
                return False
    
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("算法视频文档生成器 - 依赖检查")
    print("=" * 50)
    
    # 检查所有依赖
    dependencies = {
        'ffmpeg': check_ffmpeg(),
        'tesseract': check_tesseract(),
        'whisper': check_python_package('whisper'),
        'cv2': check_python_package('cv2'),
        'pytesseract': check_python_package('pytesseract'),
        'moviepy': check_python_package('moviepy')
    }
    
    # 显示结果
    print("\n" + "=" * 50)
    print("依赖检查结果:")
    print("=" * 50)
    
    all_installed = all(dependencies.values())
    
    if all_installed:
        print("\n✓ 所有依赖已安装，可以开始使用！")
        return 0
    
    # 提供安装指导
    print("\n以下依赖需要安装:")
    
    if not dependencies['ffmpeg']:
        install_ffmpeg_windows() if platform.system() == 'Windows' else print("请使用包管理器安装 ffmpeg")
    
    if not dependencies['tesseract']:
        install_tesseract_windows() if platform.system() == 'Windows' else print("请使用包管理器安装 tesseract-ocr")
    
    # 安装Python包
    if not all([dependencies['whisper'], dependencies['cv2'], dependencies['pytesseract'], dependencies['moviepy']]):
        install_python_packages()
    
    print("\n" + "=" * 50)
    print("安装完成后，请重新运行依赖检查")
    print("=" * 50)
    
    return 1


if __name__ == '__main__':
    sys.exit(main())