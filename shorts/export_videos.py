#!/usr/bin/env python3
"""
Export news shorts as videos for social media platforms.
Uses headless browser automation to record HTML animations as video.
"""

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Tuple

# Platform specifications for video export
PLATFORM_SPECS = {
    "tiktok": {
        "resolution": (1080, 1920),  # 9:16 aspect ratio
        "fps": 60,
        "duration": 10,
        "format": "mp4",
        "quality": "high"
    },
    "youtube": {
        "resolution": (1080, 1920),  # YouTube Shorts 9:16
        "fps": 30,
        "duration": 10,
        "format": "mp4", 
        "quality": "high"
    },
    "instagram": {
        "resolution": (1080, 1920),  # Instagram Reels 9:16
        "fps": 30,
        "duration": 10,
        "format": "mp4",
        "quality": "medium"
    },
    "twitter": {
        "resolution": (1080, 1920),  # Twitter video 9:16
        "fps": 30,
        "duration": 10,
        "format": "mp4",
        "quality": "medium"
    }
}

def check_dependencies():
    """Check if required tools are installed."""
    required_tools = ["playwright", "ffmpeg"]
    missing = []
    
    try:
        import playwright
    except ImportError:
        missing.append("playwright (pip install playwright)")
    
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("ffmpeg (brew install ffmpeg)")
    
    if missing:
        print("Missing dependencies:")
        for tool in missing:
            print(f"  - {tool}")
        print("\\nInstall missing dependencies and try again.")
        return False
    
    return True

def setup_video_page(width: int, height: int) -> str:
    """Create HTML page optimized for video recording."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width={width}, height={height}">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                width: {width}px; 
                height: {height}px; 
                overflow: hidden;
                font-family: 'Arial Black', sans-serif;
            }}
            .video-container {{
                width: 100%;
                height: 100%;
                position: relative;
            }}
        </style>
        <script src="../index.html"></script>
    </head>
    <body>
        <div class="video-container">
            <!-- Shorts content will be injected here -->
        </div>
    </body>
    </html>
    """

async def record_short_video(short_data: Dict, platform: str, output_dir: Path):
    """Record a single short as video using Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright")
        return None
    
    spec = PLATFORM_SPECS[platform]
    width, height = spec["resolution"]
    duration = spec["duration"]
    fps = spec["fps"]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})
        
        # Load the shorts viewer with specific short
        await page.goto("http://localhost:8000")
        
        # Wait for content to load and navigate to specific short
        await page.wait_for_load_state("networkidle")
        
        # Start recording
        video_path = output_dir / f"{short_data['id']}_{platform}.mp4"
        await page.video.start_recording(path=str(video_path))
        
        # Let the short play through its duration
        await page.wait_for_timeout(duration * 1000)
        
        # Stop recording
        await page.video.stop_recording()
        await browser.close()
        
        return video_path

def add_watermark_and_optimize(input_path: Path, platform: str, output_path: Path):
    """Add watermark and optimize video for platform."""
    spec = PLATFORM_SPECS[platform]
    
    # FFmpeg command to add watermark and optimize
    watermark_text = "Scrantenna News"
    
    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-vf", f"drawtext=text='{watermark_text}':fontcolor=white:fontsize=24:x=10:y=10",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23" if spec["quality"] == "high" else "28",
        "-r", str(spec["fps"]),
        "-y",  # Overwrite output file
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")
        return False

def generate_social_metadata(short_data: Dict, platform: str) -> Dict:
    """Generate platform-specific metadata for posting."""
    base_hashtags = ["#ScrantonNews", "#LocalNews", "#Pennsylvania"]
    
    metadata = {
        "title": short_data.get("title", "Scranton News Update"),
        "description": short_data.get("content", ""),
        "hashtags": base_hashtags,
        "url": short_data.get("url", ""),
        "source": short_data.get("source", "Scrantenna")
    }
    
    # Platform-specific customizations
    if platform == "tiktok":
        metadata["hashtags"].extend(["#TikTokNews", "#FYP", "#Scranton"])
    elif platform == "youtube":
        metadata["hashtags"].extend(["#YouTubeShorts", "#News"])
    elif platform == "instagram":
        metadata["hashtags"].extend(["#Reels", "#InstagramNews"])
    
    return metadata

async def export_all_shorts(platform: str, output_dir: Path):
    """Export all shorts as videos for specified platform."""
    
    # Load shorts data
    shorts_file = Path("shorts_data.json")
    if not shorts_file.exists():
        print("No shorts data found. Run generate_shorts.py first.")
        return
    
    with open(shorts_file) as f:
        data = json.load(f)
    
    shorts = data["shorts"]
    platform_dir = output_dir / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Exporting {len(shorts)} shorts for {platform}...")
    
    for i, short in enumerate(shorts):
        print(f"Recording short {i+1}/{len(shorts)}: {short['id']}")
        
        # Record the video
        raw_video = await record_short_video(short, platform, platform_dir)
        if not raw_video:
            continue
        
        # Add watermark and optimize
        final_video = platform_dir / f"{short['id']}_final.mp4"
        if add_watermark_and_optimize(raw_video, platform, final_video):
            # Clean up raw video
            raw_video.unlink()
            
            # Generate metadata
            metadata = generate_social_metadata(short, platform)
            metadata_file = platform_dir / f"{short['id']}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✓ Exported: {final_video}")
        else:
            print(f"✗ Failed to process: {short['id']}")
    
    print(f"\\nExport complete! Videos saved to: {platform_dir}")

def main():
    parser = argparse.ArgumentParser(description="Export news shorts as videos")
    parser.add_argument("--platform", 
                       choices=["tiktok", "youtube", "instagram", "twitter"],
                       default="tiktok",
                       help="Target platform for export")
    parser.add_argument("--output", 
                       type=Path,
                       default=Path("./exports"),
                       help="Output directory for videos")
    
    args = parser.parse_args()
    
    if not check_dependencies():
        return
    
    print(f"🎬 Exporting shorts for {args.platform}")
    print("⚠️  Make sure the shorts viewer is running on http://localhost:8000")
    
    import asyncio
    asyncio.run(export_all_shorts(args.platform, args.output))

if __name__ == "__main__":
    main()