#!/usr/bin/env python3
"""
Run the complete Scrantenna news pipeline:
1. Fetch fresh news articles
2. Generate distilled content
3. Create shorts data with knowledge graphs
"""

import requests
import json
import os
import re
from datetime import datetime
from typing import List, Dict
from pathlib import Path

# Try to import OpenAI for LLM-based distillation
try:
    import openai
    llm_available = True
    client = openai.OpenAI()
except ImportError:
    print("OpenAI not available. Using fallback distillation.")
    llm_available = False
    client = None

def create_distilled_version_llm(text: str) -> str:
    """Create distilled version using LLM."""
    if not llm_available or not text:
        return ""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Extract the core facts from news text into direct, precise statements. Use simple subject-verb-object format. Avoid referring to 'the article' or 'the story'. State facts directly as if reporting them yourself. Keep it under 100 characters."
                },
                {
                    "role": "user", 
                    "content": f"Distill this news text: {text}"
                }
            ],
            max_tokens=50,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM distillation failed: {e}")
        return create_distilled_version_fallback(text)

def create_distilled_version_fallback(text: str) -> str:
    """Fallback distillation using simple text processing."""
    if not text:
        return ""
    
    # Extract first sentence
    sentences = text.split('.')
    first_sentence = sentences[0].strip() if sentences else text
    
    # Remove common article references
    first_sentence = re.sub(r'\(.*?\)', '', first_sentence)  # Remove parentheses
    first_sentence = re.sub(r'^(The|A|An)\s+', '', first_sentence)  # Remove articles
    
    # Don't truncate - keep it natural
    if not first_sentence.endswith('.'):
        first_sentence += "."
    
    return first_sentence

def create_distilled_version(text: str) -> str:
    """Create distilled version using best available method."""
    if llm_available:
        return create_distilled_version_llm(text)
    else:
        return create_distilled_version_fallback(text)

def process_article(article: Dict) -> Dict:
    """Process article to include distilled versions alongside original text."""
    processed = article.copy()
    
    # Use description as main content since API content is truncated
    main_content = article.get('description', '') or article.get('title', '')
    
    # Add distilled versions
    if article.get('title'):
        processed['title_distilled'] = create_distilled_version(article['title'])
    
    if article.get('description'):
        processed['description_distilled'] = create_distilled_version(article['description'])
    
    # Since content is truncated, use description as main content
    processed['content_distilled'] = create_distilled_version(main_content)
    
    return processed

def fetch_news_with_demo_fallback():
    """Fetch news articles with demo data fallback if API fails."""
    
    # Try with demo NewsAPI key (you should replace this with your own)
    api_key = 'be93936988fd4df185bd56e8a11125a0'  # Demo key from notebook
    query = "Scranton"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    
    try:
        print("🔄 Fetching fresh news articles...")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                print(f"✅ Successfully fetched {len(articles)} articles")
                return data
            else:
                print("⚠️  No articles returned from API")
        else:
            print(f"❌ API request failed: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ Failed to fetch news: {e}")
    
    # Fallback to demo data
    print("📝 Using demo data fallback...")
    return create_demo_news_data()

def create_demo_news_data():
    """Create demo news data for testing."""
    demo_articles = [
        {
            "title": "Scranton Mayor Announces New Infrastructure Investment",
            "description": "Mayor Paige Cognetti announced a $5 million investment in road improvements across the city, focusing on downtown areas and major thoroughfares.",
            "content": "The City of Scranton will receive significant funding for infrastructure improvements...",
            "source": {"name": "Times Tribune"},
            "publishedAt": datetime.now().isoformat(),
            "url": "https://example.com/infrastructure",
            "urlToImage": "https://example.com/infrastructure.jpg"
        },
        {
            "title": "Local Business District Sees Growth in Q2",
            "description": "Downtown Scranton businesses report increased foot traffic and sales following recent development initiatives.",
            "content": "Local business owners are optimistic about continued growth...",
            "source": {"name": "Scranton Business Journal"},
            "publishedAt": datetime.now().isoformat(),
            "url": "https://example.com/business",
            "urlToImage": "https://example.com/business.jpg"
        },
        {
            "title": "University of Scranton Hosts Technology Summit",
            "description": "The annual technology summit brings together local entrepreneurs and students to discuss innovation in northeastern Pennsylvania.",
            "content": "The University of Scranton hosted its annual technology summit...",
            "source": {"name": "University News"},
            "publishedAt": datetime.now().isoformat(),
            "url": "https://example.com/tech-summit",
            "urlToImage": "https://example.com/tech-summit.jpg"
        }
    ]
    
    return {
        "status": "ok",
        "totalResults": len(demo_articles),
        "articles": demo_articles
    }

def save_news(news_data):
    """Save news articles with both original and distilled formats."""
    data_dir = Path("../data/daily")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Process articles to add distilled versions
    processed_articles = []
    for article in news_data.get('articles', []):
        processed_articles.append(process_article(article))
    
    # Create data structure with metadata
    output_data = {
        "query": "Scranton",
        "fetched_at": datetime.now().isoformat(),
        "total_articles": len(processed_articles),
        "has_distilled": True,
        "distillation_method": "llm" if llm_available else "fallback",
        "articles": processed_articles
    }
    
    # Save with date-based filename
    file_path = data_dir / f"scranton_news_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(file_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"📄 Saved {len(processed_articles)} articles to {file_path}")
    if llm_available:
        print("✅ LLM-based distilled versions included")
    else:
        print("✅ Fallback distilled versions included")
    
    return file_path

def run_complete_pipeline():
    """Run the complete news regeneration pipeline."""
    print("🎬 Starting Scrantenna News Pipeline...")
    print("=" * 60)
    
    # Step 1: Fetch fresh news
    news_data = fetch_news_with_demo_fallback()
    
    # Step 2: Save with distilled content
    news_file = save_news(news_data)
    
    # Step 3: Generate shorts data
    print("🔄 Generating shorts data with knowledge graphs...")
    
    # Import and run the shorts generator
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, 'generate_shorts.py', '--force'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Shorts data generated successfully")
            print(result.stdout)
        else:
            print("❌ Shorts generation failed:")
            print(result.stderr)
    
    except Exception as e:
        print(f"❌ Failed to run shorts generator: {e}")
    
    print("=" * 60)
    print("🎉 Pipeline complete! You can now view the shorts at:")
    print("   python3 -m http.server 8000")
    print("   Then open: http://localhost:8000")

if __name__ == "__main__":
    run_complete_pipeline()