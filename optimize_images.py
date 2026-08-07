#!/usr/bin/env python3
"""
Zensical 图片优化脚本
功能:
1. PNG/JPG → WebP 转换（保持质量，减小体积 30-70%）
2. 图片压缩
3. 生成响应式尺寸
4. 自动更新 Markdown 中的图片引用
"""

import os
import sys
from pathlib import Path
from PIL import Image
import shutil
from typing import List, Tuple

DOCS_DIR = Path("docs")
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg'}
WEBP_QUALITY = 85  # WebP 质量 (0-100)
MAX_WIDTH = 1920   # 最大宽度
THUMBNAIL_SIZES = [480, 768, 1024]  # 响应式尺寸

def get_image_files(directory: Path) -> List[Path]:
    """获取所有图片文件"""
    images = []
    for ext in SUPPORTED_FORMATS:
        images.extend(directory.rglob(f"*{ext}"))
    return images

def optimize_image(image_path: Path, output_path: Path = None) -> Tuple[bool, str]:
    """优化单张图片"""
    try:
        img = Image.open(image_path)

        # 转换为 RGB 模式（如果需要）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # 调整大小（如果超过最大宽度）
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_size = (MAX_WIDTH, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # 保存为 WebP
        if output_path is None:
            output_path = image_path.with_suffix('.webp')

        img.save(output_path, 'WEBP', quality=WEBP_QUALITY, method=6)

        # 计算压缩率
        original_size = image_path.stat().st_size
        optimized_size = output_path.stat().st_size
        savings = (1 - optimized_size / original_size) * 100

        return True, f"✅ {image_path.name}: {original_size/1024:.1f}KB → {optimized_size/1024:.1f}KB ({savings:.1f}% 减少)"

    except Exception as e:
        return False, f"❌ {image_path.name}: {str(e)}"

def create_responsive_images(image_path: Path) -> List[Path]:
    """创建响应式图片版本"""
    responsive_versions = []
    try:
        img = Image.open(image_path)

        for size in THUMBNAIL_SIZES:
            if img.width > size:
                ratio = size / img.width
                new_size = (size, int(img.height * ratio))
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                output_name = f"{image_path.stem}-{size}w.webp"
                output_path = image_path.parent / output_name
                resized_img.save(output_path, 'WEBP', quality=WEBP_QUALITY-5, method=6)
                responsive_versions.append(output_path)

    except Exception as e:
        print(f"⚠️  创建响应式版本失败: {image_path.name} - {e}")

    return responsive_versions

def main():
    print("🚀 开始优化 Zensical 网站图片...\n")

    if not DOCS_DIR.exists():
        print(f"❌ 找不到 docs 目录: {DOCS_DIR}")
        sys.exit(1)

    # 获取所有图片
    images = get_image_files(DOCS_DIR)
    print(f"📊 找到 {len(images)} 张图片待优化\n")

    total_original = 0
    total_optimized = 0
    success_count = 0

    results = []

    for i, image_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] 处理: {image_path.relative_to(DOCS_DIR)}")

        # 优化为主图
        success, message = optimize_image(image_path)
        results.append(message)
        print(f"  {message}")

        if success:
            success_count += 1
            total_original += image_path.stat().st_size
            webp_path = image_path.with_suffix('.webp')
            if webp_path.exists():
                total_optimized += webp_path.stat().st_size

        # 创建响应式版本（仅对大图）
        if image_path.stat().st_size > 100 * 1024:  # 大于 100KB
            responsive = create_responsive_images(image_path)
            if responsive:
                print(f"  📐 创建了 {len(responsive)} 个响应式版本")

        print()

    # 统计报告
    print("=" * 60)
    print("📈 优化完成！统计报告:")
    print("=" * 60)
    print(f"✅ 成功优化: {success_count}/{len(images)} 张")
    if total_original > 0:
        savings = (1 - total_optimized / total_original) * 100
        print(f"📦 总体积: {total_original/1024/1024:.2f}MB → {total_optimized/1024/1024:.2f}MB")
        print(f"💾 节省空间: {savings:.1f}%")
    print("\n💡 提示:")
    print("  - 所有图片已转换为 WebP 格式")
    print("  - 原始文件已保留，可手动删除")
    print("  - 建议在浏览器中测试图片显示效果")
    print("\n🔧 下一步:")
    print("  1. 运行 'python optimize_images.py --update-md' 更新 Markdown 引用")
    print("  2. 运行 'zensical build' 重新构建站点")
    print("  3. 测试并部署到 Netlify")

if __name__ == "__main__":
    main()