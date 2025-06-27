#!/usr/bin/env python3
"""
Quick verification script to check if the fixes are working.
"""

import json
import sys

def check_truncation_issues():
    """Check for truncation in distilled content."""
    print("🔍 Checking for truncation issues...")
    
    try:
        with open('shorts_data.json', 'r') as f:
            data = json.load(f)
        
        issues_found = []
        
        for i, short in enumerate(data['shorts']):
            # Check title_distilled
            title_distilled = short.get('title_distilled', '')
            if title_distilled and title_distilled.endswith('...'):
                issues_found.append(f"Short {i}: title_distilled truncated: '{title_distilled}'")
            
            # Check description_distilled
            desc_distilled = short.get('description_distilled', '')
            if desc_distilled and desc_distilled.endswith('...'):
                issues_found.append(f"Short {i}: description_distilled truncated: '{desc_distilled}'")
            
            # Check content_distilled
            content_distilled = short.get('content_distilled', '')
            if content_distilled and content_distilled.endswith('...'):
                issues_found.append(f"Short {i}: content_distilled truncated: '{content_distilled}'")
        
        if issues_found:
            print("❌ Truncation issues found:")
            for issue in issues_found:
                print(f"   {issue}")
            return False
        else:
            print("✅ No truncation issues found")
            return True
            
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return False

def check_graph_data():
    """Check if knowledge graphs are present."""
    print("🔍 Checking knowledge graph data...")
    
    try:
        with open('shorts_data.json', 'r') as f:
            data = json.load(f)
        
        graph_stats = {
            'has_graph': 0,
            'has_entities': 0,
            'has_svg': 0,
            'total_entities': 0
        }
        
        for short in data['shorts']:
            graph = short.get('graph', {})
            
            if graph:
                graph_stats['has_graph'] += 1
                
                entities = graph.get('entities', [])
                if entities:
                    graph_stats['has_entities'] += 1
                    graph_stats['total_entities'] += len(entities)
                
                svg = graph.get('svg', '')
                if svg and len(svg) > 50:  # Basic SVG content check
                    graph_stats['has_svg'] += 1
        
        total_shorts = len(data['shorts'])
        
        print(f"📊 Graph data statistics:")
        print(f"   Total shorts: {total_shorts}")
        print(f"   Shorts with graph data: {graph_stats['has_graph']}")
        print(f"   Shorts with entities: {graph_stats['has_entities']}")
        print(f"   Shorts with SVG: {graph_stats['has_svg']}")
        print(f"   Total entities found: {graph_stats['total_entities']}")
        
        if graph_stats['has_svg'] == total_shorts:
            print("✅ All shorts have SVG graph data")
            return True
        else:
            print(f"⚠️  Only {graph_stats['has_svg']}/{total_shorts} shorts have SVG data")
            return False
            
    except Exception as e:
        print(f"❌ Failed to analyze graph data: {e}")
        return False

def show_sample_data():
    """Show a sample of the processed data."""
    print("📄 Sample data preview:")
    
    try:
        with open('shorts_data.json', 'r') as f:
            data = json.load(f)
        
        sample = data['shorts'][0]
        
        print(f"   Title: {sample.get('title', 'N/A')[:80]}...")
        print(f"   Title Distilled: {sample.get('title_distilled', 'N/A')}")
        print(f"   Content Distilled: {sample.get('content_distilled', 'N/A')[:100]}...")
        
        graph = sample.get('graph', {})
        entities = graph.get('entities', [])
        print(f"   Entities: {[e.get('name') for e in entities[:3]]}...")
        print(f"   SVG length: {len(graph.get('svg', ''))} characters")
        
    except Exception as e:
        print(f"❌ Failed to show sample: {e}")

def main():
    """Run all verification checks."""
    print("🧪 Scrantenna Fixes Verification")
    print("=" * 50)
    
    truncation_ok = check_truncation_issues()
    print()
    
    graph_ok = check_graph_data()
    print()
    
    show_sample_data()
    print()
    
    print("=" * 50)
    if truncation_ok and graph_ok:
        print("🎉 All fixes verified successfully!")
        print("✅ Distilled text is not truncated")
        print("✅ Knowledge graphs are visible")
        print("\n🚀 You can view the shorts at: http://localhost:8001")
    else:
        print("⚠️  Some issues detected - see details above")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())