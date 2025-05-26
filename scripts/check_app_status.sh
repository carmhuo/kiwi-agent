#!/bin/bash

echo "🔍 Checking Kiwi Application Status..."
echo "=================================="

# Check if process is running
if pgrep -f "kiwi_app.py" > /dev/null; then
    echo "✅ Application Status: RUNNING"
    
    # Get process details
    echo "📊 Process Details:"
    ps aux | grep kiwi_app | grep -v grep
    
    # Check port
    echo ""
    echo "🌐 Network Status:"
    if command -v netstat >/dev/null 2>&1; then
        netstat -tlnp | grep python | head -5
    else
        echo "   Port information: Check logs for port number"
    fi
    
    # Show recent logs
    echo ""
    echo "📝 Recent Logs (last 10 lines):"
    tail -10 logs/kiwi_app.log 2>/dev/null || echo "   No logs found"
    
    echo ""
    echo "🌍 Access URL: Check logs for the exact port number"
    echo "   Format: http://localhost:[PORT]"
    
else
    echo "❌ Application Status: NOT RUNNING"
    echo ""
    echo "🚀 To start the application:"
    echo "   cd /workspace/kiwi"
    echo "   python src/kiwi/kiwi_app.py"
fi

echo ""
echo "📖 For more details, see: APPLICATION_STATUS.md"