#!/bin/bash
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
