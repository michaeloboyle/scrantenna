#!/usr/bin/env python3
"""
Daily news generation script for Scrantenna
Orchestrates fetching news and generating static pages
"""
import os
import sys
from datetime import datetime
from news_fetcher import NewsFetcher
from static_generator import StaticNewsGenerator

def main():
    """
    Main script to generate daily news page
    """
    print(f"Starting daily news generation for {datetime.now().strftime('%Y-%m-%d')}")
    
    # Get API key from environment
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("ERROR: NEWSAPI_KEY environment variable not set")
        sys.exit(1)
    
    try:
        # Step 1: Fetch news
        print("Fetching news from NewsAPI...")
        fetcher = NewsFetcher(api_key)
        news_file = fetcher.save_daily_news()
        
        # Step 2: Generate static HTML
        print("Generating static HTML page...")
        import json
        with open(news_file, 'r') as f:
            news_data = json.load(f)
        
        generator = StaticNewsGenerator()
        html_file = generator.generate_daily_page(news_data)
        
        print(f"✅ Daily news generation complete!")
        print(f"   News data: {news_file}")
        print(f"   HTML page: {html_file}")
        print(f"   Articles found: {news_data['total_results']}")
        
    except Exception as e:
        print(f"❌ Error generating daily news: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()