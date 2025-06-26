#!/usr/bin/env python3
"""
Generate optimized shorts data from news articles.
Creates condensed, visual-friendly versions for the shorts player.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

def clean_text(text: str) -> str:
    """Clean text for shorts display."""
    if not text:
        return ""
    
    # Remove character count indicators
    text = re.sub(r'\[\+\d+ chars\]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Limit length for shorts
    if len(text) > 200:
        text = text[:197] + "..."
    
    return text

def create_short_from_article(article: Dict, index: int) -> Dict:
    """Convert a news article into a short format."""
    
    # Extract key information
    title = clean_text(article.get('title', ''))
    title_svo = clean_text(article.get('title_svo', ''))
    description = clean_text(article.get('description', ''))
    description_svo = clean_text(article.get('description_svo', ''))
    
    # Create engaging title if original is too long
    if len(title) > 80:
        title = title[:77] + "..."
    
    # Ensure we have SVO fallbacks
    if not title_svo and title:
        title_svo = f"Article reports {title.lower()}"
    if not description_svo and description:
        description_svo = f"Story mentions key details."
    
    short = {
        "id": f"short_{index}",
        "title": title,
        "title_svo": title_svo,
        "description": description,
        "description_svo": description_svo,
        "source": article.get('source', {}).get('name', 'Unknown'),
        "publishedAt": article.get('publishedAt', ''),
        "url": article.get('url', ''),
        "urlToImage": article.get('urlToImage', ''),
        "duration": 8000,  # 8 seconds per short
        "background_gradient": get_background_gradient(index),
        "animation_delay": min(index * 0.1, 1.0)  # Stagger animations
    }
    
    return short

def get_background_gradient(index: int) -> str:
    """Get a background gradient based on index."""
    gradients = [
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
        "linear-gradient(135deg, #ff8a80 0%, #ea80fc 100%)",
        "linear-gradient(135deg, #82b1ff 0%, #b388ff 100%)",
        "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)"
    ]
    return gradients[index % len(gradients)]

def generate_shorts_from_news(news_file: Path, max_shorts: int = 15) -> Dict:
    """Generate shorts data from news file."""
    
    print(f"Loading news from: {news_file}")
    
    with open(news_file, 'r') as f:
        news_data = json.load(f)
    
    articles = news_data.get('articles', [])
    print(f"Found {len(articles)} articles")
    
    # Filter and sort articles for best shorts
    # Prioritize articles with both title and description
    good_articles = []
    for article in articles[:max_shorts]:
        if (article.get('title') and 
            article.get('description') and 
            len(article.get('title', '')) > 10):
            good_articles.append(article)
    
    print(f"Selected {len(good_articles)} articles for shorts")
    
    # Generate shorts
    shorts = []
    for i, article in enumerate(good_articles):
        short = create_short_from_article(article, i)
        shorts.append(short)
    
    # Create shorts data structure
    shorts_data = {
        "generated_at": datetime.now().isoformat(),
        "source_file": str(news_file),
        "total_shorts": len(shorts),
        "total_duration": len(shorts) * 8,  # seconds
        "has_svo": news_data.get('has_svo', False),
        "shorts": shorts
    }
    
    return shorts_data

def main():
    """Main function to generate shorts."""
    
    # Find the latest news file
    data_dir = Path("../data/daily")
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    news_files = sorted(data_dir.glob("scranton_news_*.json"), reverse=True)
    if not news_files:
        print("No news files found")
        return
    
    latest_file = news_files[0]
    
    # Generate shorts data
    shorts_data = generate_shorts_from_news(latest_file)
    
    # Save shorts data
    output_file = Path("shorts_data.json")
    with open(output_file, 'w') as f:
        json.dump(shorts_data, f, indent=2)
    
    print(f"Generated {shorts_data['total_shorts']} shorts")
    print(f"Total duration: {shorts_data['total_duration']} seconds")
    print(f"Saved to: {output_file}")
    
    # Generate a simple player launcher
    create_player_launcher()

def create_player_launcher():
    """Create a simple launcher script."""
    launcher_content = '''#!/bin/bash
# Scrantenna Shorts Player Launcher

echo "🎬 Starting Scrantenna Shorts..."
echo "📱 Full-screen news stories with SVO toggle"
echo ""

# Check if we have a local server running
if command -v python3 &> /dev/null; then
    echo "🚀 Starting local server on port 8000..."
    echo "📱 Open: http://localhost:8000"
    echo "⌨️  Controls: ↑↓ arrows, spacebar, 't' to toggle format"
    echo ""
    python3 -m http.server 8000
else
    echo "❌ Python3 not found. Please install Python to run the server."
    echo "💡 Or open index.html directly in your browser"
fi
'''
    
    with open("launch_shorts.sh", 'w') as f:
        f.write(launcher_content)
    
    # Make executable
    os.chmod("launch_shorts.sh", 0o755)
    print("Created launcher: ./launch_shorts.sh")

if __name__ == "__main__":
    main()